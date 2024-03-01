from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
username_validator = UnicodeUsernameValidator()

class User(AbstractUser):
    # WARNING!
    """
    Some officially supported features of Crowdbotics Dashboard depend on the initial
    state of this User model (Such as the creation of superusers using the CLI
    or password reset in the dashboard). Changing, extending, or modifying this model
    may lead to unexpected bugs and or behaviors in the automated flows provided
    by Crowdbotics. Change it at your own risk.


    This model represents the User instance of the system, login system and
    everything that relates with an `User` is represented by this model.
    """

    # First Name and Last Name do not cover name patterns
    # around the globe.
    username = models.CharField(
        _('username'),
        max_length=150,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        null=True,
        blank=True,
    )
    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True, null=True, unique=True)
    email = models.EmailField(_("Email"), blank=True, null=True, unique=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    role = models.CharField(max_length=255, choices=[('buyer','buyer'), ('seller','seller')], blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    credit_card_verified = models.BooleanField(default=False)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
    
    def verify_code(self, verification_code):
        if self.verification_code == verification_code:
            # Clear the verification code after successful verification
            self.verification_code = None
            self.save()
            return True
        else:
            return False
