from django import VERSION as DJANGO_VERSION
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import include, path, reverse_lazy

from auth_tests.urls import CustomRequestAuthenticationForm
from authtools import views
from authtools.forms import FriendlyPasswordResetForm

admin.autodiscover()


def dumbview(request):
    return HttpResponse('dumbview')


extra_email_context = {'greeting': 'Hello!'}
if DJANGO_VERSION[:2] >= (3, 0):
    extra_email_context.update(domain='custom.example.com')


urlpatterns = [
    path('reset_and_login/<uidb64>/<token>/', views.PasswordResetConfirmAndLoginView.as_view()),
    path('logout-then-login/', views.LogoutView.as_view(url=reverse_lazy('login')), name='logout_then_login'),
    path('friendly_password_reset/',
        views.PasswordResetView.as_view(form_class=FriendlyPasswordResetForm),
        name='friendly_password_reset'),
    path('login_required/', login_required(dumbview), name='login_required'),
    # From django.contrib.auth.tests.url

    path('password_reset_extra_email_context/', views.PasswordResetView.as_view(extra_email_context=extra_email_context)),
    path('password_reset/html_email_template/', views.PasswordResetView.as_view(html_email_template_name='registration/html_password_reset_email.html')),
    path('', include('authtools.urls')),
    path('reset/post_reset_login/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(post_reset_login=True)),
    path('custom_request_auth_login/',
        views.LoginView.as_view(authentication_form=CustomRequestAuthenticationForm)),
    path(
        'reset/post_reset_login_custom_backend/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(
            post_reset_login=True,
            post_reset_login_backend='django.contrib.auth.backends.AllowAllUsersModelBackend',
        ),
    ),
    path('logout/allowed_hosts/', views.LogoutView.as_view(success_url_allowed_hosts={'otherserver'})),
    path('login/allowed_hosts/', views.LoginView.as_view(success_url_allowed_hosts={'otherserver'})),
]
