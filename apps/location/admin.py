from django.contrib import admin
from apps.location.models import Region, District


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'code', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name_uz', 'code')
    ordering = ('name_uz',)
    readonly_fields = ('id', 'created_at', 'created_by', 'modified_at', 'modified_by')

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name_uz', 'code', 'is_active')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('created_at', 'created_by', 'modified_at', 'modified_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_uz', 'code', 'region', 'is_active', 'created_at')
    list_filter = ('is_active', 'region', 'created_at')
    search_fields = ('name_uz', 'code', 'region__name_uz')
    readonly_fields = ('id', 'created_at', 'created_by', 'modified_at', 'modified_by')
    autocomplete_fields = ['region']

    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('name_uz', 'code', 'region', 'is_active')
        }),
        ('Qo\'shimcha ma\'lumotlar', {
            'fields': ('created_at', 'created_by', 'modified_at', 'modified_by'),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "region":
            kwargs["queryset"] = Region.objects.filter(is_active=True, is_deleted=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)