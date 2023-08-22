from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import StreamingHttpResponse, JsonResponse
from datetime import datetime

from AI_HealthTrainer import health_trainer
from datetime import datetime
from .models import Workout, Goal, Exercise
from django.db.models import Sum
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from AI_HealthTrainer.models import Goal, Exercise


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
    return StreamingHttpResponse(health_trainer.generate_frames(set_value, reps_value, rest_value, exercise_name), content_type='multipart/x-mixed-replace; boundary=frame')


@csrf_protect
def camera(request):    
    global start_time, exercise_name
    
    sets = request.POST['sets']
    reps = request.POST['reps']
    rest = request.POST['rest']

    start_time = datetime.now()

    return render(request, "Structures/camera.html", {'sets_value': sets, 'reps_value': reps, 'rest_value': rest, 'exercise_name': exercise_name})


def set_time(request):
    global exercise_name
    exercise_name = request.GET.get('exercise_name')
    return render(request, "Structures/time.html")

def completion(request):
    global end_time, exercise_name
    calories = 0
    
    end_time = datetime.now()

    sets_value = int(request.GET.get('sets_value'))
    reps_value = int(request.GET.get('reps_value'))

    if exercise_name == "Dumbbell Curl":
        calories = 1 * reps_value * sets_value
    elif exercise_name == "Lunge":
        calories = 3 * reps_value * sets_value
    elif exercise_name == "Jumping Jack":
        calories = 5 * reps_value * sets_value

    time_interval = end_time - start_time
    workoutTime = round(int(time_interval.total_seconds()) / 60, 2)
    count = sets_value * reps_value
        
    user = request.user
    exercise = Exercise.objects.get(name=exercise_name)
    
    workout_data = {
        'count': sets_value,
        'start_time': start_time,
        'end_time': end_time,
        'reps': reps_value,
        'user_id': user.id,
        'Exercise_idExercise': exercise,
        'calories': calories,
        'workout_time': workoutTime 
    }

    workout = Workout(**workout_data)
    workout.save()
    
    return render(request, "Structures/completion.html", {'calories': calories, 'total_time': workoutTime, 'count': count})


def homepage(request):
    return render(request, "Structures/homepage.html")


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']  # Menggunakan username field sebagai email
        password = request.POST['password']
        print(username)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            have_goal = Goal.objects.filter(user_id=user.id)

            if have_goal.exists():
                login(request, user)
                # print("login Berhasil")
                return redirect('mypage')  # Ganti 'home' dengan nama URL yang sesuai
            else:
                return redirect('goal')
        else:
            error_message = "Invalid email or password."
            return render(request, 'Structures/login.html', {'error_message': error_message})

    return render(request, 'Structures/login.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form)
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            print("Form is not valid", form.errors)
    else:
        form = SignUpForm()

    return render(request, 'Structures/signup.html', {'form': form})


def user_goal(request):
    if request.method == 'POST':
        user = request.user.id
        start_date = request.POST['start-date']  # Menggunakan username field sebagai email
        end_date = request.POST['end-date']
        minutes = int(request.POST['minutes'])
        hours = int(request.POST['hours'])  # Mengambil input dari POST dan mengonversi menjadi integer
        
        count_duration = hours * 60 + minutes
        goal = Goal(start=start_date, end=end_date, goal= count_duration, user_id = user)
        goal.save()
        return redirect('mypage')
    return render(request, "Structures/goal.html")

def exercise(request):
    return render(request, "Structures/exercise.html")


def mypage(request):
    user = request.user
    today = datetime.now()
    
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    
    # db 에서 데이터 가져오는 코드
    user_goal = Goal.objects.get(user_id = user.id)
    
    total_calories = Workout.objects.filter(user=user, start_time__range=(start_of_day, end_of_day)).aggregate(Sum('calories'))
    workout_time = Workout.objects.filter(user=user, start_time__range=(start_of_day, end_of_day)).aggregate(Sum('workout_time'))
    
    
    if workout_time['workout_time__sum'] is None:
        workout = 0
    else:
        workout = round(int(workout_time['workout_time__sum']))
    
    if total_calories['calories__sum'] is None:
        calories = 0
    else:
        calories = total_calories['calories__sum']
    
    goal_min = user_goal.goal
    
    accomplishment = round(round(workout) / goal_min * 100)

    return render(request, "Structures/mypage.html", {'calories': calories, 'workout': workout, 'goal': goal_min, 'user': user, "accomplishment": accomplishment})