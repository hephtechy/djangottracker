from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Attendance, Token
from django.utils import timezone

from .forms import CustomUserCreationForm

from datetime import datetime, date
from twilio.rest import Client
from django.http import HttpResponse
import secrets


account_sid = 'ACef8360beb63c55c90e40efbef944f872'
auth_token = 'ebb7745999c42eb03780fbcd09c67f4b'

def chat_HR(admin='whatsapp:+2347037006829'):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body="Good day HR Mgr \n{} {} just signed in {}!!!".format("first", "second", "third"),
    to=admin
    )



def send_token(request, admin='whatsapp:+2347037006829'):
    if not Token.objects.filter(date=timezone.now().date()).exists():
        global remote_token
        global onsite_token
        remote_token = secrets.token_hex(4)
        onsite_token = secrets.token_hex(4)

        Token.objects.create(
                    remote_token=remote_token,
                    onsite_token=onsite_token)

    token = Token.objects.get(date=timezone.now().date())
    remote_token = token.remote_token
    onsite_token = token.onsite_token

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="Good day HR Mgr \nToday\'s login_token for remote staffs: {}\
        \nToday\'s login_token for on-premise staffs: {}".format(remote_token, onsite_token),
        to=admin
    )

    return HttpResponse(f"Token for remote staffs: {remote_token}, Token for on-premise staffs: {onsite_token}")

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tests')
            # return redirect('attendance_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def tests(request):
    users = CustomUser.objects.all()
    return render(request, "accounts/tests.html", {'users': users})

def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        token = request.POST['token']
        user = authenticate(request, username=username, password=password)
        if user is not None:

            token_object = Token.objects.get(date=timezone.now().date())
            remote_token = token_object.remote_token
            onsite_token = token_object.onsite_token
            user_location = None
            print(remote_token, onsite_token)

            if token == remote_token or token == onsite_token:
                if token == remote_token:
                    user_location = 'remotely'
                else:
                    user_location = 'on premise'
                # Check if user is yet to sign-in today before creating Log instance
                if not Attendance.objects.filter(user=user,date=timezone.now().date()):
                    Attendance.objects.create(
                        user=user,
                        date=timezone.now().date())

                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body="Good day HR Mgr \n{} {} just signed in {}!!!".format(str(user.first_name),
                         str(user.last_name), user_location),
                    to='whatsapp:+2347037006829')
                return redirect('attendance_list')
            else:
                messages.success(request, ("Incorrect token try again."))
        else:
            messages.success(request, ("Invalid username or password. Try again...."))
            return render(request, 'accounts/sign_in.html')
    return render(request, 'accounts/sign_in.html')


def sign_out(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the POST data is being retrieved correctly
        print(f"Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        # Debugging the authenticate function
        if user is not None:
            print(f"Authenticated user: {user.username}")

            try:
                # Check if the user has already signed in today
                if Attendance.objects.filter(user=user, date=timezone.now().date()).exists():
                    attendance = Attendance.objects.get(user=user, date=timezone.now().date())
                    if attendance.sign_out_time == None:
                        attendance.sign_out_time = datetime.now().time()
                        attendance.save()

                        client = Client(account_sid, auth_token)
                        message = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body="Good day HR Mgr \n{} {} just signed out!!!".format(str(user.first_name),
                             str(user.last_name)),
                        to='whatsapp:+2347037006829')
                else:
                    messages.error(request, "You have not signed-in today.")
            except Attendance.DoesNotExist:
                messages.error(request, "Attendance record does not exist.")
        else:
            messages.error(request, "Invalid username or password. Try again....")
        return redirect('attendance_list')
    return render(request, 'accounts/sign_out.html')

def attendance_list(request):
    if request.user.is_authenticated:
        attendances = Attendance.objects.all()
        attendances = Attendance.objects.filter(date=timezone.now().date())
        return render(request, 'accounts/new_attendance_list.html', {'attendances': attendances})
    return redirect('login')
