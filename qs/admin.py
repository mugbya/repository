from django.contrib import admin
from qs.models import Qs,Tag,Category

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'category')

admin.site.register(Tag, TagAdmin)
admin.site.register([Qs,  Category])