from django.shortcuts import render


def math_index(request):
    return render(request, 'mathematics/index.html')
