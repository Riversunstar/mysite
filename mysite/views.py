from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from reading_statistics.utils import get_seven_day_read_data, get_today_hot_blogs, get_yesterday_hot_blogs, get_7_days_hot_blogs
from blog.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_day_read_data(blog_content_type)
    # 获取7天热门博客缓存数据
    
    seven_day_hot_blogs = cache.get('seven_day_hot_blogs')
    if seven_day_hot_blogs is None:
        seven_day_hot_blogs = get_7_days_hot_blogs()
        cache.set('seven_day_hot_blogs', seven_day_hot_blogs, 3600)
    

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates    
    context['today_hot_blogs'] = get_today_hot_blogs()
    context['yesterday_hot_blogs'] = get_yesterday_hot_blogs()
    context['seven_day_hot_blogs'] = seven_day_hot_blogs
    return render(request, 'home.html', context)

def todo(request):
    context = {}
    return render(request, 'todo.html', context)

