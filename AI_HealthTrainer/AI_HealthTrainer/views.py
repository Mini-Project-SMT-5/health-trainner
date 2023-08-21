from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import StreamingHttpResponse, JsonResponse

from AI_HealthTrainer import health_trainer
from .goal import set_goal
from .mypage import mypage
from .completion import completion


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
    print("run completion")
    sets_value = request.GET.get('sets_value')  # URL 파라미터 'set_value' 값 가져오기
    reps_value = request.GET.get('reps_value')  # URL 파라미터 'reps_value' 값 가져오기

    print("completion run")
    print("sets", sets_value)
    print("reps", reps_value)
    
    #디비 저장
    return render(request, "Structures/completion.html")


def index(request):
    return render(request, 'index.html')