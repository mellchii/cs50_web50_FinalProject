from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("product/<int:Product_id>", views.product, name="product"),
    path("category/<str:category>", views.category, name="category"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("stock", views.stock, name="stock"),
    path("results", views.search, name="results"),

    # API Routes
    path("edit/<int:Product_id>", views.edit, name="edit"),
    path("wish/<int:Product_id>", views.wish, name="wish"),
    path("review/<int:Product_id>", views.review, name="review"),
    path("all", views.all, name="all"),
    path("cart-count", views.cart_count, name="cart-count"),
    path("update-cart", views.update_cart, name="update-cart"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)