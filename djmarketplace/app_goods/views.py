from _csv import reader
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import View, TemplateView

from app_goods.forms import UploadPriceFileForm
from app_goods.models import Item, Shop, ItemInShop, Cart, CartItem, OrderItem, Order
from app_users.forms import BoughtItemsReportFilter


class ItemListView(ListView):
    model = Item
    template_name = 'goods/items_list.html'
    context_object_name = 'items_list'


class ShopsListView(ListView):
    template_name = 'goods/shops_list.html'
    queryset = Shop.objects.all()


class ItemDetailView(DetailView):
    template_name = 'goods/item_detail.html'
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        item = self.get_object()
        if self.request.user.is_authenticated:
            cart = Cart.objects.get(user=self.request.user)
            context['cart_items'] = CartItem.objects.filter(cart=cart, item=item)
        available_items = ItemInShop.objects.filter(item=item)
        context['available_items'] = available_items
        return context


class ItemBuyView(LoginRequiredMixin, View):

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
        return redirect('item_detail', pk=item.pk)


class ItemDismissView(LoginRequiredMixin, View):

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
        return redirect('item_detail', pk=item.pk)


class PriceUpdateView(LoginRequiredMixin, FormView):
    form_class = UploadPriceFileForm
    template_name = 'media/upload_file.html'

    def post(self, request, *args, **kwargs):
        upload_file_form = UploadPriceFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            price_file = upload_file_form.cleaned_data['file'].read()
            price_str = price_file.decode('utf-8').split('\n')[:-1]
            csv_reader = reader(price_str, delimiter=",", quotechar='"')
            for row in csv_reader:
                Item.objects.filter(code=row[0]).update(price=Decimal(row[1]))
            return HttpResponse(content='Цены были успешно обновлены', status=200)


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'goods/order_detail.html'
    model = Order


class BoughtItemsReport(LoginRequiredMixin, ListView):
    template_name = 'goods/bought_items_report.html'
    queryset = Item.objects.annotate(bought=Sum('item_in_orders__quantity'))
    context_object_name = 'bought_items'

    def get_context_data(self, **kwargs):
        context = super(BoughtItemsReport, self).get_context_data(**kwargs)
        filter_form = BoughtItemsReportFilter()
        context['filter_form'] = filter_form
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        filter_form = BoughtItemsReportFilter(request.POST)
        if filter_form.is_valid():
            first_date = filter_form.cleaned_data['first_date']
            second_date = filter_form.cleaned_data['second_date']
            if first_date:
                self.object_list = Item.objects.filter(item_in_orders__order__created__gte=first_date)
            if second_date:
                self.object_list = Item.objects.filter(item_in_orders__order__created__lte=second_date)
        self.object_list.annotate(bought=Sum('item_in_orders__quantity'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)



