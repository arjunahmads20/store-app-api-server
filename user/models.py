from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

class OTPVerification(models.Model):
    phone_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_verified = models.DateTimeField(null=True, blank=True)
    
    # Advanced Rate Limiting Logic
    is_otp_blocked = models.BooleanField(default=False)
    nm = models.PositiveSmallIntegerField(default=settings.OTP_MINUTE_LIMIT)
    nd = models.PositiveSmallIntegerField(default=settings.OTP_DAY_LIMIT)
    dm = models.DateTimeField(null=True, blank=True)
    dd = models.DateTimeField(null=True, blank=True)

    def check_blocking(self):
        from django.conf import settings
        from django.utils import timezone
        
        now = timezone.now()
        minute_block_expired = True
        if self.dm:
            delta = now - self.dm
            if delta.total_seconds() < settings.OTP_MINUTE_BLOCK_DURATION:
                minute_block_expired = False
        
        day_block_expired = True
        if self.dd:
            delta = now - self.dd
            if delta.total_seconds() < settings.OTP_DAY_BLOCK_DURATION:
                day_block_expired = False
        
        if not minute_block_expired:
            return True, "Blocked for 2 minutes."
        if not day_block_expired:
            return True, "Blocked for 1 day."
        
        # Unblock if expired
        if self.is_otp_blocked and minute_block_expired and day_block_expired:
             self.is_otp_blocked = False
             self.save()
             
        return False, None

    def decrease_counters(self):
        from django.conf import settings
        from django.utils import timezone
        
        self.nm -= 1
        self.nd -= 1
        now = timezone.now()
        
        blocked_msg = None
        
        if self.nd <= 0:
            self.is_otp_blocked = True
            self.dd = now
            self.nm = settings.OTP_MINUTE_LIMIT
            self.nd = settings.OTP_DAY_LIMIT
            blocked_msg = "Too many attempts. Blocked for 1 day."
        elif self.nm <= 0:
            self.is_otp_blocked = True
            self.dm = now
            self.nm = settings.OTP_MINUTE_LIMIT
            blocked_msg = "Too many attempts. Blocked for 2 minutes."
            
        self.save()
        return blocked_msg

class User(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    datetime_email_verified = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=50, default='active')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    daily_product_quota = models.PositiveSmallIntegerField(default=10)
    id_store_work_on = models.ForeignKey('store.Store', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    datetime_last_login = models.DateTimeField(null=True, blank=True)
    datetime_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class UserInbox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inbox')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    image_url = models.URLField(max_length=500, null=True, blank=True)
    is_readed = models.BooleanField(default=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_readed = models.DateTimeField(null=True, blank=True)

class InvitationRule(models.Model):
    point_earned_by_inviter = models.PositiveIntegerField(default=0)
    point_earned_by_invitee = models.PositiveIntegerField(default=0)
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_updated = models.DateTimeField(auto_now=True)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_finished = models.DateTimeField(null=True, blank=True)

class UserInvitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_sent')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations_received')
    invitation_rule = models.ForeignKey(InvitationRule, on_delete=models.SET_NULL, null=True)
    datetime_accepted = models.DateTimeField(auto_now_add=True)

class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    details = models.TextField(null=True, blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
