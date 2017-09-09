import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from posts.models import Member, Post, Upvote, Comment


#deprecated (updated - getLeaderboard)
def getLeaderBoard(request, format=None):
    queryset = Member.objects.exclude(email__in=[
        'citysavior1@gmail.com', 'riddhi@rechargers.co.in',
        'purnendu@rechargers.co.in', 'purnendurocks@gmail.com',
        'ridz.bagri@gmail.com'
    ]).order_by('-karma_points')[:20]
    data = serializers.serialize('json', queryset)
    return HttpResponse(data, content_type='application/json')


#deprecated (updated to get request - getUserRank)
@csrf_exempt
def getMyRank(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        points = jsondata['karma_points']
        rank = Member.objects.exclude(email__in=[
            'citysavior1@gmail.com', 'riddhi@rechargers.co.in',
            'purnendu@rechargers.co.in', 'purnendurocks@gmail.com',
            'ridz.bagri@gmail.com'
        ]).filter(karma_points__gt=points).count()
        rec = {'rank': rank}
        return JsonResponse(rec)


def post_search(request, email=None, format=None):
    queryset = Post.objects.filter(email=email).order_by('-timestamp')
    data = serializers.serialize('json', queryset)
    return HttpResponse(data, content_type='application/json')


def post_search_nearby(request, lat=None, lon=None, format=None):

    lat1 = float(lat) - 5.0
    lat2 = float(lat) + 5.0
    lon1 = float(lon) - 5.0
    lon2 = float(lon) + 5.0
    queryset = Post.objects.filter(
        lat__gt=lat1, lat__lt=lat2, lon__gt=lon1, lon__lt=lon2).order_by('id')
    data = serializers.serialize('json', list(queryset))
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def post_search_nearby1(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        min_lat = jsondata['min_lat']
        min_lon = jsondata['min_lon']
        max_lat = jsondata['max_lat']
        max_lon = jsondata['max_lon']

        queryset = Post.objects.filter(
            lat__gt=min_lat, lat__lt=max_lat, lon__gt=min_lon,
            lon__lt=max_lon).exclude(status='Archived').order_by('id')
        data = serializers.serialize('json', list(queryset))
        return HttpResponse(data, content_type='application/json')


# deprecated (updated - upvoteCheck )
# deprecated (updated - updatePostUpvote)
# deprecated (updated deleteUpvote)
# deprecated (updated - updatePostUpvote)
#deprecated (updated - getComment)


# deprecated (update - delete request to CommentDetail )
# deprecated (update - patch request to CommentDetail )


@csrf_exempt
def checkUpvote(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        email = jsondata['email']
        post_id = jsondata['post_id']
        records = Upvote.objects.filter(email=email, post_id=post_id).count()
        rec = {'count': records}
        return JsonResponse(rec)


@csrf_exempt
def updateUpvote(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        id1 = jsondata['post_id']
        post = Post.objects.get(id=id1)
        upvote = post.upvotes
        upvote = upvote + 1
        post.upvotes = upvote
        post.save()
        new_post = Post.objects.get(id=id1)
        rec = {'count': new_post.upvotes}
        return JsonResponse(rec)


@csrf_exempt
def cancelUpvote(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        email = jsondata['email']
        post_id = jsondata['post_id']
        Upvote.objects.filter(email=email, post_id=post_id).delete()
        record = Upvote.objects.filter(email=email, post_id=post_id).count()
        rec = {'count': record}
        return JsonResponse(rec)


@csrf_exempt
def decreaseUpvote(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        id1 = jsondata['post_id']
        post = Post.objects.get(id=id1)
        upvote = post.upvotes
        if upvote >= 0:
            upvote = upvote - 1
        post.upvotes = upvote
        post.save()
        new_post = Post.objects.get(id=id1)
        rec = {'count': new_post.upvotes}
        return JsonResponse(rec)


def getComments(request, post_id=None, format=None):
    comments = Comment.objects.filter(post_id=post_id).order_by('comment_id')
    data = serializers.serialize('json', list(comments))
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def deleteComment(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        comment_id = jsondata['comment_id']
        Comment.objects.filter(comment_id=comment_id).delete()
        record = Comment.objects.filter(comment_id=comment_id).count()
        rec = {'count': record}
        return JsonResponse(rec)


@csrf_exempt
def updateComment(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        comment_id = jsondata['comment_id']
        comment_text = jsondata['comment_text']
        comment = Comment.objects.get(comment_id=comment_id)
        comment.comment_text = comment_text
        comment.save()
        updated_comment = Comment.objects.get(comment_id=comment_id)
        rec = {'comment_text': updated_comment.comment_text}
        return JsonResponse(rec)


@csrf_exempt
def updatePost(request, format=None):
    if (request.method == 'POST'):
        jsondata = json.loads(request.body)
        post_id = jsondata['post_id']
        issueDes = jsondata['issueDes']
        post = Post.objects.get(id=post_id)
        post.desc = issueDes
        post.save()
        updated_post = Post.objects.get(id=post_id)
        rec = {'issueDes': updated_post.desc}
        return JsonResponse(rec)


@csrf_exempt
def member_update(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        email1 = jsondata['email']
        phone = jsondata['phone_number']
        name1 = jsondata['name']
        picture = jsondata['profile_picture']

        member = Member.objects.get(email=email1)
        if name1 != None:
            member.name = name1
            member.save()
        if phone != None:
            member.phone_number = phone
            member.save()
        if picture != None:
            member.profile_picture = picture
            member.save()
        queryset = Member.objects.filter(email=email1)
        data = serializers.serialize('json', list(queryset))
        return HttpResponse(data, content_type='application/json')


@csrf_exempt
def updateKarma(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        email1 = jsondata['email']
        #  operate = jsondata['operate']
        points = jsondata['karma_points']
        member = Member.objects.get(email=email1)
        #  karma = member.karma_points
        #  if(operate == "add"):
        #      karma = karma + points
        #  else :
        #      karma = karma - points

        member.karma_points = points
        member.save()
        new_member = Member.objects.get(email=email1)
        rec = {'count': new_member.karma_points}
        return JsonResponse(rec)
