from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls', namespace='core')),
    path('auth/', include('auth0a.urls', namespace='auth0a')),
    path('authm/', include('auth0m.urls', namespace='auth0m')),
    path('authenticate/', include('authenticate.urls', namespace='authenticate')),
    path('admin/', admin.site.urls),
]
