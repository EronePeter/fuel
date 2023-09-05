from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .forms import CreateUser


@permission_required('users.add_user')
def register_user(request):
    if request.method == "POST":
        form = CreateUser(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request, "User account created, the user can now login")
            return redirect('register')
    
    form = CreateUser()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
