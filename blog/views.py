from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Blog, BlogType
from reading_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request, blogs_all_list):
    #创建分页器
    paginator = Paginator(blogs_all_list, settings.NUMBER_PER_PAGE)  
    page_num = request.GET.get('page', 1)           #获取url的页面参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)       #获取Page对象
    #页码显示范围
    page_range = [ x for x in range(page_of_blogs.number - 2, page_of_blogs.number + 3) 
                    if 0 < x < paginator.num_pages + 1 ]          
    #添加首页尾页和之间的省略号...
    if page_of_blogs.number > 3:           
        page_range.insert(0, 1)
        page_range.insert(1,'...')
    if page_of_blogs.number < paginator.num_pages - 2:
        page_range.insert(page_of_blogs.number  + 3, '...')
        page_range.append(paginator.num_pages)                 
    #获取日期归档的对应博客数量['blog_dates']
    blog_dates = Blog.objects.dates('created_time', 'month', 'DESC')
    blog_date_dict = {} 
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year = blog_date.year, 
                        created_time__month = blog_date.month ).count()
        blog_date_dict[blog_date] = blog_count

    context = {}
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.all()         
    context['blog_dates'] = blog_date_dict
    return context

def blog_list(request):   #获取blog模型的所有数据 才能打印出所有blog的列表
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request,'blog_list.html', context)

def blog_with_types(request,blog_type_pk):
    blog_types = get_object_or_404(BlogType, pk = blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type = blog_types)
    context = get_blog_list_common_data(request, blogs_all_list)        
    context['blog_type'] = blog_types    
    return render(request,'blog_with_types.html', context)

def blog_with_date(request, year, month):    
    blogs_all_list = Blog.objects.filter(created_time__year = year, created_time__month = month )   #该页显示所需的对象(博客)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = "%s年%s月" % (year, month)
    return render(request, 'blog_with_date.html', context)

def blog_detail(request, blog_pk):  #要读取blog列表的每一个blog所以有参数
    blog = get_object_or_404(Blog, pk = blog_pk)  #每个主键pk对应一个博客(键值) 
    read_cookie_key = read_statistics_once_read(request, blog)
    
    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt = blog.created_time ).last() 
    #把大于本键值的创建时间的所有博客筛选出来↑,last()把最后一篇即就是本键值的上一个键值提取出来
    context['next_blog'] = Blog.objects.filter(created_time__lt = blog.created_time ).first()
    context['blog'] = blog
    response = render(request, 'blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response












