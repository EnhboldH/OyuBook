from django.shortcuts import render
from django.views import View

class NetworkView(View):
    context = {
        'title': 'Компьютерийн сүлжээ | OyuBook',
    }
    def get(self, request, *args, **kwargs):
      return render(request, 'network/index.html', self.context)
