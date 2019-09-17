"""bledisfood URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import *
from rest_framework import routers
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm

router = routers.DefaultRouter()
router.register('customers', CustomerView)
router.register('vendors', VendorView)
router.register('dishes', DishView)
router.register('allergens', AllergenView)
router.register('allergenDish', AllergenDishView)
router.register('typeDish', TypeDishView)
router.register('invoices', InvoiceView)
router.register('comments', CommentView)
router.register('users', UserView)
router.register('orders', OrderView)
router.register('detailed-orders', DetailedOrderView)
router.register('contents', ContentView)

urlpatterns = [

    path('', include(router.urls)),

    path('dishes/rate-sorted', DishListByRate.as_view({
        'get': 'list',
        'get': 'listFilter'
    }), name='dish-sort-rate'),

    path('dishes/<int:pk>', DishDetail.as_view({
        'get': 'detailInstance'
    }), name='dish-detail'),
    path('vendors/<int:pk>', VendorDetail.as_view({
        'get': 'detailInstance',
    }), name='vendor-detail'),

    path('vendors/users/<int:u_id>', VendorDetail.as_view({
        'get': 'get_object_by_user_id'
    }), name='vendor-user-detail'),

    path('customers/users/<int:u_id>', CustomerDetail.as_view({
        'get': 'get_object_by_user_id'
    }), name='customer-user-detail'),

    path('vendors/<int:pk>/dishes/', DishDetail.as_view({
        'get': 'dishesByVendor'
    }), name='dishesByVendor'),

    path('dishes/<int:pk>/allergenDish/', DishDetail.as_view({
        'get': 'allergensByDish'
    }), name='allergensByDish'),

    path('allergens/<int:pk>', AllergenDetail.as_view({
        'get': 'detailInstance'
    }), name='allergen-detail'),

    path('users/<int:pk>', UserDetail.as_view({
        'get': 'detailInstance'
    }), name='user-detail'),

    path('typeDish/<int:pk>', TypeDishDetail.as_view({
        'get': 'detailInstance'
    }), name='typeDish-detail'),

    path('orders/<int:pk>', OrderDetail.as_view({
        'get': 'detailInstance'
    }), name='order-detail'),

    path('detailed-orders/<int:pk>', DetailedOrderView.as_view({
        'get': 'detailInstance'
    }), name='detailed-order'),

    path('detailed-orders/<int:pk>/contents/', DetailedOrderDetail.as_view({
        'get': 'contentsbyDetailedOrder'
    }), name='contents'),

    path('customers/<int:pk>/detailed-orders/', CustomerDetail.as_view({
        'get': 'detailedOrdersByCustomer'
    }), name='detailed-order-by-customer'),

    path('vendors/<int:pk>/detailed-orders/', VendorDetail.as_view({
         'get': 'detailedOrdersByVendor'
         }), name='detailed-order-by-vendor'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
