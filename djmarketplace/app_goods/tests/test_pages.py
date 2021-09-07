from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_goods.models import Item, Order
from app_users.models import Profile


class GoodPagesTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.get_by_natural_key(username='testuser')
        self.client.force_login(user=user)

    @classmethod
    def setUpTestData(cls):
        new_user = User.objects.create_superuser('testuser')
        Profile.objects.create(user=new_user)
        Item.objects.create(code='ASG32', price=1200, description='Тестовый товар')
        Order.objects.create(user=new_user, total_sum=1000, created=datetime.now(), items=1)

    def test_item_list_page(self):
        url = reverse('item_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/items_list.html')

    def test_item_detail_page(self):
        item = Item.objects.first()
        url = reverse('item_detail', kwargs={'pk': item.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/item_detail.html')

    def test_order_detail_page(self):
        order = Order.objects.first()
        url = reverse('order_detail', kwargs={'pk': order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/order_detail.html')

    def test_shops_list_page(self):
        url = reverse('shops_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'goods/shops_list.html')
