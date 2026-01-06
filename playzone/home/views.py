from django.shortcuts import render

from django.views import View

# Create your views here.


class HomeView (View) :

    template = 'home.html'

    def get (self,request,*args,**kwargs) :

        data = {'page':'Home'}

        return render(request,self.template,context=data)
    