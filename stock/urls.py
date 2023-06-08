from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static


app_name = 'stock'

urlpatterns = [
    path('', views.index, name='index'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/import/', views.stock_detail, name='stock_detail'),
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
