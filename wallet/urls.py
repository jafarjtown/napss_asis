from django.urls import path
from . import views

app_name = 'wallet'
urlpatterns = [
  path('', views.wallet, name='index'),
  path('virtual-top-up/data/', views.buy_data, name='buy_data'),
  path('virtual-top-up/airtime/', views.buy_airtime, name='buy_airtime'),
  path('virtual-top-up/airtime/buy/', views.purchase_airtime_with_wallet, name='purchase_airtime_with_wallet'),
  path('virtual-top-up/data/buy/', views.purchase_data_with_wallet, name='purchase_data_with_wallet'),
  path('generate/account/', views.generate_wallet, name='generate_account'),
  path('generate/link/', views.generate_link, name='generate_link'),
  path('generate/link/<id>/', views.use_generated_link, name='generated_link'),
  path('monnify/webhook/', views.monnify_webhook, name='monnify_webhook'),
  ]

