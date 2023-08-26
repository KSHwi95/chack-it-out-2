from django.contrib import admin
from .models import User, Favorite, Reading, Wish  


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "user_name", "registered_dttm")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "category")


class ReadingAdmin(admin.ModelAdmin):
    list_display = ("user", "book")

class WishAdmin(admin.ModelAdmin):
    list_display = ("user", "book")



# User 앱 관리자에서 보여주기
admin.site.register(User, UserAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Reading,ReadingAdmin)
admin.site.register(Wish, WishAdmin)

