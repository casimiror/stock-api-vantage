from django.urls import re_path
from stocker import views

urlpatterns = [
    re_path(r"^signup/$", views.create_user, name="index"),
    re_path(r"^login/$", views.login_user, name="bio"),
    re_path(r"^ticker/", views.get_ticker_prices, name="ticker"),
]
