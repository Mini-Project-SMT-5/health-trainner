from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import StreamingHttpResponse, JsonResponse
from datetime import datetime

from AI_HealthTrainer import health_trainer
from .goal import set_goal
from .mypage import mypage
from .completion import completion
from .models import Workout, UserFitnessData, Exercise

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

# def completion(request):
#     # print("run completion")
#     # sets_value = request.GET.get('sets_value')  # URL 파라미터 'set_value' 값 가져오기
#     # reps_value = request.GET.get('reps_value')  # URL 파라미터 'reps_value' 값 가져오기
    
#     count = 3
#     reps = 5
#     used_calories = 1000

#     start_time = datetime(2023, 8, 18, 13, 27, 40)
#     end_time = datetime(2023, 8, 18, 13, 47, 40)

#     # start_time = "15:10:15"
#     # end_time = "15:12:20"
#     total_exercise_time = end_time - start_time
#     # exercise_id = 1  # 예시로 Exercise 모델의 기본 키 값을 넣어주세요
#     # exercise_record = Exercise.objects.get(pk=exercise_id)

#     print("completion run")

#     #디비 저장 하는 코드 여기 넣기
#     user = request.user
#     exercise_record = Exercise.objects.get(pk=exercise_id)

#     workout, created = Workout.objects.get_or_create(user=user)
#     workout.count = count
#     workout.reps = reps
#     workout.calories = used_calories
#     workout.start_time = start_time
#     workout.end_time = end_time
#     workout.exercise = exercise_record
#     workout.save()

#     context = {
#             'used_calories': used_calories,
#             'total_exercise_time': total_exercise_time,
#             'total_repetition': reps,
#     }
#     return render(request, 'Structures/completion.html', context)

#     # Update the values for MYPAGE
#     user_fitness_data, created = UserFitnessData.objects.get_or_create(user=user)
#     user_fitness_data.used_calories += used_calories
#     user_fitness_data.exercise_time += total_exercise_time
#     # user_fitness_data.total_repetition += total_repetition //rep은 mypage에 없으니까
#     user_fitness_data.save() #db 저장까지


#     return render(request, "Structures/completion.html")


def index(request):
    return render(request, 'index.html')