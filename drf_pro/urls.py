from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Docs UI
    path('api/v1/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('api/v1/user/', include('apps.authentication.urls'))
]
