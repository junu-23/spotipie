from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from common.forms import UserForm


def logout_view(request):
    logout(request)
    return redirect('index')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # form.cleaned_data.get 함수는 폼의 입력값을 개별적으로 얻고 싶은 경우에 사용하는 함수
            user = authenticate(username=username, password = raw_password)
            login(request, user) # 로그인
            return redirect('index')

    else:
        form = UserForm()

        return render(request,'common/signup.html',{'form': form})