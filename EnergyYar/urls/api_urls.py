from django.urls import include, path

from apps.order.urls import v1_router as order_router
from apps.product.urls import v1_router as product_router
from apps.payment.urls import v1_router as payment_router

urlpatterns = [
    path('', include(order_router.urls)),
    path('', include(product_router.urls)),
    path('', include(payment_router.urls)),
]
