from django.shortcuts import render, redirect
from .models import UserFitnessData

def completion(request):
    if request.method == 'POST':
        user = request.user

        # Assume you have received values from the form
        used_calories = int(request.POST.get('used_calories', 0))
        total_exercise_time = int(request.POST.get('total_exercise_time', 0))
        total_repetition = int(request.POST.get('total_repetition', 0))

        user_fitness_data, created = UserFitnessData.objects.get_or_create(user=user)

        # used_calories = 50
        # total_exercise_time = 40
        # total_repetition = 30

        # Update the values
        user_fitness_data.used_calories += used_calories
        user_fitness_data.exercise_time += total_exercise_time
        # user_fitness_data.total_repetition += total_repetition //rep은 mypage에 없으니까
        user_fitness_data.save() #db 저장까지

        context = {
            'used_calories': used_calories,
            'total_exercise_time': total_exercise_time,
            'total_repetition': total_repetition,
        }
        return render(request, 'Structures/completion.html', context)

    return render(request, 'Structures/completion.html')
