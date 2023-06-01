from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# Create your models here.

class Director(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Cast(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Film(models.Model):
    film_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    directors = models.ManyToManyField(Director, blank=True, null=True)
    cast = models.ManyToManyField(Cast, blank=True, null=True)
    description = models.TextField()
    age_rating = models.CharField(max_length=5)
    image = models.ImageField(upload_to='film_images/', blank=True, null=True)
    now_showing = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Screen(models.Model):
    screen_number = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)], # Limit the screens to 10
        unique=True
    )
    seats = models.PositiveIntegerField(default=0)
    social_distancing = models.BooleanField(default=False)

    def __str__(self):
        return f"Screen {self.screen_number}"
        
class ShowTime(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='show_times')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.film.title} - {self.start_time} to {self.end_time} on Screen {self.screen.screen_number}"

class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    show_time = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.CharField(max_length=3)
    is_available = models.BooleanField(default=True)
    user = models.ForeignKey(
        'CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('screen', 'seat_number', 'show_time')

    def __str__(self):
        return f"Screen {self.screen.screen_number} - Seat {self.seat_number} - Show Time {self.show_time}"


class Address(models.Model):
    street_number = models.CharField(max_length=50)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    post_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street_number} {self.street}, {self.city} {self.post_code}"


class Contact(models.Model):
    landline = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"Landline: {self.landline}, Mobile: {self.mobile}, Email: {self.email}"


class Representative(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    rep_number = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def generate_unique_rep_number(self):
        while True:
            rep_number = uuid.uuid4().hex[:10]
            if not Representative.objects.filter(rep_number=rep_number).exists():
                return rep_number

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (0, 'superuser'),
        (1, 'cinema_manager'),
        (2, 'account_manager'),
        (3, 'student'),
        (4, 'club_rep'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=0)

    REQUIRED_FIELDS = ['email', 'password', 'user_type', 'first_name', 'last_name']

    def get_account(self):
        if self.user_type == 3:
            account = self.student.accounts.first()
        elif self.user_type == 4:
            if self.club_rep.accounts.exists():
                account = self.club_rep.accounts.first()
            else:
            #     # create a new account for the club rep
            #     account_title = f"{self.club_rep.representative.first_name} {self.club_rep.representative.last_name} Account"
                account = None
        else:
            account = None
        
        return account


class Club(models.Model):
    name = models.CharField(max_length=200)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    representative = models.ForeignKey(Representative, on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class ClubRep(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='club_rep')
    representative = models.OneToOneField(Representative, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def club_account(self):
        return self.club.account

class Student(models.Model):
    Student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    has_discount = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.accounts.first().credit_left} Left"

    @property
    def account(self):
        return Account.objects.get(content_type=ContentType.objects.get_for_model(self), object_id=self.pk)

class StatementAccountRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiration_month = models.CharField(max_length=2)
    expiration_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)

class Account(models.Model):
    account_number = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    account_title = models.CharField(max_length=100)
    credit_left = models.DecimalField(max_digits=5, decimal_places=2, default=0, validators=[MaxValueValidator(100)])
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='accounts')
    club_rep = models.ForeignKey(ClubRep, on_delete=models.CASCADE, null=True, blank=True, related_name='accounts')
    account_holder_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Account Number: {self.account_number} - Account Title: {self.account_title}"

    def save(self, *args, **kwargs):
        if self.student:
            self.account_holder_name = self.student.user.username
        elif self.club_rep:
            self.account_holder_name = self.club_rep.user.username
        super(Account, self).save(*args, **kwargs)

class PaymentDetail(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_details')
    # student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_details')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_details')
    cardholder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16)
    expiration_month = models.CharField(max_length=2)
    expiration_year = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.account.content_object.user.username} - {self.card_number[-4:]}"
        
class Booking(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    date_booked = models.DateTimeField(auto_now_add=True)
    booking_number = models.CharField(max_length=36, default=uuid.uuid4, editable=False)
    student_tickets = models.PositiveSmallIntegerField(default=0)
    adult_tickets = models.PositiveSmallIntegerField(default=0)
    senior_tickets = models.PositiveSmallIntegerField(default=0)
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=5)

    def __str__(self):
        return f'{self.user} - {self.film} - {self.screen} - Booking Number: {self.booking_number}'

class SeatSelection(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='seat_selections')
class AccountStatement(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    statement_date = models.DateField()
    film_name = models.CharField(max_length=255)
    ticket_quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount", help_text="Enter a positive or negative amount.")
    credit_balance = models.DecimalField(max_digits=10, decimal_places=2)
    TRANSACTION_TYPE_CHOICES = (
        ('C', 'Cancel Booking'),
        ('B', 'Confirm Booking'),
    )
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE_CHOICES)
    
    def __str__(self):
        return f"{self.user} - {self.statement_date} - {self.film_name} - {self.amount} - {self.credit_balance()}"