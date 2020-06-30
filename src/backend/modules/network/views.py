from django.shortcuts import render


def network_index(request):
    return render(request, 'network/index.html')
