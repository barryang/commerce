from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Categories", views.category, name="categories"),
    path("Categories/<str:categories_name>", views.cat, name="category"),
    path("ActiveListings", views.activelistings, name="activelistings"),
    path("Watchlist", views.watchlist, name="watchlist"),
    path("Create", views.create, name="create"),
    path("<int:listing_id>", views.listing, name="listing"),
]
