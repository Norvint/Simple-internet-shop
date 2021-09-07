from django.urls import path, include

from app_users.views import RegisterView, UserEditView, \
    AddBalanceView, AccountDetailView, ItemBuyFromCartView, ItemDismissFromCartView, LogoutView, LoginView, \
    RestorePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', include([
        path('detail/', AccountDetailView.as_view(), name='account'),
        path('update/', UserEditView.as_view(), name='account_update'),
        path('add-balance/', AddBalanceView.as_view(), name='add_balance'),
        path('item-<int:pk>/store-<int:shop_pk>/', include([
            path('buy/', ItemBuyFromCartView.as_view(), name='buy_item_from_cart'),
            path('dismiss/', ItemDismissFromCartView.as_view(), name='dismiss_item_from_cart')
        ]))
    ])),
    path('restore_password/', RestorePasswordView.as_view(), name='restore_password'),
]
