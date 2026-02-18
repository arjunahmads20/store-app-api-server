from django.db import models

class Membership(models.Model):
    LEVEL_CHOICES = (
        (1, 'Bronze'),
        (2, 'Silver'),
        (3, 'Gold'),
        (4, 'Platinum'),
    )
    NAME_CHOICES = (
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
    )

    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, unique=True)
    name = models.CharField(max_length=20, choices=NAME_CHOICES, unique=True)
    description = models.TextField(null=True, blank=True)
    min_point_earned = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class UserMembership(models.Model):
    user = models.OneToOneField('user.User', on_delete=models.CASCADE, related_name='membership')
    referal_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    point = models.PositiveIntegerField(default=0)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    datetime_attached = models.DateTimeField(auto_now_add=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)
    level_up_point = models.IntegerField(default=0)

    def earn_point(self, amount):
        self.point += amount
        # Update the level up point
        self.level_up_point -= amount
        self.save()

class UserMembershipHistory(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    datetime_attached = models.DateTimeField()
    datetime_ended = models.DateTimeField(null=True, blank=True)

class PointMembershipReward(models.Model):
    point_earned = models.PositiveIntegerField()
    for_membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)

class UserPointMembershipReward(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    point_membership_reward = models.ForeignKey(PointMembershipReward, on_delete=models.CASCADE)
    datetime_claimed = models.DateTimeField(auto_now_add=True)

class VoucherOrderMembershipReward(models.Model):
    voucher_order = models.OneToOneField('voucher.VoucherOrder', on_delete=models.CASCADE)
    for_membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    datetime_started = models.DateTimeField(null=True, blank=True)
    datetime_ended = models.DateTimeField(null=True, blank=True)
