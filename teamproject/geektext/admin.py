from django.contrib import admin
from .models import Book, Author, Comments, Rating
from .models import CreditCard, User, WishList, BookItem


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(CreditCard)
admin.site.register(User)
admin.site.register(WishList)
admin.site.register(BookItem)
class BookAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'description', 'published_date', 'isbn_number')

class CommentAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'comment', 'created_at')

class RatingAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'rating', 'created_at')