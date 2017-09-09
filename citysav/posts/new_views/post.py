import json
import os
import PIL.Image
from PIL import ImageOps, ImageDraw
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from posts.models import Post, Comment, Upvote, Image, Thumbnail
from posts.serializers import PostSerializer, CommentSerializer, UpvoteSerializer


class PostList(APIView):
    def get(self, request, format=None):
        post = Post.objects.all().order_by('-id')
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = PostSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


@csrf_exempt
def image_upload(request, format=None):
    if request.method == 'POST':
        data = []
        post_id = request.POST.get('post_id')
        if post_id is None:
            raise ValidationError('post id not provided')
        #post_id = request.POST['post_id']
        post = Post.objects.get(id=post_id)

        i = Image.objects.filter(post_id=post.id).count()
        i = i + 1
        for f in request.FILES.getlist('uploadedfile'):
            filename = "image" + str(post.id) + str(i)
            destination = open('/tmp/' + filename + '.png', 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            img = Image.objects.create(post_id_id=post_id)
            img.image.save('IMG_' + str(img.id) + '.png',
                           File(open('/tmp/' + filename + '.png', 'r')))
            img.save()

            size = [50, 50]
            im = PIL.Image.open('/tmp/' + filename + '.png').convert('RGBA')
            im.thumbnail(size,
                         PIL.Image.ANTIALIAS)  # create thumbnail of image
            img1 = ImageOps.expand(
                im, border=2, fill='green')  # create border around thumbnail

            img2 = ImageOps.expand(im, border=2, fill='red')
            img3 = ImageOps.expand(im, border=2, fill='#00ffff')
            img4 = ImageOps.expand(im, border=2, fill='#f5c52c')
            (width1, height1) = img1.size
            width = width1 + 10
            height = height1 + 10
            im1 = PIL.Image.new("RGBA", (width, height),
                                "white")  # create transparent image
            im2 = PIL.Image.new("RGBA", (width, height), "white")
            im3 = PIL.Image.new("RGBA", (width, height), "white")
            im4 = PIL.Image.new("RGBA", (width, height), "white")

            transparent_area = (0, 0, width, height)
            mask = PIL.Image.new('L', im1.size, color=255)
            draw = ImageDraw.Draw(mask)
            draw.rectangle(transparent_area, fill=0)

            im1.putalpha(mask)
            im2.putalpha(mask)
            im3.putalpha(mask)
            im4.putalpha(mask)

            im1.paste(img1, (5, 0),
                      img1)  # paste thumbnail on transparent image
            im2.paste(img2, (5, 0), img2)
            im3.paste(img3, (5, 0), img3)
            im4.paste(img4, (5, 0), img4)

            x1 = (width / 2) - 5
            x2 = (width / 2)
            x3 = (width / 2) + 5

            draw1 = ImageDraw.Draw(im1)
            draw2 = ImageDraw.Draw(im2)
            draw3 = ImageDraw.Draw(im3)
            draw4 = ImageDraw.Draw(im4)

            draw1.polygon(
                (x1, height1, x2, height, x3, height1),
                fill='green')  # draw arrrow at the bottom of thumbnail
            draw2.polygon((x1, height1, x2, height, x3, height1), fill='red')
            draw3.polygon(
                (x1, height1, x2, height, x3, height1), fill='#00ffff')
            draw4.polygon(
                (x1, height1, x2, height, x3, height1), fill='#f5c52c')

            im1.save('/tmp/' + filename + '_green.png', 'PNG')
            im2.save('/tmp/' + filename + '_red.png', 'PNG')
            im3.save('/tmp/' + filename + '_blue.png', 'PNG')
            im4.save('/tmp/' + filename + '_yellow.png', 'PNG')

            thumbnail1 = Thumbnail.objects.create(
                post_id_id=post_id, status='closed',
                img_id_id=img.id)  # save thumbnail
            thumbnail1.image.save(
                'IMG_' + str(thumbnail1.id) + '.png',
                File(open('/tmp/' + filename + '_green.png', 'r')))
            thumbnail1.save()

            thumbnail2 = Thumbnail.objects.create(
                post_id_id=post_id, status='verification', img_id_id=img.id)
            thumbnail2.image.save(
                'IMG_' + str(thumbnail2.id) + '.png',
                File(open('/tmp/' + filename + '_red.png', 'r')))
            thumbnail2.save()

            thumbnail3 = Thumbnail.objects.create(
                post_id_id=post_id, status='review', img_id_id=img.id)
            thumbnail3.image.save(
                'IMG_' + str(thumbnail3.id) + '.png',
                File(open('/tmp/' + filename + '_blue.png', 'r')))
            thumbnail3.save()

            thumbnail4 = Thumbnail.objects.create(
                post_id_id=post_id, status='in-progress', img_id_id=img.id)
            thumbnail4.image.save(
                'IMG_' + str(thumbnail4.id) + '.png',
                File(open('/tmp/' + filename + '_yellow.png', 'r')))
            thumbnail4.save()

            send = {'url': img.image.url}
            data.append(send)
            i = i + 1
        return HttpResponse(data, content_type='application/json')


@csrf_exempt
def send_image(request, format=None):
    send_data = []
    jsondata = json.loads(request.body)
    post_id = jsondata['post_id']
    rows = Image.objects.filter(post_id_id=post_id)
    #rows = Image1.objects.filter(post=post_id)
    #for row in rows:
    for row in rows.iterator():
        #for row in range(1,4):
        image = getattr(row, 'image')
        post = getattr(row, 'post_id_id')
        id = getattr(row, 'id')
        #filename = file + str(row) + '.png'
        #image1 = open('/home/citysavior/citysav-python/citysav/uploads/'+filename,'rb')
        #image_read = image1.read()
        #image_64_encode=base64.encodestring(image_read)
        data = {'image_url': image.url, 'post_id': post, 'image_id': id}
        send_data.append(data)
    return JsonResponse(send_data)


class CommentList(APIView):
    def get(self, request, format=None):
        comment = Comment.objects.all().order_by('-comment_id')
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = CommentSerializer(
            data=request.data, context={'user': user})
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpvoteList(APIView):
    def get(self, request, format=None):
        upvote = Upvote.objects.all().order_by('-upvote_id')
        serializer = UpvoteSerializer(upvote, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = UpvoteSerializer(
            data=request.data, context={'user': user})
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def deleteImage(request, format=None):
    if (request.method == 'POST'):
        jsondata = json.loads(request.body)
        images = jsondata['no_of_images']
        no_of_images = int(0)
        images = int(images)
        for i in range(0, images):
            image_name = 'image' + str(i)
            image_id = jsondata[image_name]
            thumbnails = Thumbnail.objects.filter(
                img_id_id=image_id)  # get thumbnails for the image
            for thumbnail_row in thumbnails.iterator():
                thumbnail = getattr(thumbnail_row, 'image')
                thumbnail_url = thumbnail.url
                thumbnail_path = os.path.join(
                    settings.HOME_DIR, thumbnail_url[1:len(thumbnail_url)])
                if os.path.exists(thumbnail_path):
                    os.remove(thumbnail_path)  # delete thumbnail images
            Thumbnail.objects.filter(img_id_id=image_id).delete(
            )  # delete thumbnail enteries in thumbnail table
            row = Image.objects.get(id=image_id)  # get Image
            image_url = row.image.url
            image_path = os.path.join(settings.HOME_DIR,
                                      image_url[1:len(image_url)])
            if os.path.exists(image_path):  # delete image
                os.remove(image_path)
            Image.objects.filter(
                id=image_id).delete()  # delete image entry in Image table
            record = Image.objects.filter(id=image_id).count()
            record_thumbnail = Thumbnail.objects.filter(
                img_id_id=image_id).count()
            no_of_images = no_of_images + int(record) + int(record_thumbnail)
        rec = {'count': no_of_images}
        return JsonResponse(rec)


@csrf_exempt
def updatePostViews(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        post_id = jsondata['post_id']
        #views = jsondata['views']
        post = Post.objects.get(id=post_id)
        post.views = post.views + 1
        post.save()
        new_post = Post.objects.get(id=post_id)
        rec = {'views': new_post.views}
        return JsonResponse(rec)


# updated post_search - updated Response
def user_post(request, email=None, format=None):
    queryset = Post.objects.filter(email=email).order_by('-timestamp')
    serializer = PostSerializer(queryset, many=True)  # serializing the result
    return JsonResponse(serializer.data)


# updated post_search_nearby1 - updated Response
@csrf_exempt
def post_nearby(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        min_lat = jsondata['min_lat']
        min_lon = jsondata['min_lon']
        max_lat = jsondata['max_lat']
        max_lon = jsondata['max_lon']
        queryset = Post.objects.filter(
            lat__gt=min_lat, lat__lt=max_lat, lon__gt=min_lon,
            lon__lt=max_lon).order_by('id')
        serializer = PostSerializer(
            queryset, many=True)  # serializing the result
        return JsonResponse(serializer.data)


# updated send_image (not tested)
def get_image(request, post=None, format=None):
    send_data = []
    rows = Image.objects.filter(post_id_id=post)
    for row in rows.iterator():
        image = getattr(row, 'image')
        post = getattr(row, 'post_id_id')
        id = getattr(row, 'id')
        data = {'image_url': image.url, 'post_id': post, 'image_id': id}
        send_data.append(data)
    return JsonResponse(send_data)


# updated delete comment and update comment
class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# updated checkUpvote(updated - Response)
@csrf_exempt
def upvoteCheck(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        email = jsondata['email']
        post_id = jsondata['post_id']
        records = Upvote.objects.filter(email=email, post_id=post_id)
        serializer = UpvoteSerializer(records, many=True)
        return JsonResponse(serializer.data)


# updated getComments (updated - Response)
def getComment(request, post_id=None, format=None):
    comments = Comment.objects.filter(post_id=post_id).order_by('comment_id')
    serializer = CommentSerializer(comments, many=True)
    return JsonResponse(serializer.data)


# updated updateUpvote and decreaseUpvote(updated - 2 views combined to 1 and updated Response and request type changed to patch)
@csrf_exempt
def updatePostUpvote(request, format=None):
    if request.method == 'PATCH':
        jsondata = json.loads(request.body)
        post_id = jsondata['post_id']
        operate = jsondata['operate']
        post = Post.objects.get(id=post_id)
        upvote = post.upvotes
        if operate == 'increase':
            upvote = upvote + 1
        elif (operate == 'decrease' and upvote > 0):
            upvote = upvote - 1
        post.upvotes = upvote
        post.save()
        new_post = Post.objects.get(id=post_id)
        serializer = PostSerializer(new_post)
        return JsonResponse(serializer.data)


# updated cancelUpvote(updated - request type changed to delete and Response)
@csrf_exempt
def deleteUpvote(request, format=None):
    if request.method == 'DELETE':
        jsondata = json.loads(request.body)
        email = jsondata['email']
        post_id = jsondata['post_id']
        Upvote.objects.filter(email=email, post_id=post_id).delete()
        record = Upvote.objects.filter(email=email, post_id=post_id)
        serializer = UpvoteSerializer(record, many=True)
        return JsonResponse(serializer.data)


# updated updatePostViews (updated - request type changed to patch, Response type)
@csrf_exempt
def increasePostViews(request, format=None):
    if request.method == 'PATCH':
        jsondata = json.loads(request.body)
        post_id = jsondata['post_id']
        post = Post.objects.get(id=post_id)
        post.views = post.views + 1
        post.save()
        new_post = Post.objects.get(id=post_id)
        serializer = PostSerializer(new_post)
        return JsonResponse(serializer.data)


@csrf_exempt
def getThumbnail(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        post_id = jsondata['post_id']
        status = jsondata['status']
        send_data = []
        thumbnails = Thumbnail.objects.filter(
            post_id_id=post_id, status__iexact=status)
        for thumbnail in thumbnails.iterator():
            image = getattr(thumbnail, 'image')
            post = getattr(thumbnail, 'post_id_id')
            id = getattr(thumbnail, 'id')
            data = {
                'thumbnail_url': image.url,
                'post_id': post,
                'thumbnail_id': id
            }
            send_data.append(data)
        return JsonResponse(send_data)
