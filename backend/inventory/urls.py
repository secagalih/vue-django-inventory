from django.urls import path

from .views import (
    ProductListView,
    ProductCreateView,
    ProductDeleteView,
    ProductUpdateView,
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/create/", ProductCreateView.as_view(), name="product-create"),
    path(
        "products/update/<uuid:pk>", ProductUpdateView.as_view(), name="product-update"
    ),
    path(
        "products/delete/<uuid:pk>", ProductDeleteView.as_view(), name="product-delete"
    ),
]
