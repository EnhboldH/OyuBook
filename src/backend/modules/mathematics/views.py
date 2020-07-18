from django.shortcuts import render
from django.views import View

class MathematicsView(View):
    context = {
        'title': 'Математик | OyuBook',
    }
    def get(self, request, *args, **kwargs):
      return render(request, 'mathematics/index.html', self.context)
