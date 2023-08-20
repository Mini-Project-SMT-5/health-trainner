from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
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

# @csrf_protect
# def submit_form_view(request):
#     if request.method == 'POST':
#         form = YourForm(request.POST)
#         if form.is_valid():
#             # 폼이 유효한 경우 처리
#             # ...
#     else:
#         form = YourForm()


def camera(request):
    return render(request, "Structures/camera.html")

def time(request):
    return render(request, "Structures/time.html")

def index(request):
    return render(request, 'index.html')