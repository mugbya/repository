from django.contrib import admin
from qs.models import Question, Solution, Tag

# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'description')

# class SolutionAdmin(admin.ModelAdmin):
#     fields = ('content',)

class SolutionInline(admin.TabularInline):
    model = Solution
    template = 'admin/edit_inline/tabular.html'

class QuestionAdmin(admin.ModelAdmin):
    inlines = [SolutionInline]

admin.site.register(Tag, TagAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register([Solution,  ])