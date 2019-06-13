from django import forms
from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}

# 创建一个与模型Entry相关联的表单，供用户添加新条目用
class EntryForm(forms.ModelForm):
    #Meta类指出了表单基于的模型以及要在表单中包含哪些字段
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text':''}
        #  widgets是一个HTML表单元素，通过设置属性widgets，可覆盖Django选择的
        # 的默认小部件。 Forms.Textarea,将文本区域的宽度设置为80 而不是默认的40列
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}