from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
<<<<<<< Updated upstream
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
=======
from .models import Book, Author, Comments, Rating, Users
from .serializers import BookSerializer, AuthorSerializer, CommentSerializer, RatingSerializer, UserSerializer, UserTotalPriceSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render
# Cairo
from rest_framework.views import APIView


>>>>>>> Stashed changes




@csrf_exempt
@api_view(['POST'])
def create_book(request):
    author_data = request.data.pop('author', None)
    if author_data:
        try:
            author = Author.objects.get(
                first_name=author_data['first_name'],
                last_name=author_data['last_name']
            )
        except Author.DoesNotExist:
            author_serializer = AuthorSerializer(data=author_data)
            if author_serializer.is_valid():
                author = author_serializer.save()
            else:
                return Response(author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
        else:
            return Response({'error': 'Author already exists'}, status=status.HTTP_400_BAD_REQUEST)
    book_serializer = BookSerializer(data=request.data)
    if book_serializer.is_valid():
        book_serializer.save(author=author)
        
        return Response(book_serializer.data, status=status.HTTP_201_CREATED)
    return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def retrieve_book(request, isbn):
    try:
        book = Book.objects.get(isbn=isbn)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book)
    return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def create_author(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        author = serializer.save()
        serialized_author = AuthorSerializer(author)
        return Response(serialized_author.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
def list_books_by_author(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    books = author.book_set.all()
    serializer = BookSerializer(books, many=True)
<<<<<<< Updated upstream
    return Response(serializer.data)
=======
    return Response(serializer.data)



#priscilla's views
class book_list(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class book_individual(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class comment_list(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

class comment_individual(generics.RetrieveUpdateDestroyAPIView):    
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

class rating_list(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class rating_individual(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

def book_comments(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    comments = Comments.objects.filter(book=book)
    serializer = CommentSerializer(comments, many=True)
    return JsonResponse(serializer.data, safe=False)

def book_rating_average(request, book_id):
    book = Book.objects.get(id=book_id)
    ratings = Rating.objects.filter(book=book)
    total_rating = 0
    for rating in ratings:
        total_rating += rating.rating
    average_rating = total_rating / len(ratings)
    context = {'book': book, 'average_rating': average_rating}
    return render(request, 'book_rating_average.html', context)

#@api_view(['GET'])
#def book_average_rating(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    avg_rating = None
    if book.ratings is not None:
        avg_rating = book.ratings.aggregate(Avg('rating')).get('rating__avg')
    if avg_rating is not None:
        avg_rating = round(avg_rating, 2)
    else:
        avg_rating = 'N/A'
    data = {'avg_rating': avg_rating}
    return JsonResponse(data)


# Cairo
'''
API view for Users. This determines what kind of requests can be sent and what they can do. Uses generics module to 
avoid creating specific functions to handle requests. The ListCreateAPIView allows new users to be created and allows 
the entire list of users in the database to be viewed. Sets the queryset as all objects in the User model from models.py
and uses the User serializer from serializers.py    
'''
class UserList(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

'''
Second API view for Users. Uses RetrieveUpdateDestroyAPIView from generics module to allow for retrieval of singular 
users, update user information in the database, and destroy users in the database. Sets the queryset as all objects in 
the User model from models.py and uses the User serializer from serializers.py
'''
class UserIndividual(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

'''
API view for a users shopping cart. Uses ListAPIView to return the list of book objects in a specific users shopping 
cart. Sets the serializer class to BookSerializer because that is the output object and overrides get_queryset to 
retrieve the user_id from the URL using kwargs['user_id'] with 'user_id' being the reference in the URL path then gets
the user object using get(id=user_id) and finally sets the queryset as the result of the GetCart method from the user
object. 
'''
class UserShoppingCartList(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(Users, pk=user_id)
        queryset = user.GetCart()

        return queryset

'''
API view for adding a book to the users shopping cart. Uses APIView and overrides the post method to get the user object
using the user_id and book_id provided in the URL to retrieve the user and book object then uses the .add() method to 
add the book object to the user Cart then returns a response with a string saying the book was successfully added to 
the cart. 
'''
class UserAddBookToCart(APIView):
    def post(self, request, user_id, book_id):
        user = get_object_or_404(Users, pk=user_id)
        book = get_object_or_404(Book, pk=book_id)

        user.Cart.add(book)

        return Response({f'Successfully added book ID: {book_id} to cart'}, status=status.HTTP_200_OK)

'''
Destroy APIView for removing books from the users cart. Retrieves the user and book object from the user_id and book_id
from the URl and checks them using get_object_or_404 which will return 404 if the object doesnt exist then uses 
.remove() to remove the book object from the user cart and returns a string confirming the book was removed from the 
cart.  
'''
class UserRemoveBookFromCart(generics.DestroyAPIView):
    def delete(self, request, user_id, book_id):
        user = get_object_or_404(Users, pk=user_id)
        book = get_object_or_404(Book, pk=book_id)

        user.Cart.remove(book)

        return Response({f'Successfully removed book ID: {book_id} from cart'}, status=status.HTTP_200_OK)

'''
Uses ListAPIView to return the total price using the TotalPrice method from the User model. sets the serializer as the 
UserShoppingCartTotal to handle the output of .TotalPrice() and and .Cart.all() then overrides the get method to 
retrieve the user object and its cart attribute then implements the .TotalPrice() method, storing the response in the 
total_price variable. user.Cart.all() returns a list of book objects which isnt readable by JSON so cart_items 
serializes the book objects and allows the cart items to shown in the response.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
'''
class UserShoppingCartTotal(generics.ListAPIView):
    serializer_class = UserTotalPriceSerializer

    def get(self, request, user_id):
        user = get_object_or_404(Users, pk=user_id)
        cart = user.Cart.all()
        total_price = user.TotalPrice()
        cart_items = [BookSerializer(book).data for book in cart]

        data = {
            'The total price is': total_price,
            'cart_items': cart_items,
        }

        return Response(data)

'''
API view for Books. Uses ListCreateAPIView from the generics module to allow new users to be created and allows the 
entire list of users in the database to be viewed. Sets the queryset as all objects in the Books model from models.py 
and uses the Book serializer from serializers.py    
'''
class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

'''
Second API view for Books. Uses RetrieveUpdateDestroyAPIView from generics module to allow for retrieval of singular 
book, update book information in the database, and destroy books in the database. Sets the queryset as all objects in 
the Books model from models.py and uses the Book serializer from serializers.py
'''
class BookIndividual(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
# Cairo

>>>>>>> Stashed changes
