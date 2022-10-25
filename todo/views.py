from unittest import TestSuite
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Todo
from .forms import TodoForm
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
def completed_by_id(request, id):
    todo = Todo.objects.get(id=id)
    todo.completed = not todo.completed
    todo.date_completed = datetime.now() if todo.completed else None
    todo.save()

    return redirect('todo')


@login_required
def delete(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()
    return redirect('todo')


@login_required
def completed(request):
    # 篩選已完成項目
    todos = Todo.objects.filter(user=request.user,
                                completed=True)
    return render(request, './todo/completed.html',
                  {'todos': todos})


@login_required
def createtodo(request):
    message = ''
    form = TodoForm()
    try:
        if request.method == 'POST':
            print(request.POST)
            if request.user.is_authenticated:
                form = TodoForm(request.POST)
                todo = form.save(commit=False)
                todo.user = request.user
                todo.date_completed = datetime.now() if todo.completed else None
                todo.save()

                return redirect('todo')
    except Exception as e:
        print(e)
        message = '資料輸入錯誤!'

    return render(request, './todo/createtodo.html', {'form': form, 'message': message})

# Create your views here.


def todo(request):
    todos = None
    # 確定有使用者登入
    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user)

    return render(request, './todo/todo.html', {'todos': todos})


@login_required
def viewtodo(request, id):
    try:
        todo = Todo.objects.get(id=id)
        if request.method == 'GET':
            form = TodoForm(instance=todo)

        elif request.method == 'POST':
            print(request.POST)
            # 更新
            if request.POST.get('update'):
                # 將POST回傳值填入todo，產生Form表單
                form = TodoForm(request.POST, instance=todo)
                if form.is_valid():
                    # 資料暫存
                    todo = form.save(commit=False)
                    # 更新完成日期
                    todo.date_completed = datetime.now() if todo.completed else None
                    # 更新資料
                    form.save()
            # 刪除之後馬上回首頁
            elif request.POST.get('delete'):
                todo.delete()
                return redirect('todo')

        return render(request, './todo/viewtodo.html', {'todo': todo, 'form': form})
    except Exception as e:
        print(e)

    return render(request, './todo/404.html')
