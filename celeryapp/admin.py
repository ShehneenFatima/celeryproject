from django.contrib import admin
from celeryapp.models import Customer

class NoUtcFilter(admin.SimpleListFilter):
    title = 'UTC Conversion Status'
    parameter_name = 'utc_status'

    def lookups(self, request, model_admin):
        return (
            ('no_utc', 'No UTC Set'),
            ('has_utc', 'UTC Set'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no_utc':
            return queryset.filter(created_at_utc__isnull=True)
        elif self.value() == 'has_utc':
            return queryset.filter(created_at_utc__isnull=False)
        return queryset

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at_pst', 'created_at_utc', 'utc_converted')
    search_fields = ('name', 'email')
    list_filter = (NoUtcFilter, 'created_at_pst', 'created_at_utc')
    ordering = ('-created_at_pst',)
    readonly_fields = ('name', 'email', 'created_at_pst', 'created_at_utc')

    def utc_converted(self, obj):
        return obj.created_at_utc is not None
    utc_converted.boolean = True
    utc_converted.short_description = 'UTC Converted?'