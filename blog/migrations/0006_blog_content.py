# Generated by Django 2.1.5 on 2019-03-03 10:51

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_blog_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default='abc'),
        ),
    ]