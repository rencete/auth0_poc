from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('auth/', include('auth0.urls', namespace='auth0')),
    path('authenticate/', include('authenticate.urls', namespace='authenticate')),
    path('admin/', admin.site.urls),
]
