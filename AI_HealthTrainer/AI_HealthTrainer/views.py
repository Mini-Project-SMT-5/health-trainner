from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import StreamingHttpResponse, JsonResponse

from AI_HealthTrainer import health_trainer
from datetime import datetime

global start_time, end_time, exercise_name

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
    global start_time
    
    set = request.POST['sets']
    reps = request.POST['reps']
    rest = request.POST['rest']

    start_time = datetime.now()

    return render(request, "Structures/camera.html", {'sets_value': set, 'reps_value': reps, 'rest_value': rest})


def set_time(request):
    global exercise_name
    exercise_name = request.GET.get('exercise_name')
    return render(request, "Structures/time.html")

def completion(request):
    global end_time, exercise_name
    
    end_time = datetime.now()

    sets_value = int(request.GET.get('sets_value'))
    reps_value = int(request.GET.get('reps_value'))

    if exercise_name == "dumbbellcurl":
        calories = round(0.15 * reps_value * sets_value, 2)
    elif exercise_name == "lunge":
        calories = round(0.3 * reps_value * sets_value, 2)
    elif exercise_name == "jumpingjack":
        calories = round(0.1 * reps_value * sets_value, 2)

    time_interval = end_time - start_time
    workoutTime = int(time_interval.total_seconds())    
    count = sets_value * reps_value
    
    print("start_time:", start_time.strftime('%H:%M:%S'))
    print("end_time:", end_time.strftime('%H:%M:%S'))   
        
    #디비 저장
    return render(request, "Structures/completion.html", {'calories': calories, 'total_time': workoutTime, 'count': count})


def exercise(request):
    return render(request, "Structures/exercise.html")


def mypage(request):
    
    today = datetime.now()
    print("today:", today.date())
    
    # db 에서 데이터 가져오는 코드
    
    return render(request, "Structures/mypage.html")


def index(request):
    return render(request, 'index.html')