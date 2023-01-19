from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, UpdateView

from .decorators import user_not_authenticated
from .forms import UserRegistrationForm, CustomUserChangeForm
from .models import CustomUser
from .tokens import account_activation_token


class MainPageView(LoginRequiredMixin, TemplateView):
    template_name = "base/main.html"


class CustomLoginView(LoginView):
    template_name = "base/login.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('base:main')

    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data()

        if 'email_confirmed' in self.request.session:
            context['email_confirmed'] = self.request.session['email_confirmed']
            del self.request.session['email_confirmed']
        return context


def confirm_email(request):
    return render(
        request=request,
        template_name="base/confirm_email.html",
    )


@user_not_authenticated
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('base:confirm_email')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="base/register.html",
        context={"form": form}
    )


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = CustomUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "base/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@student_helper.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="base/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("base:password_reset_complete")


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('base/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():

        return redirect('base.html')
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    print(user)
    print(account_activation_token.check_token(user, token))

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        request.session['email_confirmed'] = 'Thank you for your email confirmation. Now you can login into your ' \
                                             'account.'
        return redirect('base:login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('base:main')


class ProfileUpdateView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'base/user_update.html'
    success_url = reverse_lazy('todolist:tasks')

    def get_object(self, *args, **kwargs):
        return self.request.user


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "base/password/password_change.html"
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('todolist:tasks')
