from .profile import Profile
from .users import Users
from django_otp.plugins.otp_email.models import EmailDevice


class Repository:
    @property
    def user(self):
        return Users.objects.all()

    @property
    def profile(self):
        return Profile.objects.all()

    @property
    def email_device(self):
        return EmailDevice.objects.all()
