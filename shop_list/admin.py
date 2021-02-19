from django.contrib import admin
from .models import List, Review, TreatBrands

# Register your models here.
admin.site.register(List)
admin.site.register(TreatBrands)
admin.register(Review)

class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'review', 'author')
    list_filter = ('post', 'review', 'author')
    search_fields = ('post', 'review')
    raw_id_fields = ('author',) 