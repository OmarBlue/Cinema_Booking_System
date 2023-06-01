from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.signals import request_finished

@receiver(request_finished)
def create_superuser(sender, **kwargs):
    User = get_user_model()

    # Define the superuser details
    username = "superuser"
    email = "superuser@gmail.com"
    password = "superpassword"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)

        
@receiver(post_migrate)
def create_default_managers(sender, **kwargs):
    User = get_user_model()

    Cinema_Manager_username = 'User_CM'
    Cinema_Manager_email = 'cinema_manager@gmail.com'
    Cinema_Manager_password = 'cinemamanager1'

    Account_Manager_username = 'User_AM'
    Account_Manager_email = 'account_manager@gmail.com'
    Account_Manager_password = 'accountmanager1'

    if not User.objects.filter(username=Cinema_Manager_username).exists():
        User.objects.create_user(
            username=Cinema_Manager_username,
            email=Cinema_Manager_email,
            password=Cinema_Manager_password,
            user_type=1
        )

    if not User.objects.filter(username=Account_Manager_username).exists():
        User.objects.create_user(
            username=Account_Manager_username,
            email=Account_Manager_email,
            password=Account_Manager_password,
            user_type=2
        )
