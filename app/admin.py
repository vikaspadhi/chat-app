from django.contrib import admin
from .models import Chat,Group

# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display=['id','msg','group','timestamp']

admin.site.register(Chat,ChatAdmin)

class GroupAdmin(admin.ModelAdmin):
    list_display=['id','name']

admin.site.register(Group,GroupAdmin)
