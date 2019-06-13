from django.contrib import admin
from learning_logs.models import Topic,Entry
# Register your models here.

# 向管理网站注册topic
admin.site.register(Topic)
admin.site.register(Entry)