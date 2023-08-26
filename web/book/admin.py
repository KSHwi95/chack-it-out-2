from django.contrib import admin
from .models import Book, Category, reviewUser, Review


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("book_isbn", "book_title", "book_author", "category")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")


# 댓글
class reviewUserAdmin(admin.ModelAdmin):
    list_display = ("book", "review")


# 알라딘
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "label")


# User 앱 관리자에서 보여주기
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(reviewUser, reviewUserAdmin)
admin.site.register(Review, ReviewAdmin)
