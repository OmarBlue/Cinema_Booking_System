from django import forms
from Booking_System.models import Booking, Student, Film, CustomUser, ShowTime, Screen, PaymentDetail, Representative, Club, Address, Contact, Account,ClubRep
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.forms import PasswordInput
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

def check_screen_limit(value, screen):
    date = value.date()
    screen_showtimes = ShowTime.objects.filter(screen=screen, start_time__date=date)
    daily_limit = 3  # Daily film limit in a screen
    
    if screen_showtimes.count() >= daily_limit:
        raise ValidationError(f"Screen {screen.screen_number} has reached the daily limit of {daily_limit} films.")

class ManagerUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'user_type']

    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Invalid Username or Password.',
        'inactive': 'This account is inactive.',
    }

class ClubLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Invalid Club Rep Number or Password.',
        'inactive': 'This Account is Inactive.',
    }
    

class StudentRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
 
class CommaSeparatedInput(forms.widgets.TextInput):
    def value_from_datadict(self, data, files, name):
        return [i.strip() for i in data[name].split(',')]

class FilmForm(forms.ModelForm):
    directors = forms.CharField(widget=CommaSeparatedInput)
    cast = forms.CharField(widget=CommaSeparatedInput)

    class Meta:
        model = Film
        fields = ['title', 'release_date', 'directors', 'cast', 'description', 'age_rating', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'age_rating': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class ShowTimeForm(forms.ModelForm):
    film = forms.ModelChoiceField(queryset=Film.objects.all())
    screen = forms.ModelChoiceField(queryset=Screen.objects.order_by('screen_number'))
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = ShowTime
        fields = ['film', 'screen', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        screen = cleaned_data.get('screen')

        if start_time and screen:
            check_screen_limit(start_time, screen)

        return cleaned_data

class ScreenForm(forms.ModelForm):
    screen_number = forms.IntegerField(
        validators=[MaxValueValidator(10)],  # Limit the screen numbers to 10
        required=True,
        help_text="Enter a screen number between 1 and 10"
    )
    seats = forms.IntegerField(
        validators=[MaxValueValidator(100)],  # Set the maximum number of seats
        required=True,
        help_text="Enter the number of seats (max 100)"
    )

    social_distancing = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Enable or disable social distancing"
    )
    class Meta:
        model = Screen
        fields = ['screen_number', 'seats', 'social_distancing']

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'last_name', 'email']

class EditFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'release_date', 'directors', 'cast', 'description', 'age_rating', 'image']

class EditScreenForm(forms.ModelForm):
    screen_number = forms.IntegerField(
        validators=[MaxValueValidator(10)],  # Limit the screen numbers to 10
        required=True,
        help_text="Enter a screen number between 1 and 10"
    )
    seats = forms.IntegerField(
        validators=[MaxValueValidator(100)],  # Set the maximum number of seats
        required=True,
        help_text="Enter the number of seats (max 100)"
    )

    social_distancing = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Enable or disable social distancing"
    )

    class Meta:
        model = Screen
        fields = ['screen_number', 'seats', 'social_distancing']

class EditShowingForm(forms.ModelForm):
    class Meta:
        model = ShowTime
        fields = ['start_time','end_time', 'film', 'screen']
        widgets = {
            'film': forms.Select(attrs={'class': 'custom-select'}),
            'screen': forms.Select(attrs={'class': 'custom-select'}),
        }

class PaymentForm(forms.Form):
    cardholder_name = forms.CharField(max_length=100)
    card_number = forms.CharField(max_length=12)
    expiration_date = forms.CharField(max_length=7)
    cvv = forms.CharField(max_length=3)

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not card_number.isnumeric():
            raise forms.ValidationError('Please enter only numbers for the card number')
        return card_number

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        try:
            month, year = expiration_date.split('/')
            if not (1 <= int(month) <= 12):
                raise forms.ValidationError('Please enter a valid month (e.g. 01 for January)')
            if not (int(year) >= 2022):
                raise forms.ValidationError('Please enter a valid year (e.g. 2022)')
        except ValueError:
            raise forms.ValidationError('Please enter the expiration date in the format MM/YYYY')
        return expiration_date

    def clean_cvv(self):
        cvv = self.cleaned_data['cvv']
        if not cvv.isnumeric():
            raise forms.ValidationError('Please enter only numbers for the CVV')
        return cvv

class AddSearchFilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['title', 'release_date', 'directors', 'cast', 'description', 'age_rating', 'image', 'now_showing']

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        exclude = ['address', 'contact', 'representative', 'rep_number', 'account']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street_number', 'street', 'city', 'post_code']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['landline', 'mobile', 'email']


class RepresentativeForm(forms.ModelForm):

    class Meta:
        model = Representative
        fields = ['first_name', 'last_name', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

User = get_user_model()

class CreateStatementAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_title', 'credit_left', 'discount_rate']
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.filter(user_type__in=[3, 4]), initial=user, validators=[self.validate_user_has_no_accounts])
    
    def validate_user_has_no_accounts(self, value):
        if Account.objects.filter(Q(student__user=value) | Q(club_rep__user=value)).exists():
            raise forms.ValidationError("This user already has an account.")
        return value

    def save(self, commit=True):
        account = super().save(commit=False)
        user = self.cleaned_data['user']
        account.user = user
        
        if commit:
            account.save()
            if user.user_type == 3 and hasattr(user, 'student'):
                user.student.accounts.add(account)
                user.student.save()
            elif user.user_type == 4 and hasattr(user, 'club_rep'):
                user.club_rep.accounts.add(account)
                user.club_rep.save()

        return account


class EditStatementAccountForm(forms.ModelForm):
    account_holder_name = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        student_users = CustomUser.objects.filter(student__isnull=False)
        club_rep_users = CustomUser.objects.filter(club_rep__isnull=False)
        choices = [(user.username, user.username) for user in student_users] + [(user.username, user.username) for user in club_rep_users]
        self.fields['account_holder_name'].choices = choices

    class Meta:
        model = Account
        fields = ['account_title', 'discount_rate','account_holder_name']


class GuestTicketBookingForm(forms.Form):
    student = forms.IntegerField(initial=0, min_value=0, label='Student')
    adults = forms.IntegerField(initial=0, min_value=0, label='Adult')
    senior = forms.IntegerField(initial=0, min_value=0, label='Senior')

