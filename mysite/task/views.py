from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForms
from .models import Task 
from django.utils import timezone


#Retorna o templete do menu.html
def home(request):
    return render(request, "home.html")  

def sigup(request):
    
    if request.method == "GET":

        return render(request, 'sigup.html', {
            'form' : UserCreationForm
        })
    
    else:

        if request.POST['password1'] == request.POST['password2']:

            try:

                user = User.objects.create_user(username=request.POST['emailuser'], password = request.POST['password1'])
                user.save()

                login(request, user)
                return redirect('tasks')
            
            except:

                return render (request,'sigup.html', {
                'form' : UserCreationForm,       
                "error": 'Usuario já existe!!'})
            
        return  render (request, 'sigup.html', 
                        {
                            'form' : UserCreationForm,
                            'error': 'Senhas diferentes!!'
                        })
    
def sigin(request):

    if request.method == 'GET':
        return render(request, "sigin.html", {
        'form': AuthenticationForm
        })  

    else:

        user = authenticate(

            request, username=request.POST['emailuser'], password=request.POST['password'])

        if user is None:
            return render(request, 'sigin.html',{
            'form': AuthenticationForm,
            'error': "Usuario ou senha incorreto"
            })

        else:
            login(request, user)
            return redirect('tasks')

@login_required          
def sair(request):
    logout(request)
    return redirect('home')

@login_required        
def tasks(request):
    return render(request, "tasks.html")  

@login_required   
def criar_tarefa(request):

    if request.method == "GET":
        return render(request, 'criar_tarefa.html', {
            'form' : TaskForms
        })
    
    else:

        try: 
            form = TaskForms(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        
        except ValueError:

            return render(request, 'criar_tarefa.html',{
                'form': TaskForms,
                'error': 'Insira dados validos'
            })
        

@login_required  
def tasks(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, "tasks.html", {'tasks':tasks})

@login_required  
def task_detalhe(request,task_id):

    if request.method == 'GET':
        tasks = get_object_or_404(Task,pk=task_id, user=request.user)
        form = TaskForms(instance=tasks)
        return render(request, 'task_detalhe.html', {'task' : tasks, 'form' : form})
    
    else:

        try:
            tasks = get_object_or_404(Task,pk=task_id, user=request.user)
            form = TaskForms(request.POST, instance=tasks)
            form.save()
            return redirect('tasks')
        
        except ValueError:

            return render(request, 'task_detalhe',{ 
                'tasks' : tasks, 
                'form' : form,
                'error': 'Erro ao atualizar uma tarefa.',
            })

@login_required  
def complete_tarefa(request, task_id):
    task = get_object_or_404(Task,pk=task_id, user=request.user)

    if request.method =="POST":
        task.date_completed = timezone.now()

        task.save()
        return redirect('tasks')
    
@login_required
def deletar_tarefa(request, task_id):
    tasks = get_object_or_404(Task,pk=task_id, user=request.user)

    if request.method == 'POST':
        tasks.delete()
        return redirect('tasks') 

@login_required
def exibir_tarefas_completadas(request):
    tasks = Task.objects.filter(user=request.user, date_completed__isnull=False)
    return render(request, 'tasks.html', {'tasks': tasks})
