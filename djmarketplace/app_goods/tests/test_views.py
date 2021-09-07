from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_goods.models import Item, Cart, Order, Shop, ItemInShop
from app_users.models import Profile


class GoodsViewsTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.get(username='testuser')
        self.client.force_login(user=user)

    @classmethod
    def setUpTestData(cls):
        new_user = User.objects.create_superuser('testuser')
        Item.objects.create(code='ASG32', price=1200, description='Тестовый товар')
        Shop.objects.create(title='Тестовый магазин', address='Тестовый адрес')
        ItemInShop.objects.create(item=Item.objects.first(), shop=Shop.objects.first(), quantity=1000)
        Profile.objects.create(user=new_user, city='Тестовый', phone_number='1234567890',
                               date_of_birth=datetime(year=1996, month=1, day=1))
        Order.objects.create(user=new_user, total_sum=1000, created=datetime.now(), items=1)

    def test_buy_from_catalog_view(self):
        shop = Shop.objects.first()
        item = Item.objects.first()
        url = reverse('buy_item', kwargs={'pk': item.pk, 'shop_pk': shop.pk})
        response = self.client.post(url)
        item_in_shop = ItemInShop.objects.first()
        cart = Cart.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(item_in_shop.quantity, 999)
        self.assertEqual(cart.items, 1)

    def test_dismiss_from_catalog_view(self):
        shop = Shop.objects.first()
        item = Item.objects.first()
        for x in range(5):
            url = reverse('buy_item', kwargs={'pk': item.pk, 'shop_pk': shop.pk})
            self.client.post(url)
        url = reverse('dismiss_item', kwargs={'pk': item.pk, 'shop_pk': shop.pk})
        response = self.client.post(url)
        item_in_shop = ItemInShop.objects.get(shop=shop, item=item)
        cart = Cart.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(item_in_shop.quantity, 996)
        self.assertEqual(cart.items, 4)

    def test_create_order_view(self):
        shop = Shop.objects.first()
        item = Item.objects.first()
        for x in range(5):
            url = reverse('buy_item', kwargs={'pk': item.pk, 'shop_pk': shop.pk})
            self.client.post(url)
        url = reverse('create_order')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Order.objects.all()), 2)
