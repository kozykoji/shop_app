from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
 
 
class CustomUserCreationForm(UserCreationForm):
    """ 
https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
    """
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'username')
 
 
class CustomUserChangeForm(UserChangeForm):
    """ https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.forms.UserChangeForm
    """
 
    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('email', 'username')
