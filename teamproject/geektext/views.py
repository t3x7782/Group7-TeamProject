from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt




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