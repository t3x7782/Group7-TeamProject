from rest_framework import serializers
<<<<<<< Updated upstream
from .models import Book, Author
=======
from .models import Book, Author, Comments, Rating, Users
>>>>>>> Stashed changes


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
<<<<<<< Updated upstream
=======


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('user', 'book', 'comment', 'created_at')


# Cairo
'''
Serializer for Users model. This is what determines the response to GET requests. Sets the model as Users from models.py,
sets the output fields as the ID, username, first name, last name, and home address. 
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username','first_name', 'last_name', 'HomeAddress')

'''
Serializer for Total Price. This is what determines the response to GET requests. Sets the total_price as a FloatField()
and the cart_items as a BookSerializer object and enables processing of multiple objects 
'''
class UserTotalPriceSerializer(serializers.Serializer):
    total_price = serializers.FloatField()
    cart_items = BookSerializer(many=True)

# Cairo
>>>>>>> Stashed changes
