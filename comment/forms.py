from django import forms
from django.contrib.contenttypes.models import ContentType 
from django.core.exceptions import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.IntegerField(widget=forms.HiddenInput())
    msg = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'),
                            error_messages={'required': '评论内容不能为空'})
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))



    def __init__(self, *args, **kw):
        if 'user' in kw:
            self.user = kw.pop('user')
        super().__init__(*args, **kw)
        

    def clean(self):
        # 验证用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录') 
        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model = content_type).model_class()
            model_obj = model_class.objects.get(pk = object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
       
        return self.cleaned_data

    def clean_reply_comment_id(self):
        # 验证parent
        reply_comment_id = self.cleaned_data['reply_comment_id']

        if reply_comment_id < 0 :
            raise form.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk = reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.get(pk = reply_comment_id)
        else:
            raise form.ValidationError('回复出错')
        return reply_comment_id




