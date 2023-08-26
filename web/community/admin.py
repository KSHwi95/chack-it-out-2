from django.contrib import admin
from .models import Community, Member, reviewMember


# Register your models here.
class CommunityAdmin(admin.ModelAdmin):
    list_display = ("id", "creator", "book", "meeting_date", "meeting_place", "creator")


class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


class reviewMemberAdmin(admin.ModelAdmin):
    list_display = ("community", "review")


admin.site.register(Community, CommunityAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(reviewMember, reviewMemberAdmin)
