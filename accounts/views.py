from django.shortcuts import render, redirect, HttpResponse
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Q
from .forms import login_form
from cart.views import create_cart
from order.models import Order

# Create your views here.

#user registration view
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            has_email = User.objects.filter(email= email)
            if has_email.exists():
                form.add_error('email', 'This email already exists!')
            else:
                user = form.save(commit= True)
                user_id = user.id
                current_site = get_current_site(request)
                #user email varification system implementation
                mail_subject = 'Activation link has been sent to your email id'
                message = render_to_string('accounts/confirmation_link.html',{
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user_id)),
                    'token': default_token_generator.make_token(user)
                })
                to_send = user.email
                email = EmailMessage(
                            mail_subject, message, to=[to_send, ]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

#user activated after email verification
def activated(request, uid, token):
    user_id = urlsafe_base64_decode(uid).decode()
    try:
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()
        login(request, user)
        create_cart(user)
        return redirect('home')
    except ValueError:
        return HttpResponse('Invalid activation link')
    except User.DoesNotExist:
        return HttpResponse('User not found')

#user login view
def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #authenticate with username and password
            user = authenticate(request, username=username, password=password)
            #check user account
            if user:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, ('Please correct the error below.'))
                return redirect('login')
    else:
        form = login_form()
    return render(request, 'accounts/signin.html', {'form': form})

#user logout view
def user_logout(request):
    logout(request)
    return redirect('home')

#user password change implementation
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, ('Your password was successfully updated!'))
                return redirect('change_password')
            else:
                messages.error(request, ('Please correct the error below.'))
        else:
            form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})
    else:
        return redirect('home')

#user profile view
def profile(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, status__in=['New', 'Accepted', 'Complete'])
        return render(request, 'accounts/dashboard.html', {'orders': orders})

#Receive product view
def received_view(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user, status= 'Received')
        return render(request, 'accounts/received_order.html', {'orders': orders})