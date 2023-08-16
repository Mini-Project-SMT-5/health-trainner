from django.shortcuts import render
from django.http import StreamingHttpResponse

from AI_HealthTrainer import health_trainer

def video_feed(request):
    return StreamingHttpResponse(health_trainer.generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    
    return render(request, 'index.html')