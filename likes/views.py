from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import LikeCount, LikeRecord

def SuccessReseponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def ErrorReseponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    # 获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorReseponse(400, 'you were not login')

    content_type = request.GET.get('content_type') #从前端拿回来的只是一个str,并不是真正的ContentType对象
    object_id = int(request.GET.get('object_id')) #同理这里的id也是str,要用int转化为数字

    try:
        content_type = ContentType.objects.get(model=content_type) 
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk = object_id)
    except ObjectDoesNotExist:
        return ErrorReseponse(401, 'object not exist')
    
    # 处理数据
    if  request.GET.get('is_like') == 'true':
        # 要点赞       
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过,进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessReseponse(like_count.liked_num)
        else:
            # 已经点赞,不能重复点赞
            return ErrorReseponse(402, 'you were liked')      
    else:
        # 取消点赞
        if  LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过,取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessReseponse(like_count.liked_num)  
            else:
                return ErrorReseponse(404, 'data error')
        else:
            #没有点赞过不能取消
            return ErrorReseponse(403, 'you were not liked')
    