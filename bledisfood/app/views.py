from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework import response
from rest_framework import decorators
from rest_framework import parsers
from rest_framework.permissions import BasePermission, IsAuthenticated


# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class AllergenView(viewsets.ModelViewSet):
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer


class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class VendorFilter(filters.FilterSet):
    class Meta:
        model = Vendor
        fields = {
            'code_postal': ['exact'],
        }


class VendorView(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    filterset_class = VendorFilter


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CreditCardView(viewsets.ModelViewSet):
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer


class CustomerDetail(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_customer_by_user_id(self, request, u_id):
        customer = Customer.objects.all().get(user_id=u_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def detailInstance(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        Customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvoiceView(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class DishFilter(filters.FilterSet):
    class Meta:
        model = Dish
        fields = {
            'name': ['icontains'],
            'country': ['in'],
            'isVegan': ['icontains'],
            'isHalal': ['icontains'],
        }


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
            request.user and
                request.user.is_authenticated):
            return True
        return False


class DishView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filterset_class = DishFilter


class AllergenDishView(viewsets.ModelViewSet):
    queryset = AllergenDish.objects.all()
    serializer_class = AllergenDishSerializer


class TypeDishView(viewsets.ModelViewSet):
    queryset = TypeDish.objects.all()
    serializer_class = TypeDishSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class DetailedOrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = DetailedOrderSerializer


class ContentView(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def get_object(self, pk):
        return Content.objects.get(pk=pk)

    def detailInstance(self, request, pk, format=None):
        content = self.get_object(pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def contentsbyDetailedOrder(self, request, pk, format=None):
        contents = Content.objects.all()
        contentsByOrder = []
        for c in contents:
            print(pk)
            print(c.order.id)
            if(c.order.id == pk):
                contentsByOrder.append(c)
        serializer = ContentSerializer(contentsByOrder, many=True)
        return Response(data=serializer.data)


class DishListByRate(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    def list(self, request, *args, **kwargs):
        lst = Dish.objects.all().order_by('-rating')
        serializer = DishSerializer(lst, many=True)
        return Response(data=serializer.data)


class DishDetail(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        return Dish.objects.get(pk=pk)

    def detailInstance(self, request, pk, format=None):
        dish = self.get_object(pk)
        serializer = DishSerializer(dish)
        return Response(serializer.data)

    def dishesByVendor(self, request, pk, format=None):
        dishes = Dish.objects.all()
        dishesByVendor = []
        for d in dishes:
            if(d.vendor.id == pk):
                dishesByVendor.append(d)
        serializer = DishSerializer(dishesByVendor, many=True)
        return Response(data=serializer.data)

    def allergensByDish(self, request, pk, format=None):
        allergenDishes = AllergenDish.objects.all()
        allergensByDish = []
        for ad in allergenDishes:
            if(ad.dish.id == pk):
                allergensByDish.append(ad)
        serializer = AllergenDishSerializer(allergensByDish, many=True)
        return Response(data=serializer.data)

    def put(self, request, pk, format=None):
        dish = self.get_object(pk)
        serializer = DishSerializer(dish, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dish = self.get_object(pk)
        dish.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorDetail(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_object_by_user_id(self, request, u_id):
        vendor = Vendor.objects.all().get(user_id=u_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            raise Http404

    def detailInstance(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vendor = self.get_object(pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vendor = self.get_object(pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def detailedOrdersByVendor(self, request, pk, format=None):
        detailedOrders = Order.objects.all()
        detailerOrdersByVendor = []
        for do in detailedOrders:
            print(pk)
            print(do.vendor.id)
            if(do.vendor.id == pk):
                detailerOrdersByVendor.append(do)
        serializer = DetailedOrderSerializer(
            detailerOrdersByVendor, many=True)
        return Response(data=serializer.data)


class CustomerDetail(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object_by_user_id(self, request, u_id):
        customer = Customer.objects.all().get(user_id=u_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def detailInstance(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def detailedOrdersByCustomer(self, request, pk, format=None):
        detailedOrders = Order.objects.all()
        detailerOrdersByCustomer = []
        for do in detailedOrders:
            print(pk)
            print(do.customer.id)
            if(do.customer.id == pk):
                detailerOrdersByCustomer.append(do)
        serializer = DetailedOrderSerializer(
            detailerOrdersByCustomer, many=True)
        return Response(data=serializer.data)

    def put(self, request, pk, format=None):
        customer = self.get_object(pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        customer = self.get_object(pk)
        Customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AllergenDetail(viewsets.ModelViewSet):
    queryset = Allergen.objects.all()
    serializer_class = AllergenSerializer

    def get_object(self, pk):
        try:
            return Allergen.objects.get(pk=pk)
        except Allergen.DoesNotExist:
            raise Http404

    def detailInstance(self, request, pk, format=None):
        allergen = self.get_object(pk)
        serializer = AllergenSerializer(allergen)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        allergen = self.get_object(pk)
        serializer = AllergenSerializer(allergen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        allergen = self.get_object(pk)
        allergen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def detailInstance(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class TypeDishDetail(viewsets.ModelViewSet):
    def get_object(self, pk):
        return TypeDish.objects.get(pk=pk)

    def detailInstance(self, request, pk, format=None):
        td = self.get_object(pk)
        serializer = TypeDishSerializer(td)
        return Response(serializer.data)


class OrderDetail(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object_by_user_id(self, request, u_id):
        order = Order.objects.all().get(user_id=u_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def detailInstance(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DetailedOrderDetail(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = DetailedOrderSerializer

    def get_object(self, pk):
        return Content.objects.get(pk=pk)

    def get_order(self, pk):
        return Order.objects.get(pk=pk)

    def detailInstance(self, request, pk, format=None):
        content = self.get_object(pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data)

    def contentsbyDetailedOrder(self, request, pk, format=None):
        contents = Content.objects.all()
        contentsByOrder = []
        for c in contents:
            if(c.order.id == pk):
                contentsByOrder.append(c)
        serializer = ContentSerializer(contentsByOrder, many=True)
        # order = self.get_order(pk)
        # serializer = DetailedOrderSerializer(order)
        return Response(serializer.data)
