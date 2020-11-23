from django.contrib import admin
from .models import *


class LineNotifyTokenAdmin(admin.ModelAdmin):
    pass


class LineNotifyGroupAdmin(admin.ModelAdmin):
    # 多對多項目設定
    filter_horizontal = ('members',)


admin.site.register(LineNotifyToken, LineNotifyTokenAdmin)
admin.site.register(LineNotifyGroup, LineNotifyGroupAdmin)
