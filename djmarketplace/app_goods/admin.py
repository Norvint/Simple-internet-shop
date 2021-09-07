from django.contrib import admin

from app_goods.models import Item, Shop, ItemInShop, Cart, CartItem, ItemImage, Offer, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'price']


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'image']


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'address']


@admin.register(ItemInShop)
class ItemInShopAdmin(admin.ModelAdmin):
    list_display = ['shop', 'item', 'quantity']


class CartItemInLine(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_sum']
    inlines = [CartItemInLine]


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active']


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_sum', 'created']
    inlines = [OrderItemInLine]
