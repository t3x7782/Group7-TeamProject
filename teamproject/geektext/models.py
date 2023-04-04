from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser



class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField()
    publisher = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    isbn = models.CharField(max_length=13)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    year_published = models.IntegerField()
    copies_sold = models.IntegerField()
    ratings = models.ForeignKey('Rating', on_delete=models.CASCADE, related_name='books', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return f"Comment on {self.book}: {self.text}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    groups = models.ManyToManyField('auth.Group', related_name='auth_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='auth_user_permissions', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        app_label = 'geektext'


class CreditCard(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    card_number = models.CharField(max_length=16)
    card_type = models.CharField(max_length=255)
    expiration_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credit_cards', null=True, blank=True)

    class Meta:
        app_label = 'geektext'

    def __str__(self):
        return self.card_number
