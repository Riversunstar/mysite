from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
from reading_statistics.models import ReadNumExpandMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length = 15)

    def __str__(self):
        return self.type_name
    #model_set反向获取外键实例的模型对象
    def blog_count(self):
        return self.blog_set.count()   

class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length = 30)
    blog_type = models.ForeignKey(BlogType, on_delete = models.CASCADE)
    content = RichTextUploadingField()
    read_details = GenericRelation(ReadDetail)
    author = models.ForeignKey(User, on_delete = models.CASCADE)    
    created_time = models.DateTimeField(auto_now_add = True)
    last_updated_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "<blog: %s >" % self.title

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    class Meta:
        ordering = ['-created_time']
        



  
