from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'type_profil', 'is_approved')
    list_filter = ('type_profil', 'is_approved')
    search_fields = ('user__username',)
    actions = ['approve_profiles']

    def approve_profiles(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} profil(s) approuvé(s) avec succès.')
    approve_profiles.short_description = "Approuver les profils sélectionnés"

admin.site.register(Profile, ProfileAdmin)
