from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apps/finance-tracker/api/v1/authentication/', include('authentication.api.urls')),
]