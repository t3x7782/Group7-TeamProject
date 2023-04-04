from django.db import models
<<<<<<< Updated upstream
=======
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Cairo
from django.contrib.auth.models import AbstractUser

>>>>>>> Stashed changes

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

    def __str__(self):
<<<<<<< Updated upstream
        return self.name
=======
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


# Cairo
'''
Model for User information in database. Uses AbstractUser module to handle the common user info like name, password,
email. Adds field for name and home address. 
'''
class Users(AbstractUser):
    Name = models.CharField(max_length=500, null=True, blank=True)
    HomeAddress = models.TextField(max_length=500, null=True, blank=True)
    Cart = models.ManyToManyField(Book, blank=True, default=list)

    def GetCart(self):
        return self.Cart.all()

    def TotalPrice(self):
        total = 0

        if self.Cart.__sizeof__() == 0:
            return total
        else:
            for book in self.Cart.all():
                total += book.BookPrice

            return total
>>>>>>> Stashed changes
