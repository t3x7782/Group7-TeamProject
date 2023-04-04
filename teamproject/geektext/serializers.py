from rest_framework import serializers
from .models import Book, Author, Comments, Rating, User, CreditCard


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('first_name',
                  'last_name',
                  'biography',
                  'publisher'  

       )

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'book', 'rating', 'created_at')

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)

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
                  'copies_sold',
                  'ratings'
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('user', 'book', 'comment', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'home_address', 'groups', 'user_permissions']


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'name', 'card_number', 'card_type', 'expiration_date']

