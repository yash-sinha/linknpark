import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework import status, generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from posts.models import Member, Authority, MemberActivity, Support
from posts.serializers import MemberSerializer, AuthoritySerializer, MemberActivitySerializer, SupportSerializer
from posts.enums.device_enums import DeviceTypeEnums
from posts.app_settings import INTERNAL_EMAILS


class AuthorityList(APIView):
    def get(self, request, format=None):
        authority = Authority.objects.all().order_by('-email')
        serializer = AuthoritySerializer(authority, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = AuthoritySerializer(
            data=request.data, context={'user': user})
        serializer.is_valid(raise_exception=True)
        # only comes here if serializer is valid, else raises 400
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AuthorityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer


class MemberActivityList(APIView):
    def get(self, request, format=None):
        memberActivity = MemberActivity.objects.all().order_by('-activity_id')
        serializer = MemberActivitySerializer(memberActivity, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = MemberActivitySerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def checkOrCreateFCMDevice(request, email=None, reg_id=None, format=None):
    if request.method == 'POST':
        try:
            jsondata = json.loads(request.body)
            reg_id = jsondata['reg_id']
            email = jsondata['email']
            from_device = jsondata['device']
        except Exception as e:
            raise ValidationError('json error')

        if from_device == DeviceTypeEnums.android.name:
            device_present = GCMDevice.objects.filter(
                registration_id=reg_id).count()

            if device_present == 1:
                device = GCMDevice.objects.get(registration_id=reg_id)
                if device.name != email:
                    device.name = email
                    device.save()
                device = GCMDevice.objects.filter(registration_id=reg_id)
                data = serializers.serialize('json', device)
                return HttpResponse(data, content_type='application/json')
            else:
                fcm_device = GCMDevice.objects.create(
                    registration_id=reg_id,
                    name=email,
                    cloud_message_type="FCM")
                fcm_device = GCMDevice.objects.filter(registration_id=reg_id)
                data = serializers.serialize('json', list(fcm_device))
                return HttpResponse(data, content_type='application/json')

        elif from_device == DeviceTypeEnums.ios.name:
            device_present = APNSDevice.objects.filter(
                registration_id=reg_id).count()
            if device_present == 1:
                device = APNSDevice.objects.get(registration_id=reg_id)
                if device.name != email:
                    device.name = email
                    device.save()
                device = APNSDevice.objects.filter(registration_id=reg_id)
                data = serializers.serialize('json', device)
                return HttpResponse(data, content_type='application/json')
            else:
                apns_device = APNSDevice.objects.create(
                    registration_id=reg_id, name=email)
                apns_device = APNSDevice.objects.filter(registration_id=reg_id)
                data = serializers.serialize('json', list(apns_device))
                return HttpResponse(data, content_type='application/json')
    else:
        regs = APNSDevice.objects.all()
        data = serializers.serialize('json', list(regs))
        return HttpResponse(data, content_type='application/json')


class SupportList(APIView):
    def get(self, request, format=None):
        support = Support.objects.all().order_by('-support_id')
        serializer = SupportSerializer(support, many=True)
        return Response(serializer.data)

    @permission_classes((IsAdminUser, ))
    def post(self, request, format=None):
        user = request.user
        serializer = SupportSerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# new and updated views

# updated getLeaderBoard (updated - Response type)
def get_leaderboard(request, format=None):
    queryset = Member.objects.exclude(email__in=INTERNAL_EMAILS).order_by('-karma_points')[:20]
    serializer = MemberSerializer(queryset, many=True)
    return JsonResponse(serializer.data)


# updated getMyRank (updated to get request and Response type)
def get_user_rank(request, points=None, format=None):
    rank = Member.objects.exclude(email__in=INTERNAL_EMAILS).filter(karma_points__gt=points).count()
    rec = {'rank': rank}
    return JsonResponse(rec)
