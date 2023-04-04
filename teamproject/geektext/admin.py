from django.contrib import admin
from .models import Book, Author, Users
# Register your models here.

admin.site.register(Book)
<<<<<<< Updated upstream
admin.site.register(Author)
=======
admin.site.register(Author)
admin.site.register(Comments)
admin.site.register(Rating)

# Cairo
# Registers the models from the database to allow them to be viewed in the admin panel
admin.site.register(Users)
# Cairo

class BookAdmin(admin.ModelAdmin):
    fields = ('title', 'author', 'description', 'published_date', 'isbn_number')

class CommentAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'comment', 'created_at')

class RatingAdmin(admin.ModelAdmin):
    fields = ('user', 'book', 'rating', 'created_at')
>>>>>>> Stashed changes
