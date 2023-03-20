from django.contrib import admin

from todo.models import Todo, Log
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Todo)
admin.site.register(Log)