from rest_framework import serializers
from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name',
                  'last_name',
                  'biography',
                  'publisher'  

       )


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ('id',
                  'isbn',
                  'name',
                  'description',
                  'price',
                  'author',
                  'genre',
                  'publisher',
                  'year_published',
                  'copies_sold'
        )
