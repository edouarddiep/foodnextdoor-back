from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django_countries.fields import CountryField
from django_iban.fields import IBANField

# Create your models here.


class Customer(models.Model):
    hasPaypal = models.BooleanField(null=True, blank=True)
    hasAllergies = models.BooleanField(null=True, blank=True)
    isVegan = models.BooleanField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if(self.user.first_name == ""):
            return self.user.username
        else:
            return self.user.first_name


class Vendor(models.Model):
    rating = models.FloatField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    IBAN = IBANField(null=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Param: upload_to='directory'
    photo = models.TextField(blank=True, null=True, max_length=None)
    no_rue = models.CharField(max_length=6)
    adresse = models.CharField(max_length=25)
    code_postal = models.PositiveIntegerField(
        validators=[MaxValueValidator(9999), MinValueValidator(1000)])
    ville = models.CharField(max_length=25)
    pays = models.CharField(max_length=25)

    def __str__(self):
        if(self.user.first_name == ""):
            return self.user.username
        else:
            return self.user.first_name


class TypeDish(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Allergen(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=25)
    price = models.FloatField(null=True)
    country = CountryField()
    howSpicy = models.PositiveIntegerField(
        null=True, validators=[MaxValueValidator(3), MinValueValidator(0)])
    isVegan = models.BooleanField(null=True)
    isHalal = models.BooleanField(null=True)
    # Param: upload_to='directory'
    photo = models.TextField(blank=True, null=True, max_length=None)
    typeDish = models.ForeignKey(
        TypeDish, on_delete=models.CASCADE, blank=True, null=True)
    vendor = models.ForeignKey(
        Vendor, blank=True, null=True, on_delete=models.CASCADE)
    allergens = models.ManyToManyField(Allergen, blank=True)
    isActive = models.BooleanField(null=True)
    rating = models.FloatField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    def __str__(self):
        return self.name


class AllergenDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    allergen = models.ForeignKey(Allergen, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish.name+" ("+self.allergen.name+")"


class OrderStatus(models.Model):
    state = models.PositiveIntegerField(
        null=True, validators=[MaxValueValidator(3), MinValueValidator(0)])

    def __str__(self):
        switcher = {
            1: "En préparation",
            2: "Prête",
            3: "Récupérée",
        }
        return str(switcher.get(self.state))


class Order(models.Model):
    date = models.DateTimeField(editable=True)
    isPayed = models.BooleanField(null=True, default=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    state = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    contents = models.ManyToManyField(
        Dish, through='Content', through_fields=('order', 'dish'))

    def __str__(self):
        return "Commande N°"+str(self.id)+" du "+("0"+str(self.date.day) if self.date.day < 10 else str(self.date.day))+"/"+("0"+str(self.date.month) if self.date.month < 10 else str(self.date.month))+"/"+str(self.date.year)+" | Statut : "+str(self.state)


class Content(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    price = models.FloatField(null=True)
    discount = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.quantity)+"x\""+self.dish.name+"\" "+("a" if self.quantity == 1 else "ont")+" été ajouté à la commande N°"+str(self.order.id)+" pour le prix total de CHF "+str(self.price)


class CreditCard(models.Model):
    IBAN = IBANField(null=True, default=None)
    cardHolderName = models.CharField(max_length=25)

    def __str__(self):
        return "Carte N°"+str(self.id)+" - Détenteur : "+self.cardHolderName+" | IBAN : "+self.iban


class Invoice(models.Model):
    date = models.DateTimeField(editable=True)

    def __str__(self):
        return "Facture N°"+str(self.id)+" du "+("0"+str(self.date.day) if self.date.day < 10 else str(self.date.day))+"/"+("0"+str(self.date.month) if self.date.month < 10 else str(self.date.month))+"/"+str(self.date.year)


class Comment(models.Model):
    body = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return "\""+self.body+"\" de "+self.user.username+" sur le plat \""+self.dish.name+"\" publié à "+str(self.date.hour)+"h"+("0"+str(self.date.minute) if self.date.minute < 10 else str(self.date.minute))+" le "+("0"+str(self.date.day) if self.date.day < 10 else str(self.date.day))+"/"+("0"+str(self.date.month) if self.date.month < 10 else str(self.date.month))+"/"+str(self.date.year)
