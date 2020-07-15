from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login,authenticate
from django.core.exceptions import PermissionDenied
# Create your views here.
class Login(View):
    template_name='auth/login.html'
    
    def get(self,request,*args, **kwargs):
        return render(request,self.template_name)
    
    def post(self,request,*args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        print(user)
        if user:
            try:
                perms = user.groups.get(name__icontains='docente')
                login(request,user)
                return redirect(reverse_lazy('teacher-home'))
            except Exception:
                raise PermissionDenied('Los estudiantes no tienen permiso para acceder, pronto podras disfrutar de este sistema')
            
        return render(request,self.template_name,{'errors':{'message':'Los credenciales no son correctos'}})