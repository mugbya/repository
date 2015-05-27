from django.contrib import admin
from operations.models import Classification,Contact,Tag


# Register your models here.

class TagInline(admin.TabularInline):
    model = Tag


class ContactAdmin(admin.ModelAdmin):
    # list_display = ('name', 'age', 'email') # list
    # search_fields = ('name',)

    inlines = [TagInline]  # Inline
    fieldsets = (
        ['Main',{
            'fields':('name','email'),
        }],
        ['Advance',{
            'classes': ('collapse',), # CSS
            'fields': ('age',),
        }]
    )

# admin.site.register([Classification, Contact, Tag])

admin.site.register(Contact, ContactAdmin)
admin.site.register([Classification, Tag])
