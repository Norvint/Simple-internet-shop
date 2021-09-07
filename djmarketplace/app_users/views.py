from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django.views.generic.base import View

from app_goods.models import Cart, CartItem, Shop, Item, ItemInShop, OrderItem, Order, Offer
from app_users.forms import AddBalanceForm
from app_users.forms import AuthForm, UserForm, RestorePasswordForm, CustomRegistrationForm

from app_users.models import Profile


class AnotherLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True


class AnotherLogoutView(LoginRequiredMixin, LogoutView):
    next_page = '/'


class LoginView(FormView):
    form_class = AuthForm
    template_name = 'users/login.html'

    def post(self, request, *args, **kwargs):
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('main')
                else:
                    auth_form.add_error('__all__', 'Ошибка! Учетная запись пользователя неактивна.')
            else:
                auth_form.add_error('__all__', 'Ошибка! Проверьте правильность написания логина и пароля.')


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('main')


class OrderCreateView(LoginRequiredMixin, View):

    def post(self, *args, **kwargs):
        cart = self.request.user.cart
        if len(cart.items_in_cart.all()) > 0:
            order = Order.objects.create(user=self.request.user, total_sum=cart.total_sum,
                                         items=cart.items, created=datetime.now())
            for item_in_cart in cart.items_in_cart.all():
                OrderItem.objects.create(order=order, shop=item_in_cart.shop, item=item_in_cart.item,
                                         quantity=item_in_cart.quantity)
                item_in_cart.delete()
                self.request.user.profile.balance -= item_in_cart.quantity * item_in_cart.item.price
                self.request.user.profile.save()
            cart.total_sum = 0
            cart.items = 0
            cart.save()
        return redirect('account')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = CustomRegistrationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        Profile.objects.create(user=user, phone_number=form.cleaned_data['phone_number'],
                               city=form.cleaned_data['city'], balance=0,
                               date_of_birth=form.cleaned_data['date_of_birth'])
        login(self.request, user)
        return super().form_valid(form)


class AddBalanceView(LoginRequiredMixin, FormView):
    template_name = 'users/add_balance.html'
    form_class = AddBalanceForm
    success_url = '/app_users/account/detail/'

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        profile.balance += form.cleaned_data['quantity']
        profile.save()
        return super(AddBalanceView, self).form_valid(form)


class AccountDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        offers_cache_key = f'offers:{self.request.user.username}'
        if offers_cache_key not in cache:
            offers = Offer.objects.all()
            cache.set(offers_cache_key, offers, 30*60)
        else:
            offers = cache.get(offers_cache_key)
        context['orders'] = Order.objects.filter(user=self.request.user)
        context['offers'] = offers
        return context


class UserEditView(LoginRequiredMixin, TemplateView):
    template_name = 'users/edit_account.html'

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        form = UserForm()
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            Profile.objects.filter(user=request.user).update(city=form.cleaned_data['city'],
                                                             phone_number=form.cleaned_data['phone_number'],
                                                             date_of_birth=form.cleaned_data['date_of_birth'])
            return redirect('account')
        else:
            context['form'] = form
        return self.render_to_response(context)


class ItemBuyFromCartView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user)
        shop = Shop.objects.get(pk=kwargs.get('shop_pk'))
        item = Item.objects.get(pk=kwargs.get('pk'))
        try:
            item_in_cart = CartItem.objects.get(cart=cart, shop=shop, item=item)
            item_in_cart.quantity += 1
            item_in_cart.save()
        except CartItem.DoesNotExist:
            CartItem.objects.create(item=item, shop=shop, cart=cart, quantity=1)
        cart.total_sum += item.price
        cart.items += 1
        cart.save()
        items_in_shop = ItemInShop.objects.get(item=item, shop=shop)
        items_in_shop.quantity -= 1
        items_in_shop.save()
        return redirect('account')


class ItemDismissFromCartView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user)
        shop = Shop.objects.get(pk=kwargs.get('shop_pk'))
        item = Item.objects.get(pk=kwargs.get('pk'))
        item_in_cart = CartItem.objects.get(cart=cart, shop=shop, item=item)
        item_in_cart.quantity -= 1
        if item_in_cart.quantity == 0:
            item_in_cart.delete()
        else:
            item_in_cart.save()
        cart.total_sum -= item.price
        cart.items -= 1
        cart.save()
        items_in_shop = ItemInShop.objects.get(item=item, shop=shop)
        items_in_shop.quantity += 1
        items_in_shop.save()
        return redirect('account')


class RestorePasswordView(LoginRequiredMixin, FormView):
    form_class = RestorePasswordForm
    template_name = 'users/restore_password.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = RestorePasswordForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            new_password = User.objects.make_random_password()
            try:
                current_user = User.objects.get(email=user_email)
                current_user.set_password(new_password)
                current_user.save()
                send_mail(subject='Восстановление пароля',
                          message=f'Новый пароль: {new_password}',
                          from_email='admin@company.com',
                          recipient_list=[form.cleaned_data['email']])
                return HttpResponse('Письмо с новым паролем было успешно отправлено')
            except User.DoesNotExist:
                form.add_error('email', 'Пользователь с таким адресом электронной почты не зарегистрирован.')
        context['form'] = form
        return self.render_to_response(context)
