from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import *
from django.db import IntegrityError
#from drf_writable_nested import WritableNestedModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password'
        )
        extra_kwargs = {
            'username': {'validators': []},
        }


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = '__all__'


class AllergenDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllergenDish
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        user = User.objects.create_user(**user_data)
        customer, created = Customer.objects.update_or_create(
            hasPaypal=validated_data.pop('hasPaypal'),
            isVegan=validated_data.pop('isVegan'),
            hasAllergies=validated_data.pop('hasAllergies'),
            user=user
        )
        return customer


class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Vendor
        fields = '__all__'  # A VOIR SI BESOIN DE MODIFIER __all__ AVEC LES BONS CHAMPS !!

    def create(self, validated_data):
        user_data = validated_data.pop('user', None)
        user = User.objects.create_user(**user_data)
        vendor, created = Vendor.objects.update_or_create(
            user=user,
            **validated_data
        )
        return vendor


class TypeDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDish
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):
    #vendor = serializers.SlugRelatedField(queryset=Vendor.objects.all(),slug_field = 'IBAN')
    vendor = VendorSerializer(many=False, read_only=False)
    allergens = AllergenSerializer(many=True)

    class Meta:
        model = Dish
        fields = '__all__'

    def create(self, validated_data):
        allergens_data = validated_data.pop('allergens')
        vendor_data = validated_data.pop('vendor', None)
        vendor = Vendor.objects.get(IBAN=vendor_data.pop('IBAN'))
        dish = Dish.objects.create(vendor=vendor, **validated_data)
        for allergen_data in allergens_data:
            alle = Allergen.objects.get(**allergen_data)
            AllergenDish.objects.create(dish=dish, allergen=alle)
        return dish

    def update(self, instance, validated_data):
        instance.isActive = validated_data.get('isActive', instance.isActive)
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Order
        fields = '__all__'


"""
    def create(self, validated_data):
         date = validated_data.pop('date')
        isPayed = validated_data.pop('isPayed')
        customer =Customer.objects.getvalidated_data.pop('customer')
        vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
        state = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
        contents = models.ManyToManyField(

        allergens_data = validated_data.pop('allergens')
        vendor_data = validated_data.pop('vendor', None)
        vendor = Vendor.objects.get(IBAN=vendor_data.pop('IBAN'))
        dish = Dish.objects.create(vendor=vendor, **validated_data)
        for allergen_data in allergens_data:
            alle = Allergen.objects.get(**allergen_data)
            AllergenDish.objects.create(dish=dish, allergen=alle)
        return dish """


class ContentSerializer(serializers.ModelSerializer):
    dish = DishSerializer()
    order = OrderSerializer()

    class Meta:
        model = Content
        fields = '__all__'


class DetailedOrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    vendor = VendorSerializer()
    #contents = ContentSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    dish = DishSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
