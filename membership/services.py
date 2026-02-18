import datetime
from django.utils import timezone
from .models import Membership, UserMembership, UserMembershipHistory

class MembershipSystem:
    @staticmethod
    def update(user_membership: UserMembership):
        """
        Updates the user's membership level based on level up point.
        Calculates level_up_point (points needed for next level).
        """
        level_up_point = user_membership.level_up_point
        if level_up_point > 0:
            return

        new_membership = None
        next_membership = None
        
        # 1. Determine Level
        # Get all memberships ordered by min_point_earned ascending
        memberships = Membership.objects.order_by('level')

        for membership in memberships:
            if user_membership.membership.level + 1 == membership.level:
                new_membership = membership
            elif user_membership.membership.level + 2 == membership.level:
                next_membership = membership
                break
        
        if new_membership:
            user_membership.membership = new_membership

            now = timezone.now()
            user_membership.datetime_attached = now
            end_of_year = datetime.datetime(now.year, 12, 31, 23, 59, 59, tzinfo=now.tzinfo)
            user_membership.datetime_ended = end_of_year

            # Attach new level up point
            if next_membership:
                user_membership.level_up_point = next_membership.min_point_earned # Reset the level up point
            else: # Already at the max level
                user_membership.level_up_point = 0

            user_membership.save()

            # Create a new history record
            user_membership_history = UserMembershipHistory(
                user_membership=user_membership,
                membership=new_membership,
                datetime_attached=now,
                datetime_ended=end_of_year
            )
            user_membership_history.save()
            
