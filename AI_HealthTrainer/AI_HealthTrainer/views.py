from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse

from AI_HealthTrainer import health_trainer


def get_feedback(request):
    feedback_text = health_trainer.send_feedback()
    data = {'textData': feedback_text}
    print(data)
    return JsonResponse(data)

def video_feed(request):
    #return StreamingHttpResponse(health_trainer.generate_frames(), content_type='application/json')
    return StreamingHttpResponse(health_trainer.generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def camera(request):
    return render(request, "Structures/camera.html")

def index(request):
    return render(request, 'index.html')
