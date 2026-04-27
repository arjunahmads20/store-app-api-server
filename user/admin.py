from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import (
    User, OTPVerification, UserInbox, InvitationRule, 
    UserInvitation, UserLog
)

#create custom form
class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'username', 'is_active', 'is_staff')

class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'username', 'is_active', 'is_staff')

class UserAdminCustom(admin.ModelAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'username', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    ordering = ('email',)
    add_form = UserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'username', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

admin.site.register(User, UserAdminCustom)
admin.site.register(OTPVerification)
admin.site.register(UserInbox)
admin.site.register(InvitationRule)
admin.site.register(UserInvitation)
admin.site.register(UserLog)
