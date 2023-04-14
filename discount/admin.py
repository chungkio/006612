from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Code, Status


class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['title','user_id', 'code', 'created_date']
    search_fields = ['title']

admin.site.register(Code, DiscountCodeAdmin)


class AccountInlineAdmin(admin.StackedInline):
    model = Status
    can_delete = True
    verbose_name_plural = 'Discount Settings'


class DiscountShowOnAcount(UserAdmin):
    inlines = (AccountInlineAdmin,)

admin.site.unregister(User)
admin.site.register(User, DiscountShowOnAcount)