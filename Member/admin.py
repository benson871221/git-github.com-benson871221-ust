from django.contrib import admin
from .models import School, Member

#admin顯示table欄位
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id','name','tel','address','website','image','public_private','union','school_system')
    ordering = ['id']

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id','name','identity','sex','birthday','tel','email','password','image','school_id')
    ordering = ['id']

# Register your models here.
admin.site.register(School, SchoolAdmin)
admin.site.register(Member, MemberAdmin)

