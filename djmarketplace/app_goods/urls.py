from django.urls import path, include

from app_users.views import OrderCreateView
from app_goods.views import ShopsListView, ItemDetailView, ItemBuyView, ItemDismissView, \
    OrderDetailView, ItemListView, PriceUpdateView, BoughtItemsReport

urlpatterns = [

    path('items/', include([
        path('list/', ItemListView.as_view(), name='item_list'),
        path('<int:pk>/', include([
            path('detail/', ItemDetailView.as_view(), name='item_detail'),
            path('<int:shop_pk>/buy/', ItemBuyView.as_view(), name='buy_item'),
            path('<int:shop_pk>/dismiss/', ItemDismissView.as_view(), name='dismiss_item')
        ])),
    ])),
    path('orders/', include([
        path('create/', OrderCreateView.as_view(), name='create_order'),
        path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    ])),
    path('shops', ShopsListView.as_view(), name='shops_list'),
    path('update-prices', PriceUpdateView.as_view(), name='update_prices'),
    path('bought-items-report/', BoughtItemsReport.as_view(), name='bought_items_report')
]
