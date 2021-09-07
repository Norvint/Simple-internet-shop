from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_goods.models import Item, Shop, ItemInShop, Cart, Order
from app_users.models import Profile


class UsersPagesTest(TestCase):
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
                               date_of_birth=datetime(year=1996, month=1, day=1))
        Order.objects.create(user=new_user, total_sum=1000, created=datetime.now(), items=1)

    def test_register_page(self):
        url = reverse('register')
        self.client.logout()
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.status_code, 200)

    def test_account_page(self):
        url = reverse('account')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/account.html')
        self.assertEqual(response.status_code, 200)

    def test_account_update_page(self):
        url = reverse('account_update')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/edit_account.html')
        self.assertEqual(response.status_code, 200)

    def test_add_balance_page(self):
        url = reverse('add_balance')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'users/add_balance.html')
        self.assertEqual(response.status_code, 200)
