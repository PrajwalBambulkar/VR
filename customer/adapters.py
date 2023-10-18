from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from .models import CustProfile

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Called before a user is logged in via a social account.
        """
        user = sociallogin.user

        # Set a unique username based on email
        if not user.username and user.email:
            user.username = user.email.split('@')[0]  # Use email prefix as username

        # Update the User model with Google data if available
        google_account = sociallogin.account
        if google_account:
            user_field(user, 'first_name', google_account.extra_data.get("given_name", ""))
            user_field(user, 'last_name', google_account.extra_data.get("family_name", ""))
            user_field(user, 'email', google_account.extra_data.get("email", ""))
            user.save()  # Save the User model first

            # Create or update the related CustProfile
            cust_profile, created = CustProfile.objects.get_or_create(user=user)
            cust_profile.name = google_account.extra_data.get("name", "")
            cust_profile.email = google_account.extra_data.get("email", "")
            cust_profile.save()