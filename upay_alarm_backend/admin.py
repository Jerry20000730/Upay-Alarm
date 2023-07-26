from django.contrib import admin

from upay_alarm_backend.models import UserProfile, EmailVeriRecord


# define customized user mode
class UserProfileAdmin(admin.ModelAdmin):
    # visible columns
    list_display = ['username', 'email', 'buildingCode', 'floorCode', 'roomCode', 'is_active', 'is_staff']
    search_fields = ['email']
    list_filter = ['buildingCode', 'floorCode', 'roomCode']


# register the userprofile admin here
admin.site.register(UserProfile, UserProfileAdmin)


class EmailVeriRecordAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'send_time', 'expire_time', 'email_type']
    search_fields = ['email']
    list_filter = ['send_time', 'expire_time']


# register the emailVerification admin here
admin.site.register(EmailVeriRecord, EmailVeriRecordAdmin)
