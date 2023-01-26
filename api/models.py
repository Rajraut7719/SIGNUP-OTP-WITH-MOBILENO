from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from .manager import CustomUserManager
from django.core.validators import RegexValidator,validate_email
from django.conf import settings 
phone_regex = RegexValidator(
    regex=r"^\d{10}",message='Phone number must be 10 digits only'
)


class User(AbstractBaseUser,PermissionsMixin):
    phone_number = models.CharField(unique=True,max_length=10,blank=False,null=False,validators=[phone_regex])
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_email]
    )
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True,null=True)
    max_otp_try = models.CharField(max_length=2,default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(null=True,blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registred_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"
    objects = CustomUserManager()

    
    USERNAME_FIELD = 'phone_number'
    # REQUIRED_FIELDS = ['']
    def __str__(self) -> str:
        return self.phone_number
