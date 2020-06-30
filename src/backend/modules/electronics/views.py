from django.shortcuts import render


def elec_index(request):
    return render(request, 'electronics/index.html')
