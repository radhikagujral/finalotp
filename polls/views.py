import random
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from .forms import MembershipForm
from django.conf import settings
from email.message import EmailMessage
import smtplib

def Membership(request):
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            print(email)
            user = get_user_model().objects.create_user(username=username, password=password, email=email)
            user.save()

            # Redirect to the OTP verification view
            return redirect(reverse('otp') + '?email=' + email)
    else:
        form = MembershipForm()
    
    return render(request, 'polls/registeration.html', {'form': form})


def send_otp_email(email, otp_generated):
    msg = EmailMessage()
    msg.set_content('Your OTP is {}'.format(otp_generated))

    msg['Subject'] = 'Your OTP for verification'
    msg['From'] = 'gujral.radhika11@gmail.com'  # Replace with your email address
    msg['To'] = email

    smtp_host = 'smtp.gmail.com'
    smtp_port = 587  # Replace with the SMTP server's port number
    smtp_user = 'gujral.radhika11@gmail.com'  # Replace with your email address
    smtp_password = 'ntvmgqluozkkuzhp' # Replace with your email password or app password

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        server.quit()
        print('OTP email sent successfully!')
    except Exception as e:
        print('Error sending OTP email:', str(e))


def otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '')
        if int(otp_entered) == request.session.get('otp', 0):
            # OTP verification successful
            return redirect('/success/') 
        else:
            # Invalid OTP, delete the user and show an error message
            username = request.session.get('username', '')
            user = get_user_model().objects.filter(username=username).first()
            if user:
                user.delete()
            return HttpResponse('Invalid OTP')
    else:
        otp_generated = random.randint(1000, 9999)
        request.session['otp'] = otp_generated
        request.session['username'] = request.POST.get('username', '')
        email = request.GET.get('email') or request.session.get('email')
        # Send the OTP via email
        send_otp_email(email, otp_generated)

        print('OTP:', otp_generated)
        return render(request, 'polls/otp.html')

def registration_view(request):
    return render(request, 'success.html')