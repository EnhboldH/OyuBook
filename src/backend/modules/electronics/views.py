from django.shortcuts import render
from django.views import View

class ElectronicsView(View):
    context = {
        'title': 'Электроник | OyuBook',
    }
    def get(self, request, *args, **kwargs):
      return render(request, 'electronics/index.html', self.context)
