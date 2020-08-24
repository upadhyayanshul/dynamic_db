# IMPORT THE REQUIRED MODULE FOR THE TOKEN GENERATION 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

# DEFINE TOKEN GENERATION CLASS FOR GENERATING THE TOKEN FOR USER VERIFICATION
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

	#MAKE HASHED TOKEN WITH SIX WITH BELOW COMBINATION
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
# CALL THE TOKEN ACTIVATION CLASS AS OBJECT TO USE BY MODULE NAME IN VIEWS FUNCTIONS
account_activation_token = AccountActivationTokenGenerator()