from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic.edit import FormView
from .models import Message
from .forms import ContactForm

SUCCESS_MESSAGE = 'The message was successfully sent!'

# def index(request):
#     if request.method == 'POST':
#         ContactForm().send_email(
#             request.POST['name'],
#             request.POST['email'],
#             request.POST['subject'],
#             request.POST['message']
#         )
#         messages.success(request, )
#         return HttpResponseRedirect(reverse('landing_page:index'))
#     context = None
#     return render(request, 'landing_page/index.html', context)


class  MainContactView(FormView):
    template_name = 'landing_page/index.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.send_message(
            form.cleaned_data['sender'],
            form.cleaned_data['email'],
            form.cleaned_data['subject'],
            form.cleaned_data['body']
        )
        messages.add_message(self.request, messages.SUCCESS, SUCCESS_MESSAGE)
        return super().form_valid(form)
