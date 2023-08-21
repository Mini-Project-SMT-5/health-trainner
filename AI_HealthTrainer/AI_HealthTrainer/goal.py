from django.shortcuts import render,redirect
# from AI_HealthTrainer.models import goal
from django.http import StreamingHttpResponse,JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import goal
from .models import UserFitnessData

# @login_required
def set_goal(request):
    if request.method == 'POST':
        if request.user.is_authenticated: #SimpleLazyObject 오류: 사용자(User) 객체를 예상하는 필드에 올바르지 않은 값을 할당하려고 시도
            user = request.user

            start_date = request.POST.get('start-date')
            end_date = request.POST.get('end-date')
            goal_hour = int(request.POST.get('hours', 0))
            goal_minute = int(request.POST.get('minutes', 0))
            total_goal_minutes = goal_hour * 60 + goal_minute
            
            # print("start_date:", start_date)
            # print("end_date:", end_date)
            # print("hour:", str(goal_hour))
            # print("goal_min:", str(goal_minute))
            

            # user = request.user
            user = User.objects.get(username=request.user.username)
            new_goal = goal(user=user, start=start_date, stop=end_date, hour = goal_hour, minute = goal_minute, total = total_goal_minutes)
            new_goal.save()

            user_fitness_data, created = UserFitnessData.objects.get_or_create(user=user)
            user_fitness_data.goal = total_goal_minutes
            user_fitness_data.save()

            return redirect('mypage')
        else:
            return HttpResponse("You need to be logged in.")

    return render(request, 'Structures/goal.html')