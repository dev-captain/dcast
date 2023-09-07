from django.conf import settings
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from backend.api.serializers import UserLoginSerializer, UserRegistrationSerializer,\
    CreateCheckoutSessionSerializer, UpdatePaymentMethodSerializer, AvatarSerializer, VideoSerializer
from backend.api.models import Video, AvatarModel
import stripe
from django.db.models import Q
import requests
import os
import time


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        # print(data)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        tokens = serializer.data['tokens']
        response = {
            'token': tokens['access'],
            'refresh': tokens['refresh'],
            'userStatus': tokens['status'],
            'success': 'True',
            'status code': status_code,
            'type': 'User registered  successfully',
        }
        return Response(response, status=status_code)


class UserLoginView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'status code': status.HTTP_200_OK,
            'token': serializer.data['token'],
            'refresh': serializer.data['refresh'],
            'email': serializer.data['email'],
            'userStatus': serializer.data['status']
        }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)


class Profle(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        status_code = status.HTTP_200_OK
        return Response(str(user.email), status=status_code)

    def post(self, request):
        user = request.user
        user.birthday_year = request.data['year']
        user.birthday_month = request.data['month']
        user.birthday_day = request.data['day']
        user.gender = request.data['gender']
        user.wedding = request.data['wedding']
        user.hobby = request.data['hobby']
        user.child = request.data['child']
        user.salary = request.data['salary']
        user.job = request.data['job']
        if user.status == 2:
            user.status = 2
        else:
            user.status = 1
        user.save()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'true',
            'status code': status_code
        }
        return Response(response, status=status_code)


class Ai(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        url = "https://api.d-id.com/create/dreams"
        payload = request.data
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            # "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jeF9sb2dpY19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfY3VzdG9tZXJfaWQiOiJjdXNfT1RHSE55NzliZVhySFMiLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiYXV0aDB8NjRkZWVhNjQ3Njk0ZWIwYzdjZjkzMTc4IiwiYXVkIjpbImh0dHBzOi8vZC1pZC51cy5hdXRoMC5jb20vYXBpL3YyLyIsImh0dHBzOi8vZC1pZC51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjkyOTcyNjQxLCJleHAiOjE2OTMwNTkwNDEsImF6cCI6Ikd6ck5JMU9yZTlGTTNFZURSZjNtM3ozVFN3MEpsUllxIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCByZWFkOmN1cnJlbnRfdXNlciB1cGRhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIG9mZmxpbmVfYWNjZXNzIn0.TIGPqDd5qx1-v-uWvone876WRfnBg2uOZZWq8rYdpJ2_UdhegG5YRQlzgzm99hFKvEfrLrQbHq-opvFD3VM6h2o0TUHygzl8kW584cb7XOe41P1H-Ac8x-yK35jHMjXbePjatNDmlRp3clGJa2-vrCjMOr-ZMa2eSf3kUokhPBTcboQaoTwC2T2frisf-cXzHwjXDXYXDTaxQfFS891NnUktgs5-FWpcaN1reX8PE0B4jRWLyfHRUsRaFRx5JlYp4KXuvYG7PZhCRZhE-AKaU55IrEtdw5Fq9jBlaNiYkPtcx3s4qbbperGmiM2xsdafrVp572Gw9ZaeEVTP3Rp65w"
            # "authorization": "Basic aW5mb21ldGFkYXRhbGFiQGdtYWlsLmNvbQ:jKj0IazD_FTdK5QExa2gC"
        }

        response = requests.post(url, json=payload, headers=headers)
        print(response.status_code)
        return Response({'data': response.json()}, status=status.HTTP_201_CREATED)


class VideoView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        url = "https://api.d-id.com/talks"
        payload = request.data
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Basic aW5mb21ldGFkYXRhbGFiQGdtYWlsLmNvbQ:jKj0IazD_FTdK5QExa2gC"
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if (response.status_code == 201):
                return Response(
                    {
                        'success': True,
                        'id': response.json()['id'],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response({
                    'success': False,
                },
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
            },
                status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        videos = Video.objects.filter(maker=request.user)[::-1]
        status_code = status.HTTP_200_OK

        return Response(data=VideoSerializer(videos, many=True).data, status=status_code)


def convert(seconds):
    seconds = float(seconds)
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


class SaveVideo(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        time.sleep(2)
        url = "https://api.d-id.com/create/libraryItems/" + request.data['id']

        headers = {
            "accept": "application/json",
            "authorization": "Basic aW5mb21ldGFkYXRhbGFiQGdtYWlsLmNvbQ:jKj0IazD_FTdK5QExa2gC"
        }

        get_video = requests.get(url, headers=headers)
        video_info = get_video.json()
        video = Video()
        video.videoId = video_info['id']
        video.title = video_info['name']
        video.duration = convert(video_info['duration'])
        video.maker = request.user
        video.save_thumbnail(video_info['thumbnail_url'])
        video.save_video(video_info['video_url'])
        video.save()
        return Response(
            {
                'success': True,
                'message': 'Success',
            },
            status=status.HTTP_201_CREATED,
        )


class GetVideo(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        video = Video.objects.filter(id=id).first()
        status_code = status.HTTP_200_OK
        response = {
            'success': 'true',
            'status code': status_code,
            'data': {
                'title': video.title,
                'url': video.url,
                'img': video.image
            }
        }
        return Response(response, status=status_code)

    def delete(self, request, id):
        video = Video.objects.filter(videoId=id).first()
        imgSrc = video.thumbnail.path
        videoSrc =video.video.path
        if os.path.exists(imgSrc):
            os.remove(imgSrc)
        if os.path.exists(videoSrc):
            os.remove(videoSrc)
       
        video.delete()
        status_code = status.HTTP_200_OK
        url = "https://api.d-id.com/talks/" + id

        headers = {
            "accept": "application/json",
            "authorization": "Basic aW5mb21ldGFkYXRhbGFiQGdtYWlsLmNvbQ:jKj0IazD_FTdK5QExa2gC"

        }

        response = requests.delete(url, headers=headers)

        return Response(status=status_code)


class Avatar(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if request.data['type'] == 'presenter':
            files = request.data['data']
            file_obj = AvatarModel(
                name=files.name, filename=files, maker=request.user, type="presenter")
            file_obj.save()
        if request.data['type'] == 'ai':
            print(123)
        return Response(
            {
                'url': file_obj.filename.url
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        presenter = AvatarModel.objects.filter(
            maker=request.user, type="presenter")[::-1]
        ai = AvatarModel.objects.filter(maker=request.user, type="ai")[::-1]
        response = {
            'presenter': AvatarSerializer(presenter, many=True).data,
            'ai': AvatarSerializer(ai, many=True).data
        }
        status_code = status.HTTP_201_CREATED
        return Response(response, status=status_code)

    def delete(self, request, id):
        avatar = AvatarModel.objects.filter(id=id).first()
        filename = avatar.filename.path
        avatar.delete()
        if os.path.exists(filename):
            os.remove(filename)
        status_code = status.HTTP_200_OK
        response = {
            'success': 'true',
            'status code': status_code,
        }
        return Response(response, status=status_code)


class CreateCheckoutSessionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCheckoutSessionSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = request.user.email
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email=email,
                line_items=request.data['price_info'],
                mode='subscription',
                locale='ja',
                success_url=settings.MAIN_DOMAIN + '/start',
                cancel_url=settings.MAIN_DOMAIN + '/plan',
            )

            return Response(
                {
                    'success': True,
                    'message': 'Success',
                    'result': session.id,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:

            return Response(
                {
                    'success': False,
                    'message': serializer.errors,
                    'result': [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdatePaymentMethodAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdatePaymentMethodSerializer

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            session = stripe.checkout.Session.retrieve(
                request.data['session_id'], expand=['setup_intent'])

            if session.setup_intent is not None:
                subscription = stripe.Subscription.modify(
                    session.setup_intent.metadata.subscription_id,
                    default_payment_method=session.setup_intent.payment_method
                )

                return Response(
                    {
                        'success': True,
                        'message': 'Success',
                        'result': [],
                    },
                    status=status.HTTP_200_OK)
            else:

                return Response(
                    {
                        'success': False,
                        'message': 'Can not find Stripe Checkout Session',
                        'result': [],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:

            return Response(
                {
                    'success': False,
                    'message': serializer.errors,
                    'result': [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class Plan(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_status = 0
        customer = stripe.Customer.list(
            email=user.email
        )
        if len(customer.data) > 0:
            user_status = 1
        return Response(
            {
                'success': True,
                'message': 'Success',
                'plan': user_status,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        user = request.user
        customer = stripe.Customer.list(
            email=user.email,
            expand=['data.subscriptions']
        )
        if len(customer.data) > 0:
            response = stripe.Subscription.delete(
                customer.data[0].subscriptions.data[0].id
            )
            response = stripe.Customer.delete(customer.data[0].id)

        return Response(
            {
                'success': True,
                'message': 'Success',
            },
            status=status.HTTP_200_OK,
        )
