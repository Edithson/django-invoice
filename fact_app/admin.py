from django.contrib import admin
from .models import *

# Register your models here.

class AdminCustomer(admin.ModelAdmin):
    list_display = ('name', 'sexe', 'age', 'zip_code', 'created_at', 'save_by')
    search_fields = ('name', 'zip_code')
    list_filter = ('sexe', 'age', 'created_at')
    readonly_fields = ('created_at', 'save_by')

    def save_model(self, request, obj, form, change):
        if not obj.save_by:
            obj.save_by = request.user
        obj.save()

class AdminInvoice(admin.ModelAdmin):
    list_display = ('customer', 'date', 'amount', 'paid', 'invoice_type', 'created_at', 'updated_at')
    search_fields = ('customer__name', 'invoice_type')
    list_filter = ('paid', 'invoice_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.save_by:
            obj.save_by = request.user
        obj.save()

class AdminArticle(admin.ModelAdmin):
    list_display = ('invoice', 'quantity', 'unit_price', 'get_total_price')
    search_fields = ('invoice__customer__name', 'description')
    list_filter = ('invoice__created_at',)
    readonly_fields = ('get_total_price',)

admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article, AdminArticle)
