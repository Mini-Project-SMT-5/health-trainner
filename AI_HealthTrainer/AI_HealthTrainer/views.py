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
    set_value = request.GET.get('sets')
    reps_value = request.GET.get('reps')
    rest_value = request.GET.get('rest')
    return StreamingHttpResponse(health_trainer.generate_frames(set_value, reps_value, rest_value), content_type='multipart/x-mixed-replace; boundary=frame')


@csrf_protect
def camera(request):
    set = 2
    reps = 2
    rest = 2
    # set = request.POST['sets']
    # reps = request.POST['reps']
    # rest = request.POST['rest']
    print("run camera")
    print("set", set)
    print("reps", reps)
    print("rest", rest)
        
    return render(request, "Structures/camera.html", {'sets_value': set, 'reps_value': reps, 'rest_value': rest})


def time(request):
    return render(request, "Structures/time.html")

def completion(request):
    data = request.json()  # 전송된 JSON 데이터를 파싱

    print(data)

    #디비 저장
    return render(request, "Structures/completion.html")


def index(request):
    return render(request, 'index.html')