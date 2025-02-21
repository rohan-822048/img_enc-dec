from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_image, name='upload_image'),
    path('encrypt/', views.encrypt_image, name='encrypt_image'),
    path('decrypt/', views.decrypt_image, name='decrypt_image'),
    path('download/<str:filename>/', views.download_image, name='download_image'),
]
