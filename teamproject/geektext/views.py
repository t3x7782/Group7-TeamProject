from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author, Comments, Rating
from .serializers import BookSerializer, AuthorSerializer, CommentSerializer, RatingSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.shortcuts import get_object_or_404, render






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

