# Generated by Django 2.1.3 on 2019-08-03 13:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import django_iban.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='AllergenDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Allergen')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('price', models.FloatField(null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IBAN', django_iban.fields.IBANField(default=None, enforce_database_constraint=False, max_length=34, null=True)),
                ('cardHolderName', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hasPaypal', models.BooleanField(blank=True, null=True)),
                ('hasAllergies', models.BooleanField(blank=True, null=True)),
                ('isVegan', models.BooleanField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('price', models.FloatField(null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('howSpicy', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)])),
                ('isVegan', models.BooleanField(null=True)),
                ('isHalal', models.BooleanField(null=True)),
                ('photo', models.TextField(blank=True, null=True)),
                ('isActive', models.BooleanField(null=True)),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('allergens', models.ManyToManyField(blank=True, to='app.Allergen')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('isPayed', models.BooleanField(default=True, null=True)),
                ('contents', models.ManyToManyField(through='app.Content', to='app.Dish')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.PositiveIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(3), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='TypeDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('IBAN', django_iban.fields.IBANField(default=None, enforce_database_constraint=False, max_length=34, null=True)),
                ('photo', models.TextField(blank=True, null=True)),
                ('no_rue', models.CharField(max_length=6)),
                ('adresse', models.CharField(max_length=25)),
                ('code_postal', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(9999), django.core.validators.MinValueValidator(1000)])),
                ('ville', models.CharField(max_length=25)),
                ('pays', models.CharField(max_length=25)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.OrderStatus'),
        ),
        migrations.AddField(
            model_name='order',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Vendor'),
        ),
        migrations.AddField(
            model_name='dish',
            name='typeDish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.TypeDish'),
        ),
        migrations.AddField(
            model_name='dish',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Vendor'),
        ),
        migrations.AddField(
            model_name='content',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Dish'),
        ),
        migrations.AddField(
            model_name='content',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Order'),
        ),
        migrations.AddField(
            model_name='comment',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Dish'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='allergendish',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Dish'),
        ),
    ]