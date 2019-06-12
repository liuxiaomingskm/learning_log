from django.db import models
from django.contrib.auth.models import User
class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


class Entry(models.Model):

    """
    学到的有关某个主题的具体知识
    在django2.0后，定义外键和一对一关系的时候需要加on_delete选项，此参数为了避免两个表里的数据不一致问题，不然会报错：举例说明：
    user=models.OneToOneField(User)
    owner=models.ForeignKey(UserProfile)
    需要改成：
    user=models.OneToOneField(User,on_delete=models.CASCADE) --在老版本这个参数（models.CASCADE）是默认值
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    # 在Entry类中嵌套了Meta, Meta存储用于管理模型的的额外信息,在这里它使我们能够设置一个
    # 特殊属性， 让Django在需要时使用Entries来表示多个条目，如果没有这个类，Django将使用
    # Entrys来表示多个条目。。。。不是很明白。。
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50] + "..."
