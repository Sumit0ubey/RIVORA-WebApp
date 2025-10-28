from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from time import sleep
import requests as send_request

from contact.form import ContactForm

API_LINK = settings.EMAIL_API_URL


def contact(request):
    api_up = False

    for _ in range(5):
        try:
            response = send_request.get(settings.API_TEST, timeout=5)
            if response.status_code == 200:
                api_up = True
                break
        except Exception as e:
            print("API Error:", e)
        sleep(5)

    if not api_up:
        message = "API is currently down. Please try again later."
        messages.warning(request, message)
        return redirect('Home')

    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        content = (
            f" User Name: {form.cleaned_data['name']}\n"
            f" User Email: {form.cleaned_data['email']}\n\n"
            f" User Problem: {form.cleaned_data['description']}"
        )
        data = {
            "title": form.cleaned_data['reason'],
            "content": content,
            "sendTo": settings.SYSTEM_MAIL,
        }
        headers = {"token": settings.MAIL_TOKEN}

        try:
            response = send_request.post(API_LINK, json=data, headers=headers, timeout=15)
            if response.status_code in [200, 201, 202]:
                messages.success(request, "Thanks for contacting us.")
                form = ContactForm()
                redirect("Contact")
            else:
                messages.error(request, "Failed to submit. Please try again.")
        except send_request.exceptions.RequestException:
            messages.error(request, "Server unreachable. Try again later.")

    return render(request, 'contactus.html', {'form': form})
