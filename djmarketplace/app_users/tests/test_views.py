from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_goods.models import Item, Shop, ItemInShop, Cart, Order
from app_users.models import Profile


class UsersViewsTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.get_by_natural_key(username='testuser')
        self.client.force_login(user=user)

    @classmethod
    def setUpTestData(cls):
        new_user = User.objects.create_superuser('testuser')
        Item.objects.create(code='ASG32', price=1200, description='Тестовый товар')
        Shop.objects.create(title='Тестовый магазин', address='Тестовый адрес')
        ItemInShop.objects.create(item=Item.objects.first(), shop=Shop.objects.first(), quantity=1000)
        Profile.objects.create(user=new_user, city='Тестовый', phone_number='1234567890',
                               date_of_birth=datetime(year=1996, month=1, day=1), balance=100000)
        Order.objects.create(user=new_user, total_sum=1000, created=datetime.now(), items=1)

    def test_add_balance_view(self):
        url = reverse('add_balance')
        response = self.client.post(url, data={'quantity': '100'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.first().profile.balance, 100100)

    def test_buy_item_from_cart_view(self):
        shop = Shop.objects.first()
        item = Item.objects.first()
        url = reverse('buy_item_from_cart', kwargs={'pk': item.pk, 'shop_pk': shop.pk})
        response = self.client.post(url)
        item_in_shop = ItemInShop.objects.get(shop=shop, item=item)
        self.assertEqual(Cart.objects.first().items, 1)
        self.assertEqual(item_in_shop.quantity, 999)
        self.assertEqual(response.status_code, 302)

    def test_dismiss_from_catalog_view(self):
        shop = Shop.objects.first()
        item = Item.objects.first()
        for x in range(5):
            url = reverse('buy_item_from_cart', kwargs={'pk': item.pk, 'shop_pk': shop.pk})
            self.client.post(url)
        url = reverse('dismiss_item_from_cart', kwargs={'pk': item.pk, 'shop_pk': shop.pk})
        response = self.client.post(url)
        cart = Cart.objects.first()
        item_in_shop = ItemInShop.objects.get(shop=shop, item=item)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(item_in_shop.quantity, 996)
        self.assertEqual(cart.items, 4)
