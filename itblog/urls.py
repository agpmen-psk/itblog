from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from app import forms, views


urlpatterns = [
    path("", views.index, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    path("blog/", views.blog, name="blog"),
    path("blog/<int:post_id>/", views.blogpost, name="blogpost"),
    path("blog/new/", views.newpost, name="newpost"),

    path("catalog/", views.catalog, name="catalog"),
    path("catalog/category/<int:category_id>/", views.products_by_category, name="products_by_category"),
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),

    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/checkout/", views.checkout, name="checkout"),

    path("orders/", views.orders_list, name="orders_list"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),

    path("registration/", views.registration, name="registration"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="app/login.html",
            authentication_form=forms.LoginForm
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),

    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)