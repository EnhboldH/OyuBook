from django.shortcuts import render


def ctf_index(request):
    return render(request, 'ctf/index.html')
