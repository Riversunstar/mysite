from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name="blog_list"),
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blog_with_types, name="blog_with_types"),
    path('date/<int:year>/<int:month>', views.blog_with_date, name="blog_with_date"),
]


# 参数是<int:blog_type_pk>这种，这个的意思是需要传一个名叫blog_type_pk的整数型参数给views的处理方法