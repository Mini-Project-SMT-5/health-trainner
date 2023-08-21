from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, HttpResponse
from django.contrib.auth.models import User
from .models import UserFitnessData
from django.contrib.auth.decorators import login_required

#@login_required
def mypage(request):
    user = request.user

    try:
        user_fitness_data = UserFitnessData.objects.get(user=user) #현재 로그인한 사용자 정보 가져옴
        goal = user_fitness_data.goal
        exercise_time = user_fitness_data.exercise_time
        used_calories = user_fitness_data.used_calories

        if exercise_time != 0 and goal is not None: #값 제대로 받아왔을 때
            user_fitness_data.accomplishment_rate = (exercise_time / goal) * 100
            user_fitness_data.save()  # Save the updated instance

        if goal is not None and goal > 0:
            if exercise_time > goal:
                exercise_time = goal #운동시간이 목표 초과하지 않도록 조정(최대 100%달성률)

    except UserFitnessData.DoesNotExist:
        goal = None
        exercise_time = 0
        used_calories = 0
        user_fitness_data.accomplishment_rate = (exercise_time / goal) * 100
        user_fitness_data.save()

    context = {
        'username' : user.username,
        'goal' : goal,
        'exercise_time' : exercise_time,
        'used_calories' : used_calories,
        'accomplishment_rate' : user_fitness_data.accomplishment_rate,
    }

    return render(request, 'Structures/mypage.html', context)