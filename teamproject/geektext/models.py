from django.db import models

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
        return self.name