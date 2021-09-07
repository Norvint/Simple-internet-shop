from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from app_files.models import UploadToPathAndRename


class Shop(models.Model):
    title = models.CharField(_('title'), max_length=200)
    address = models.CharField(_('address'), max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    def __str__(self):
        return self.title


class Item(models.Model):
    code = models.CharField(_('code'), max_length=100)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    description = models.CharField(_('description'), max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = _('good')
        verbose_name_plural = _('goods')

    def __str__(self):
        return self.code


class ItemInShop(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name=_('shop'), related_name='items_in_shop')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_('item'), related_name='items_in_shop')
    quantity = models.PositiveIntegerField(_('quantity'))

    class Meta:
        verbose_name = _('item quantity in shop')
        verbose_name_plural = _('items quantity in shops')

    def __str__(self):
        return f'{self.shop} - {self.item} - {self.quantity} шт.'


class ItemImage(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, verbose_name=_('item'), related_name='files')
    image = models.FileField(_('image'), upload_to=UploadToPathAndRename('items/'))

    class Meta:
        verbose_name = _('image of item')
        verbose_name_plural = _('images of items')

    def __str__(self):
        return f'{self.image} - {self.item}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    total_sum = models.DecimalField(_('total sum'), max_digits=10, decimal_places=2)
    created = models.DateField(_('created'), auto_now_add=True)
    items = models.PositiveIntegerField(_('items quantity'), default=0)
    score_accrued = models.BooleanField(_('score accrued'), default=False)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return f'Заказ №{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('order'), related_name='items_in_order')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name=_('shop'))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_('item'), related_name='item_in_orders')
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))

    class Meta:
        verbose_name = _('item in order')
        verbose_name_plural = _('items in orders')


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'), related_name='cart')
    total_sum = models.DecimalField(_('total sum'), max_digits=10, decimal_places=2, default=0)
    items = models.PositiveIntegerField(_('items quantity'), default=0)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return f'Корзина пользователя - {self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('cart'), related_name='items_in_cart')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name=_('shop'))
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name=_('item'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))

    class Meta:
        verbose_name = _('item in cart')
        verbose_name_plural = _('items in cart')

    def __str__(self):
        return f'{self.quantity} шт. {self.item} в корзине "{self.cart.user}"'


class Offer(models.Model):
    title = models.CharField(_('title'), max_length=100)
    description = models.CharField(_('description'), max_length=1000)
    created = models.DateField(_('creation date'), auto_now_add=True)
    term = models.PositiveIntegerField(_('term'))
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('offer')
        verbose_name_plural = _('offers')

    def __str__(self):
        return self.title
