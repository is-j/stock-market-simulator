from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


app_name = 'stock'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/import/', views.stock_detail, name='stock_detail'),
    path('accounts/register/', views.register, name='register'),
    path('transaction/list/', views.transaction_list, name = 'transaction_list'),
    path('transaction/create/', views.create_transaction, name = "create_transaction"),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
