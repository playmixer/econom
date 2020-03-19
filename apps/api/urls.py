from django.urls import path, include
from .views import CreatUserView

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', CreatUserView.as_view()),
    # path('auth/registration/', include('rest_auth.registration.urls')),
    path('econom/', include('apps.econom.urls')),
]
