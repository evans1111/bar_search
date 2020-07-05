from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, AccountUpdateForm
# Messages
# message.debug
# message.info
# message.success
# message.warning
# message.error

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def account(request):
    if request.method == 'POST':
        # User Update Form
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # Account Update Form
        a_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if u_form.is_valid() and a_form.is_valid():
            u_form.save()
            a_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('account')
    else:
        u_form = UserUpdateForm(instance=request.user)
        a_form = AccountUpdateForm(instance=request.user.account)

    context = {
        'u_form': u_form,
        'a_form': a_form
    }

    return render(request, 'users/account.html', context)