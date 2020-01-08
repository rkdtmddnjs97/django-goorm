from django.shortcuts import render,redirect
from django.contrib import auth
from .models import Profile

# Create your views here

def signup(request):
    if request.method == 'POST':
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:   
            try:
                user = Profile.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username has already been taken'})
            except Profile.DoesNotExist:
                user = Profile.objects.create_user(
                    request.POST['username'], password=request.POST['password1'], sex=request.POST['sex'],start_year=request.POST['start_year'])
                auth.login(request, user)   #로그인 상태를 유지시켜주는 함수임
               

                return redirect('accounts:login')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'accounts/signup.html')
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:   #유저가 none 이 아니면은 로그인 조져라  그다음에 홈창으로 가주는거임
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')          #그냥 단순하게 로그아웃 상태가 해체된다


def mypage(request, profile_name):
    mypage_info = Profile.objects.get(username=profile_name)
    return render(request,'accounts/mypage.html',{'mypage_info':mypage_info})

def edit(request, profile_name):
    edit_mypage=Profile.objects.get(username=profile_name)
    return render(request, 'accounts/edit.html', {'profile':edit_mypage})    

def update(request, profile_name):
    update_mypage = Profile.objects.get (username = profile_name)
    update_mypage.sex = request.POST['sex']
    update_mypage.start_year = request.POST['start_year']
    update_mypage.save()
    return redirect('/accounts/mypage/' + str(profile_name))     
