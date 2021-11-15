from django.contrib import admin
from .models import Order, OrderItem

@admin.action(description='Select status')
def make_status(modeladmin, request, queryset):
    queryset.update(status='progress')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated','status']
    list_filter = ['paid', 'created', 'updated']
    ordering = ['first_name']
    actions = [make_status]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
