from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Video

class VideoListView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        video_data = [{'title': video.title, 'video_url': video.video_file.url} for video in videos]
        return Response(video_data)
