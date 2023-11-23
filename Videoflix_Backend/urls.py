from django.contrib import admin
from django.urls import path, include
from authentication import views
from django.conf import settings
from django.conf.urls.static import static
from content.views import VideoListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('api/videos/', VideoListView.as_view(), name='video-list'),
    path('confirm/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm-email'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
