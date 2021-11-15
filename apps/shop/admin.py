from django.contrib import admin
from .models import Category, Brand, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class CategoryBrand(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Brand, CategoryBrand)


class CategoryProduct(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'old_price',
                    'rait', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'rait']
    list_editable = ['price', 'old_price', 'rait', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, CategoryProduct)
