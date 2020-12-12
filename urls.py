from django.urls import include
import config

urlpatterns = [
    include(config.SUBDIRECTORY, include('core.urls'))
]