
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/request/', include('request.urls')),
    path('api/alert/', include('alert.urls')),
    path('api/donation/', include('donation.urls')),
    path('api/users/', include('users.urls'))
]
