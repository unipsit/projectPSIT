from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from items.models import Item, Icon
from django.utils import timezone
from django.views.generic import ListView

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created! So go and Login!!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
    

@login_required
def show_profile(request):
    items_post = Item.objects.filter(post_by = request.user.id).order_by('-accept_by')
    items_accept = Item.objects.filter(accept_by = request.user.id).order_by('need_at')
    items_expire = list(Item.objects.filter(need_at__lt = timezone.now()))
    not_return = list(Item.objects.filter(return_at__lt = timezone.now()))
    context = {
            'items' : items_post,
            'accepts' : items_accept,
            'icon' : Icon,
            'time' : items_expire,
            'not_return' : not_return
    }
    return render(request, 'profile.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
      
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'profile_edit.html', context)