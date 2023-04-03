from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author, WishList, BookItem
from .serializers import BookSerializer, AuthorSerializer, WishListSerializer, BookItemSerializer
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

@csrf_exempt
@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
def wishlist_list(request):
    if request.method == 'GET':
        wishlists = WishList.objects.all()
        serializer = WishListSerializer(wishlists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WishListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def wishlist_detail(request, pk):
    try:
        wishlist = WishList.objects.get(pk=pk)
    except WishList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WishListSerializer(wishlist)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WishListSerializer(wishlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
def bookitem_list(request):
    if request.method == 'GET':
        bookitems = BookItem.objects.all()
        serializer = BookItemSerializer(bookitems, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def bookitem_detail(request, pk):
    try:
        bookitem = BookItem.objects.get(pk=pk)
    except BookItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookItemSerializer(bookitem)
        return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def create_wishlist(request):
    user_id = request.data.get('user_id')
    wishlist_name = request.data.get('wishlist_name')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    # check if a wishlist with the given name already exists for this user
    if WishList.objects.filter(user=user, name=wishlist_name).exists():
        return Response({'error': 'Wishlist with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    wishlist = WishList(user=user, name=wishlist_name)
    wishlist.save()

    return Response({'success': 'Wishlist created successfully.'}, status=status.HTTP_201_CREATED)
    
@csrf_exempt
@api_view(['POST'])
def add_book_to_wishlist(request, wishlist_id, book_id):
    try:
        wishlist = WishList.objects.get(id=wishlist_id)
    except WishList.DoesNotExist:
        return Response({'error': 'Wishlist does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({'error': 'Book does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    data = {
    'wishlist': wishlist_id,
    'book': book_id
    }

    serializer = BookItemSerializer(data=data)
    if serializer.is_valid():
        book_item = serializer.save()
        book_item_data = BookItemSerializer(book_item).data
        return Response(book_item_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def remove_book_from_wishlist(request, wishlist_id, book_id):
    try:
        wishlist = Wishlist.objects.get(id=wishlist_id)
        bookitem = BookItem.objects.get(id=book_id, wishlist=wishlist)
        bookitem.delete()
        return Response(status=204)
    except Wishlist.DoesNotExist:
        return Response(status=404, data={'message': 'Wishlist not found'})
    except BookItem.DoesNotExist:
        return Response(status=404, data={'message': 'Book not found in wishlist'})

@csrf_exempt
@api_view(['GET'])
def wishlist_books(request, wishlist_id):
    try:
        wishlist = WishList.objects.get(id=wishlist_id)
    except WishList.DoesNotExist:
        return Response({'error': f'Wishlist with id {wishlist_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    book_items = wishlist.bookitem_set.all()
    books_data = []
    for book_item in book_items:
        book_serializer = BookSerializer(book_item.book)
        books_data.append(book_serializer.data)

    return Response(books_data)
    