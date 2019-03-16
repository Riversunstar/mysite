import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from reading_statistics.models import ReadNum, ReadDetail
from blog.models import Blog

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj) #获取一个model
    key = '%s_%s_read' % (ct.model, obj.pk)
    if not request.COOKIES.get(key):            
            # 总阅读量
            # get_or_create:存在则取出,不存在则创建
            readnum, created = ReadNum.objects.get_or_create(content_type = ct, object_id = obj.pk )
            readnum.read_num += 1  #阅读数加1
            readnum.save()
            # 当天阅读量
            date = datetime.date.today()            
            readDetail, created = ReadDetail.objects.get_or_create(content_type = ct, object_id = obj.pk, date = date)
            readDetail.read_num += 1
            readDetail.save()
    return key

def get_seven_day_read_data(content_type):
    # 前7天,每一天的各个博客加起来的总阅读量
    today = datetime.date.today()
    dates = []
    read_nums = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days = i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type = content_type, date = date)
        result = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

def get_today_hot_blogs():
    today = datetime.date.today()    
    blogs = Blog.objects \
                .filter(read_details__date = today) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:5]

def get_yesterday_hot_blogs():
    today = datetime.date.today()
    date = today - datetime.timedelta(days = 1)
    blogs = Blog.objects \
                .filter(read_details__date = date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:5]

def get_7_days_hot_blogs():
    today = datetime.date.today()
    date = today - datetime.timedelta(days = 7)
    blogs = Blog.objects\
                .filter(read_details__date__lt = today, read_details__date__gte = date) \
                .values('id', 'title') \
                .annotate(read_num_sum = Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:5]





