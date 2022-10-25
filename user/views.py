from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserForm


@login_required
def user_logout(requset):
    logout(requset)
    return redirect('todo')


@login_required
def profile(request):
    return render(request, './user/profile.html')


def user_login(request):
    message, username = '', ''
    # 是否是POST表單
    if request.method == 'POST':
        if request.POST.get('login'):
            username = request.POST.get('username')
            password = request.POST.get('password')

            print(username, password)
            # 1.檢查帳號密碼是否為空
            if username == '' or password == '':
                message = '帳號跟密碼不能為空!'
            else:
                # 2.是否有該使用者
                # 3.匹配密碼進行登入
                user = authenticate(
                    request, username=username, password=password)
                if user is None:
                    if User.objects.filter(username=username):
                        message = '密碼有誤!'
                    else:
                        message = '帳號有誤!'
                else:
                    # 進行登入
                    login(request, user)
                    message = '登入中...'
                    return redirect('todo')

        elif request.POST.get('register'):
            return redirect('register')

    return render(request, './user/login.html', {'message': message, 'username': username})


# Create your views here.
def user_register(request):
    # 產生使用者表單
    form = MyUserForm()
    message = ''
    # 檢查是get or post
    if request.method == 'GET':
        print('GET')
    elif request.method == 'POST':
        print('POST')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        # 註冊功能
        # 密碼不能少於8各字元
        # 兩次密碼是否相同
        # 使用者名稱不能重複
        # 進行註冊
        if len(password1) < 8:
            message = '密碼少於8各字元'
        elif password1 != password2:
            message = '兩次密碼不同'
        else:
            if User.objects.filter(username=username).exists():
                message = '帳號重複'
            else:
                user = User.objects.create_user(username=username, password=password1,
                                                email=email)
                user.save()
                message = '註冊成功!'
                login(request, user)

                return redirect('profile')

    return render(request, './user/register.html', {'form': form, 'message': message})
