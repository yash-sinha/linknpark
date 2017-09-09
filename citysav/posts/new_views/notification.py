from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from posts.models import NotificationArea, Member, Post, Image
from posts.serializers import NotificationAreaSerializer
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from push_notifications.models import APNSDevice, GCMDevice
from gpxpy import geo
from django.conf import settings
from django.core.mail import send_mail


@csrf_exempt
def send_notification(request, format=None):
    #lat1 = 22.5848556
    #lon1 = 88.3580799
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body)
            lat = jsondata['lat']
            lon = jsondata['lon']
            post_id = jsondata['post_id']
            email = jsondata['email']
        except Exception as e:
            raise ValidationError('json error')

        send_users = []
        users = NotificationArea.objects.exclude(email=email)
        for user in users:
            dist = geo.haversine_distance(lat, lon, user.cen_lat, user.cen_lon)
            dist = dist / 1000
            if (dist <= user.radius):
                send_users.append(user.email)
        fcm_device = GCMDevice.objects.filter(name__in=send_users)
        fcm_device.send_message(
            'New issue posted in your area',
            extra={
                "priority": 2,
                "post": post_id,
                "visibility": 1,
                'icon': 'notif',
                'sound': 'default',
                'notId': post_id
            },
            use_fcm_notifications=False)

        #notification code for ios devices
        #apns_token = "22cfcc654ee2998fe911b71c2908a64295397875fa4308ce8ef616736a2616e0"
        #apns_device = APNSDevice.objects.get(registration_id=apns_token)
        apns_device = APNSDevice.objects.filter(name__in=send_users)
        apns_device.send_message(
            'New issue posted in your area',
            extra={
                "priority": 2,
                "post": post_id,
                "visibility": 1,
                'icon': 'notif',
                'sound': 'default'
            })

        res = {'response': 'ok'}
        return JsonResponse(res)

#deprecated (updated to class-based views - NotificationAreaList(for create) & NotificationAreaDetail(for update))
@csrf_exempt
def createOrUpdateArea(request, format=None):
    if request.method == 'POST':
        jsondata = json.loads(request.body)
        email = jsondata['email']
        cen_lat = jsondata['cen_lat']
        cen_lon = jsondata['cen_lon']
        radius = jsondata['radius']
        user_set = jsondata['user_set']
        area_count = NotificationArea.objects.filter(email=email).count()
        if (area_count == 1):
            area = NotificationArea.objects.get(email=email)
            area.cen_lat = cen_lat
            area.cen_lon = cen_lon
            area.radius = radius
            area.user_set = user_set
            area.save()
        else:
            area = NotificationArea.objects.create(
                email=email,
                cen_lat=cen_lat,
                cen_lon=cen_lon,
                radius=radius,
                user_set=user_set)
        new_area = NotificationArea.objects.filter(email=email)

        data = serializers.serialize('json', new_area)

        return HttpResponse(data, content_type='application/json')


#deprecated (updated - getNotificatArea)
def getArea(request, email=None, format=None):
    queryset = NotificationArea.objects.filter(email=email)
    data = serializers.serialize('json', queryset)
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def sendMail(request, post=None, format=None):
    rows = Image.objects.filter(post_id_id=post)[:1]
    post_details = Post.objects.get(id=post)
    title = post_details.title
    image_row = None
    image_file = ''
    for row in rows.iterator():
        image_row = getattr(row, 'image')
    if image_row is not None:
        image_file = 'https://citysavior.pythonanywhere.com' + image_row.url
        html_message = '<html>\n<body><h1 style="text-align:center;background-color:lightGrey;font-size:300%;"><i>City Savior</i></h1><h2> We have received you post :<i style="color:red;">' + title + '</i>.</h2><br><div style="text-align:center"><h2>' + title + '</h2><img src="' + image_file + '" alt="" height="500" width="500" style="border:5px solid red"/></div><div style="text-align:center"><br><a href="https://play.google.com/store/apps/details?id=com.citySavior&hl=en"><img src="https://citysavior.pythonanywhere.com/static/android-button.png" alt=""></a>  <a href="https://itunes.apple.com/us/app/city-savior/id1249164397"><img src="https://citysavior.pythonanywhere.com/static/apple-button.png" alt=""></a></div> \n</body>\n</html>'
    else:
        html_message = '<html><body><h1 style="text-align:center;background-color:lightGrey;font-size:300%;"><i>City Savior</i></h1><h2> We have received you post :<i style="color:red;">' + title + '</i>.</h2><br><div style="text-align:center"><br><a href="https://play.google.com/store/apps/details?id=com.citySavior&hl=en"><img src="https://citysavior.pythonanywhere.com/static/android-button.png" alt=""></a>  <a href="https://itunes.apple.com/us/app/city-savior/id1249164397"><img src="https://citysavior.pythonanywhere.com/static/apple-button.png" alt=""></a></div>\n</body>\n</html>'
    response = send_mail(
        'Test',
        'Test message',
        settings.EMAIL_HOST_USER, ['riddhi@rechargers.co.in'],
        fail_silently=False,
        html_message=html_message)
    res = {'response': response}
    return JsonResponse(res)


@csrf_exempt
def send_area_notification(request, format=None):

    if request.method == 'POST':
        jsondata = json.loads(request.body)
        post_id = jsondata['post_id']
        lat = jsondata['lat']
        lon = jsondata['lon']
        email = jsondata['email']
        title = jsondata['title']
        message = jsondata['message']
        not_id = jsondata['not_id']

        post = Post.objects.get(id=post_id)
        images = Image.objects.filter(post_id_id=post_id)[:1]
        image_row = None

        for image in images.iterator():
            image_row = getattr(image, 'image')
        if (image_row != None):
            image_file = 'https://citysavior.pythonanywhere.com' + image_row.url
            html_message = '<html><body><h1 style="text-align:center;background-color:lightGrey;font-size:300%;"><i>City Savior</i></h1><h3 style="text-align:center">' + message + '</h3><br><div style="text-align:center"><h2><i>' + post.title + '</i></h2><img src="' + image_file + '" alt="" height="500" width="500" style="border:5px solid red"/></div><div style="text-align:center"><br><a href="https://play.google.com/store/apps/details?id=com.citySavior&hl=en"><img src="https://citysavior.pythonanywhere.com/static/android-button.png" alt=""></a>  <a href="https://itunes.apple.com/us/app/city-savior/id1249164397"><img src="https://citysavior.pythonanywhere.com/static/apple-button.png" alt=""></a></div></body></html>'
        else:
            html_message = '<html><body><h1 style="text-align:center;background-color:lightGrey;font-size:300%;"><i>City Savior</i></h1><h3 style="text-align:center">' + message + '</h3><br><div style="text-align:center"><br><a href="https://play.google.com/store/apps/details?id=com.citySavior&hl=en"><img src="https://citysavior.pythonanywhere.com/static/android-button.png" alt=""></a>  <a href="https://itunes.apple.com/us/app/city-savior/id1249164397"><img src="https://citysavior.pythonanywhere.com/static/apple-button.png" alt=""></a></div></body></html>'
        send_users = []
        users = NotificationArea.objects.exclude(email=email)
        for user in users:
            dist = geo.haversine_distance(lat, lon, user.cen_lat, user.cen_lon)
            dist = dist / 1000
            if (dist <= user.radius):
                send_users.append(user.email)
                send_mail(
                    title,
                    message,
                    'City Savior', [user.email],
                    fail_silently=True,
                    html_message=html_message)
        fcm_device = GCMDevice.objects.filter(name__in=send_users)
        response = fcm_device.send_message(
            title,
            extra={
                "priority": 2,
                "post": post_id,
                "visibility": 1,
                'icon': 'notif',
                'sound': 'default',
                'notId': not_id
            },
            use_fcm_notifications=False)

        #notification code for ios devices
        #apns_token = "22cfcc654ee2998fe911b71c2908a64295397875fa4308ce8ef616736a2616e0"
        #apns_device = APNSDevice.objects.get(registration_id=apns_token)
        apns_device = APNSDevice.objects.filter(name__in=send_users)
        response = apns_device.send_message(
            title,
            extra={
                "priority": 2,
                "post": post_id,
                "visibility": 1,
                'icon': 'notif',
                'sound': 'default'
            })

        res = {'response': response}
        return JsonResponse(res)


@csrf_exempt
def send_user_notification(request, format=None):

    if request.method == 'POST':
        jsondata = json.loads(request.body)
        post_id = jsondata['post_id']
        email = jsondata['email']
        title = jsondata['title']
        message = jsondata['message']
        not_id = jsondata['not_id']
        send_not = jsondata['send_not']

        post = Post.objects.get(id=post_id)
        images = Image.objects.filter(post_id_id=post_id)[:1]
        image_row = None

        for image in images.iterator():
            image_row = getattr(image, 'image')

        if (image_row != None):
            image_file = 'https://citysavior.pythonanywhere.com' + image_row.url
            html_message = '<html><body><h1 style="text-align:center;background-color:lightGrey;font-size:300%;"><i>City Savior</i></h1><h3 style="text-align:center">' + message + '</h3><br><div style="text-align:center"><h2><i>' + post.title + '</i></h2><img src="' + image_file + '" alt="" height="500" width="500" style="border:5px solid red"/></div><div style="text-align:center"><br><a href="https://play.google.com/store/apps/details?id=com.citySavior&hl=en"><img src="https://citysavior.pythonanywhere.com/static/android-button.png" alt=""></a>  <a href="https://itunes.apple.com/us/app/city-savior/id1249164397"><img src="https://citysavior.pythonanywhere.com/static/apple-button.png" alt=""></a></div></body></html>'
        else:
            html_message = '<html><body><h1 style="text-align:center;background-color:lightGrey;font-size:300%;"><i>City Savior</i></h1><h3 style="text-align:center">' + message + '</h3><br><div style="text-align:center"><br><a href="https://play.google.com/store/apps/details?id=com.citySavior&hl=en"><img src="https://citysavior.pythonanywhere.com/static/android-button.png" alt=""></a>  <a href="https://itunes.apple.com/us/app/city-savior/id1249164397"><img src="https://citysavior.pythonanywhere.com/static/apple-button.png" alt=""></a></div></body></html>'

        email_response = send_mail(
            title,
            message,
            'City Savior', [email],
            fail_silently=True,
            html_message=html_message)
        # send notification to authorities
        authorities = Member.objects.filter(role__iexact='authority')
        notif_authority = []
        for authority in authorities:
            notif_authority.append(authority.email)
        fcm_device = GCMDevice.objects.filter(name__in=notif_authority)
        fcm_device.send_message(
            title,
            extra={
                "priority": 2,
                "post": post_id,
                "visibility": 1,
                'icon': 'notif',
                'sound': 'default',
                'notId': not_id
            },
            use_fcm_notifications=False)
        apns_device = APNSDevice.objects.filter(name__in=notif_authority)
        apns_device.send_message(
            title,
            extra={
                "priority": 2,
                "post": post_id,
                "visibility": 1,
                'icon': 'notif',
                'sound': 'default'
            })

        if (send_not == True):
            fcm_device = GCMDevice.objects.filter(name=email)
            pn_response = fcm_device.send_message(
                title,
                extra={
                    "priority": 2,
                    "post": post_id,
                    "visibility": 1,
                    'icon': 'notif',
                    'sound': 'default',
                    'notId': not_id
                },
                use_fcm_notifications=False)

            #notification code for ios devices
            #apns_token = "22cfcc654ee2998fe911b71c2908a64295397875fa4308ce8ef616736a2616e0"
            #apns_device = APNSDevice.objects.get(registration_id=apns_token)
            apns_device = APNSDevice.objects.filter(name=email)
            pn_response = apns_device.send_message(
                title,
                extra={
                    "priority": 2,
                    "post": post_id,
                    "visibility": 1,
                    'icon': 'notif',
                    'sound': 'default'
                })
        else:
            pn_response = 1

        res = {'email_response': email_response, 'pn_response': pn_response}
        return JsonResponse(res)


# new and updated views


# updated createArea (updated to class-based view)
class NotificationAreaList(APIView):
    def get(self, request, format=None):
        area = NotificationArea.objects.all().order_by('-notification_id')
        serializer = NotificationAreaSerializer(area, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = NotificationAreaSerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# update updateArea(updated to class based view)
class NotificationAreaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NotificationArea.objects.all()
    serializer_class = NotificationAreaSerializer


# updated getArea(updated Response type)
def getNotificationArea(request, email=None, format=None):
    queryset = NotificationArea.objects.filter(email=email)
    serializer = NotificationAreaSerializer(queryset, many=True)
    return JsonResponse(serializer.data)
