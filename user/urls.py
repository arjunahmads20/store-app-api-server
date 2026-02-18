from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    UserViewSet, UserInboxViewSet, InvitationRuleViewSet,
    UserInvitationViewSet, UserLogViewSet, OTPVerificationViewSet
)
from .auth_views import signup_request_otp, signup_verify, login, logout

# Main Router
router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'invitation-rules', InvitationRuleViewSet, basename='invitationrule')
router.register(r'otp-verifications', OTPVerificationViewSet, basename='otpverification') # Keep for admin/debug?

# Nested Router (users -> sub-resources)
users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'user-inboxes', UserInboxViewSet, basename='user-userinbox')
users_router.register(r'user-invitations', UserInvitationViewSet, basename='user-userinvitation')
users_router.register(r'user-logs', UserLogViewSet, basename='user-userlog')

urlpatterns = [
    path('signup/request-otp/', signup_request_otp, name='signup-request-otp'),
    path('signup/verify/', signup_verify, name='signup-verify'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
]
