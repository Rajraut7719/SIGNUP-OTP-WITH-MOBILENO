from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('user',views.UserViewSet,basename='user')

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth/',include("rest_framework.urls"))
]
