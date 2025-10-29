from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Job, Application, SeekerProfile

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists.')
            return redirect('signup')
        
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request,'Account created successfully! You can now login.')
        return redirect('home')
    
    return render(request, 'signup.html')

@login_required
def logout_view(request):
    logout(request)
    # Clear old success/error messages
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # this clears messages

    return redirect('home')

def main(request):
    return render(request,'mainpage.html')

def main2(request):
    return render(request,'mainpage2.html')

@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_date')
    return render(request, 'jobs.html', {'jobs': jobs})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    already_applied = Application.objects.filter(seeker=request.user, job=job).exists()
    if not already_applied:
        Application.objects.create(seeker=request.user, job=job)
        messages.success(request, f"you have successfully applied for {job.title}")
    else:
        messages.warning(request, f"you already applied for {job.title}")
    return redirect('applied_jobs')

@login_required
def applied_jobs(request):
    applications = Application.objects.filter(seeker=request.user)
    return render(request, 'applied_jobs.html', {'applications': applications})


@login_required
def profile(request):
    profile, created = SeekerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.skills = request.POST.get('skills')
        if 'resume' in request.FILES:
            profile.resume = request.FILES['resume']
        profile.save()
        messages.success(request, 'Profile updated successfully!')
         # Clear old success/error messages
        storage = messages.get_messages(request)
        for _ in storage:
            pass  # this clears messages
        return redirect('profile')
    return render(request, 'profile.html', {'profile': profile})    




        