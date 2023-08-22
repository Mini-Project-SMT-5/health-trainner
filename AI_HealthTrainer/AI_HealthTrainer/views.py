from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from AI_HealthTrainer.models import Goal, Exercise

from AI_HealthTrainer import health_trainer
from datetime import datetime, timedelta

global start_time, end_time, exercise_name

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
    # set = 2
    # reps = 4
    # rest = 10
    if request.method == 'POST':
        set = request.POST['sets']
        reps = request.POST['reps']
        rest = request.POST['rest']
    return render(request, "Structures/camera.html", {'sets_value': set, 'reps_value': reps, 'rest_value': rest})


def set_time(request):
    global exercise_name
    exercise_name = request.GET.get('exercise_name')
    return render(request, "Structures/time.html")

def completion(request):
    return render(request, "Structures/completion.html")
    return render(request, "Structures/camera.html")


def homepage(request):
    return render(request, "Structures/homepage.html")

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']  # Menggunakan username field sebagai email
        password = request.POST['password']
        print(username)
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # print("login Berhasil")
            return redirect('home')  # Ganti 'home' dengan nama URL yang sesuai
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

def home(request):
    user = request.user
    goals = Goal.objects.all()
    return render(request, "Structures/mypage.html", {'user': user,'goals':goals})

def user_goal(request):
    if request.method == 'POST':
        user = request.user.id
        start_date = request.POST['start-date']  # Menggunakan username field sebagai email
        end_date = request.POST['end-date']
        minutes = request.POST['minutes']
        hours = int(request.POST['hours'])  # Mengambil input dari POST dan mengonversi menjadi integer
        # id = user.id
        count_duration = hours * 60
        goal = Goal(start=start_date, stop=end_date, goal= count_duration, user_id = user, hour = hours, minute= minutes)
        goal.save()
        return redirect('exercise')
    return render(request, "Structures/goal.html")

def exercise(request):
    return render(request, "Structures/exercise.html")

def user_dashboard(request):
    user = request.user
    goals = Goal.objects.all()
    return render(request, "Structures/dashboard.html", {'user': user, 'goals':goals})


def admin_exercise(request):
    exercises = Exercise.objects.all()
    return render(request, "Structures/exercise_admin.html", {'exercises': exercises} )

# def index(request):
#     return render(request, 'index.html')