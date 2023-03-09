from django.contrib import admin

# Register your models here.
from .models import Todo
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Todo)