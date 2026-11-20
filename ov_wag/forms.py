from allauth.socialaccount.forms import SignupForm
from django.core.exceptions import ValidationError


class SocialSignupForm(SignupForm):
    """Social sign-up form that takes the email address from Authentik.

    There is no email field: the address is the one Authentik reports, which is also
    what links a login to an existing account, so users cannot choose another one.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('email', None)
        self.authentik_email = (self.initial.get('email') or '').lower()
        self.email_conflict = False
        if self.authentik_email:
            try:
                self.validate_unique_email(self.authentik_email)
            except ValidationError:
                self.email_conflict = True

    @property
    def conflict_message(self):
        return (
            f'An account already exists with the email address {self.authentik_email}. '
            'Ask an administrator to connect it to your Authentik account.'
        )

    def clean(self):
        cleaned_data = super().clean()
        if self.email_conflict:
            raise ValidationError(self.conflict_message)
        return cleaned_data
