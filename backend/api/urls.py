
from django.urls import path

from backend.api.views import  UserLoginView, UserRegistrationView, Profle, CreateCheckoutSessionAPIView,\
     UpdatePaymentMethodAPIView,  Plan, Avatar, VideoView, GetVideo, SaveVideo, Ai

urlpatterns = [
    path('signup', UserRegistrationView.as_view()),
    path('login', UserLoginView.as_view()),
    path('create', VideoView.as_view()),
    path('create-video', SaveVideo.as_view()),
    path('myvideos', VideoView.as_view()),
    path('delete-video/<id>', GetVideo.as_view()),
    path('get-profile', Profle.as_view()),
    path('ai-prompt', Ai.as_view()),
    path('get-plan', Plan.as_view()),
    path('cancel-plan', Plan.as_view()),
    path('update_profile', Profle.as_view()),
    path('create-checkout-session', CreateCheckoutSessionAPIView.as_view()),
    path('update-payment-method', UpdatePaymentMethodAPIView.as_view()),
    path('upload', Avatar.as_view()),
    path('delete-avatar/<uuid:id>', Avatar.as_view()),

]