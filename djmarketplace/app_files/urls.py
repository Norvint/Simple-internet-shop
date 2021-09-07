from django.urls import path

from app_files.views import FileSizeView, ForbiddenFileView, UpdatePricesView


urlpatterns = [
    path('file-size/', FileSizeView.as_view(), name='file_size'),
    path('validate-file/', ForbiddenFileView.as_view(), name='forbidden_file'),
    path('update-prices/', UpdatePricesView.as_view(), name='update_prices')
]
