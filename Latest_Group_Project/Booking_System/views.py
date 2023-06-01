from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
import requests, io, random, string
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate,get_user_model
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection, transaction, DataError
from django.contrib.auth.hashers import check_password, make_password
from .permissions import User_in_group
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from datetime import datetime, timedelta, date
from dateutil import parser
from django.db.models import Prefetch
import uuid
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
import secrets, string
from django.contrib.sessions.models import Session
from .decorators import is_cinema_manager, is_account_manager, user_passes_test_custom, is_student, is_club_rep, is_club_rep_or_student
import json, calendar, pytz

User = get_user_model()

# Create your views here.
def home(request):
    auto_logout = request.GET.get('auto_logout')

    if auto_logout:
        logout(request)
        messages.error(request, 'You have been logged out due to inactivity.')

    message = request.session.pop('permission_denied_message', None)
    if message:
        messages.error(request, message)

    current_time = timezone.now()
    now_showing_films = Film.objects.filter(now_showing=True, showtime__end_time__gt=current_time).distinct().order_by('title')
    
    film_images = [film.image for film in now_showing_films if film.image]
    
    today = datetime.now().date()
    week_today = [today.strftime('%A') ]
    
    return render(request, 'Booking_System/home.html', {'now_showing_films': now_showing_films, 'film_images': film_images, 'today':week_today[0]})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@transaction.atomic
def remove_showing(request, showing_id):
    showing = get_object_or_404(Showtime, pk=showing_id)
    film = showing.film
    film.now_showing = False
    film.save()
    showing.delete()
    return redirect('display_film')

def register_tabs(request):
    if request.method == 'POST':
        if 'student_submit' in request.POST:
            user_form = StudentRegisterForm(request.POST)
            if user_form.is_valid():
                if CustomUser.objects.filter(username=user_form.cleaned_data['username'], 
                             first_name=user_form.cleaned_data['first_name'], 
                             last_name=user_form.cleaned_data['last_name']).exists():
                    messages.error(request, 'This User Already Exist!')
                    return redirect('register_tabs')
                user = user_form.save(commit=False)
                user.user_type = 3
                user.save()
                Student.objects.create(user=user)
                messages.success(request, 'Register Request Sent Successfully.')
                return redirect('home')
            else:
                messages.error(request, 'Username Already Exist, Please Try Again!')
                return redirect('register_tabs')
        elif 'club_submit' in request.POST:
            club_form = ClubForm(request.POST)
            address_form = AddressForm(request.POST)
            contact_form = ContactForm(request.POST)
            representative_form = RepresentativeForm(request.POST)
            
            # Ignore the validity of the user form if only the club form is submitted
            user_form = None if 'student_submit' in request.POST else StudentRegisterForm()

            if Club.objects.filter(name__iexact=request.POST['name']).exists():
                messages.error(request, 'This Club Name Already Exist!')
            elif club_form.is_valid() and address_form.is_valid() and contact_form.is_valid() and representative_form.is_valid():
                first_name = representative_form.cleaned_data['first_name']
                last_name = representative_form.cleaned_data['last_name']
                if Representative.objects.filter(first_name=first_name, last_name=last_name).exists():
                    messages.error(request, 'This Representative Already Exist!')
                else:
                    club = club_form.save(commit=False)
                    address = address_form.save()
                    contact = contact_form.save()
                    representative = representative_form.save(commit=False)
                    representative.rep_number = representative.generate_unique_rep_number()
                    representative.save()  # Save the representative object
                    club.address = address
                    club.contact = contact
                    club.representative = representative
                    club.save()

                    characters = string.ascii_letters + string.digits
                    password = ''.join(secrets.choice(characters) for i in range(9))

                    # Save the club representative number, password, and club name to a text file
                    with open('./Club_Rep_User_LogIn.txt', 'a') as file:
                        file.write(f'Club Name: {club.name}\n')
                        file.write(f'Club rep number: {representative.rep_number}\n')
                        file.write(f'Password: {password}\n\n')

                    # Create new CustomUser for Club Representative
                    user = CustomUser.objects.create(
                        username=representative.rep_number,
                        email=contact.email,
                        first_name=representative.first_name,
                        last_name=representative.last_name,
                        password=make_password(password), 
                        user_type=4,  # Club Representative user type
                    )
                    user.save()

                    # Create new ClubRep object
                    club_rep = ClubRep.objects.create(user=user, representative=representative, club=club, approved=False)

                    user.club_rep = club_rep
                    user.save()

                    messages.success(request, 'Club Register Request Sent Successfully.')
                    return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials, Please Try Again!')
                return redirect('register_tabs')
    else:
        user_form = StudentRegisterForm()
        club_form = ClubForm()
        address_form = AddressForm()
        contact_form = ContactForm()
        representative_form = RepresentativeForm()
    return render(request, 'Booking_System/register_tab.html', {
        'form': user_form,
        'club_form': club_form,
        'address_form': address_form,
        'contact_form': contact_form,
        'representative_form': representative_form
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        club_form = ClubLoginForm(request, data=request.POST)
        
        if 'student_login' in request.POST and form.is_valid():
            user = form.get_user()

            if user.user_type == 4:
                messages.error(request, 'Invalid Login Credentials for Student.')
                return redirect('login_view')
                
            # Check if the user is a student and is approved
            if user.user_type == 3:
                try:
                    student = Student.objects.get(user=user)
                    if not student.approved:
                        messages.error(request, 'Please wait, Your account is not yet approved.')
                        return redirect('login_view')
                except Student.DoesNotExist:
                    messages.error(request, 'Student account not found.')
                    return redirect('login_view')

            # Check if the user is a club rep and is approved
            if user.user_type == 4:
                try:
                    club_rep = ClubRep.objects.get(user=user)
                    if not club_rep.approved:
                        messages.error(request, 'Please wait, Your club account is not yet approved.')
                        return redirect('login_view')
                except ClubRep.DoesNotExist:
                    messages.error(request, 'Club representative account not found.')
                    return redirect('login_view')
                    
            login(request, user)
            messages.success(request, 'Logged In Successfully.')
            request.session['last_activity'] = str(timezone.now())
            request.session['token'] = str(uuid.uuid4())
            return redirect('home')

        elif 'club_rep_login' in request.POST and club_form.is_valid():
            user = club_form.get_user()
            if user.user_type != 4:
                messages.error(request, 'Invalid Login Credentials for Club Rep.')
                return redirect('login_view')

            if user.user_type == 4:
                try:
                    club_rep = ClubRep.objects.get(user=user)
                    if not club_rep.approved:
                        messages.error(request, 'Please wait, Your club account is not yet approved.')
                        return redirect('login_view')
                except ClubRep.DoesNotExist:
                    messages.error(request, 'Club representative account not found.')
                    return redirect('login_view')
                    
                login(request, user)
                messages.success(request, 'Logged In Successfully.')
                request.session['last_activity'] = str(timezone.now())
                request.session['token'] = str(uuid.uuid4())
                return redirect('home')
            else:
                messages.error(request, 'Invalid Login Credentials.')
                return redirect('login_view')
       
        else: 
            messages.error(request, 'Invalid Username or Password.')
            return redirect('login_view')
    else:
        form = AuthenticationForm()
        club_form = ClubLoginForm()
 
    return render(request, 'Booking_System/login.html', {'form': form, 'club_form': club_form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required    
def register_club(request):
    if request.method == 'POST':
        club_form = ClubForm(request.POST)
        address_form = AddressForm(request.POST)
        contact_form = ContactForm(request.POST)
        representative_form = RepresentativeForm(request.POST)

        if Club.objects.filter(name__iexact=request.POST['name']).exists():
            messages.error(request, 'This Club Name Already Exist!')
        elif club_form.is_valid() and address_form.is_valid() and contact_form.is_valid() and representative_form.is_valid():
            first_name = representative_form.cleaned_data['first_name']
            last_name = representative_form.cleaned_data['last_name']
            if Representative.objects.filter(first_name=first_name, last_name=last_name).exists():
                messages.error(request, 'This Representative Already Exist!')
            else:
                club = club_form.save(commit=False)
                address = address_form.save()
                contact = contact_form.save()
                representative = representative_form.save(commit=False)
                representative.rep_number = representative.generate_unique_rep_number()
                representative.save()  # Save the representative object
                club.address = address
                club.contact = contact
                club.representative = representative
                club.save()

                # representative.rep_number = uuid.uuid4().hex[:10]

                characters = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(characters) for i in range(9))
                print('Password for club rep:', password)
                # Create new CustomUser for Club Representative
                user = CustomUser.objects.create(
                    username=representative.rep_number,
                    email=contact.email,
                    first_name=representative.first_name,
                    last_name=representative.last_name,
                    password=make_password(password), 
                    user_type=4,  # Club Representative user type
                )
                user.save()

                # Create new ClubRep object
                club_rep = ClubRep.objects.create(user=user, representative=representative, club=club)

                user.club_rep = club_rep
                user.save()

                messages.success(request, 'Club Registration Successful.')
                return redirect('home')
    else:
        club_form = ClubForm()
        address_form = AddressForm()
        contact_form = ContactForm()
        representative_form = RepresentativeForm()
    return render(request, 'Booking_System/register_club.html', {'club_form': club_form, 'address_form': address_form, 'contact_form': contact_form, 'representative_form': representative_form})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def display_all_clubs(request):
    clubs = Club.objects.all()
    return render(request, 'Booking_System/display_all_clubs.html', {'clubs': clubs})

 
def register_student(request):
    if request.method == 'POST':
        user_form = StudentRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 3  
            user.save()
            Student.objects.create(user=user)
            messages.success(request, 'Register Request Sent Successfully')
            return redirect('home')
    else:
        user_form = StudentRegisterForm()

    return render(request, 'Booking_System/register.html', {'form': user_form})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def pending_students_registrations(request):
    non_approved_students = Student.objects.exclude(approved=True)
    return render(request, "Booking_System/pending_students_registrations.html", {'students': non_approved_students})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def pending_club_registrations(request):
    pending_club_reps = ClubRep.objects.filter(approved=False)
    return render(request, 'Booking_System/pending_club_registrations.html', {'pending_club_reps': pending_club_reps})

@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def pending_statement_account(request):
    statementaccountrequest = StatementAccountRequest.objects.all()
    return render(request, "Booking_System/pending_statement_account.html", {'statementaccountrequest': statementaccountrequest})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def approve_student(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    student = Student.objects.get(user=user)
    student.approved = True
    student.user.save()
    student.save()
    username = student.user.username
    messages.success(request, f'Student {username} approved.')
    return redirect('pending_students_registrations')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def decline_student(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    student = Student.objects.get(user=user)
    username = student.user.username
    student.delete()
    user.delete()
    messages.success(request, f'Student {username} declined and removed.')
    return redirect('pending_students_registrations')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def approve_club_registration(request, club_rep_id):
    club_rep = get_object_or_404(ClubRep, pk=club_rep_id)
    club_rep.approved = True
    club_rep.save()
    club_rep_name = club_rep.club.name
    messages.success(request, f"Club {club_rep_name} registration approved.")
    return redirect('pending_club_registrations')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def decline_club_registration(request, club_rep_id):
    club_rep = get_object_or_404(ClubRep, pk=club_rep_id)
    user = club_rep.user
    club = club_rep.club
    club_name = club.name
    
    # Delete the associated Address, Contact, and Representative objects
    club.address.delete()
    club.contact.delete()
    club.representative.delete()
    
    # Delete the associated Club object
    club.delete()
    
    # Delete the associated CustomUser object
    user.delete()
    
    # Delete the ClubRep object
    club_rep.delete()

    club_rep_name = club_rep.club.name

    messages.success(request, f"Club {club_rep_name} registration declined.")
    return redirect('pending_club_registrations')

@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def finish_statement_request(request, request_id):
    statement_request = get_object_or_404(StatementAccountRequest, id=request_id)
    statement_request.delete()
    messages.success(request, "Statement account request removed.")
    return redirect('pending_statement_account')

@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def booking_history(request):
    bookings = Booking.objects.all()
    return render(request, 'Booking_System/booking_history.html', {'bookings': bookings})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def add_film(request):
    if request.method == 'POST':
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            if Film.objects.filter(title=title).exists():
                messages.warning(request, 'A film with this title already exists.')
                return redirect('add_film')
            
            director_names = [name.strip().replace("'", "").replace("[", "").replace("]", "") for name in form.cleaned_data['directors'].split(',') if name.strip()]
            directors = [Director.objects.get_or_create(name=name)[0] for name in director_names]

            cast_names = [name.strip().replace("'", "").replace("[", "").replace("]", "") for name in form.cleaned_data['cast'].split(',') if name.strip()]
            cast = [Cast.objects.get_or_create(name=name)[0] for name in cast_names]

            film = form.save(commit=False)
            film.now_showing = False
            film.save()
            film.directors.set(directors)
            film.cast.set(cast)
            messages.success(request, 'Film added successfully.')
            return redirect('home')
    else:
        form = FilmForm()
    return render(request, 'Booking_System/add_film.html', {'form': form})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def edit_film(request, film_id):
    film = Film.objects.get(film_id=film_id)

    if request.method == 'POST':
        form = EditFilmForm(request.POST, instance=film)
        if form.is_valid():
            form.save()
            messages.success(request, 'Film Updated Successfully')
            return redirect('display_film')
    else:
        form = EditFilmForm(instance=film)
        context = {'form': form}
    return render(request, 'Booking_System/edit_film.html', context)

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def delete_film(request, film_id):
    film = get_object_or_404(Film, pk=film_id)

    # Check if any showings are related to this film
    still_showing = ShowTime.objects.filter(film=film).exists()
    
    if request.method == 'POST':
        if not still_showing:
            film.delete()
            messages.success(request, 'Film deleted successfully.')
            return redirect('display_film')
        else: 
            messages.error(request, 'This Film is still in showing, Cannot Delete.')
            return redirect('display_film')

    return redirect('home')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required    
def remove_showing(request, film_id):
    film = get_object_or_404(Film, pk=film_id)
    show_times = ShowTime.objects.filter(film=film)
    show_times.delete()
    film.now_showing = False
    film.save()
    messages.success(request, 'Film showing removed successfully.')
    return redirect('display_film')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def display_film(request):
    films = Film.objects.all()
    return render(request, 'Booking_System/display_films.html', {'films': films})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def add_showtime(request):
    if request.method == 'POST':
        form = ShowTimeForm(request.POST)
        if form.is_valid():
            showtime = form.save(commit=False)
            screen = form.cleaned_data['screen']
            selected_date = form.cleaned_data['start_time'].date()
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            film = form.cleaned_data['film']

            # Check if there is any overlapping showtime on the same screen and date
            overlapping_showtimes = ShowTime.objects.filter(
                screen=screen,
                start_time__date=selected_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            if overlapping_showtimes.exists():
                messages.error(request, 'The new showtime overlaps with an existing showtime on the same screen and date.')
                return redirect('add_showtime')
            
            # Check if there is already a showtime with a different film assigned on the same screen and date
            conflicting_showtimes = ShowTime.objects.filter(
                screen=screen,
                start_time__date=selected_date
            ).exclude(film_id=film.film_id if film else None)
            if conflicting_showtimes.exists():
                messages.error(request, 'There is already a showtime with a different film assigned on the same screen and date.')
                return redirect('add_showtime')

            # Save the showtime
            showtime.save()
            film = form.cleaned_data['film']
            film.now_showing = True
            film.save()
            messages.success(request, 'Film Showtime Added.')
            return redirect('add_showtime')
    else:
        form = ShowTimeForm()

    showtimes = ShowTime.objects.all().order_by('start_time')
    return render(request, 'Booking_System/add_showtime.html', {'form': form, 'showtimes': showtimes})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def delete_finished_showtimes(request):
    if request.method == 'POST':
            finished_showtimes = ShowTime.objects.filter(end_time__lte=timezone.now())
            finished_showtimes.delete()
            messages.success(request, "Finished showtimes have been deleted.")
            return redirect('display_film') 

    return redirect('home') 

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def manage_screen(request):
    try:
        screens = Screen.objects.all().order_by('screen_number')

        if request.method == 'POST':
            form = ScreenForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Screen added successfully')
                return redirect('manage_screen')
        else:
            form = ScreenForm()

    except Screen.DoesNotExist:
        messages.error(request, 'No Screen Recorded Yet')
        return redirect('home')

    return render(request, 'Booking_System/manage_screen.html', {'form': form, 'screens': screens})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def manage_showing(request):
    showings = ShowTime.objects.all().order_by('start_time')
    return render(request, 'Booking_System/manage_showing.html', {'showings': showings})

def now_showing(request):
    today = datetime.now().date()
    selected_day_str = request.GET.get('day')

    if selected_day_str:
        selected_day = parser.parse(selected_day_str)
        # Calculate the date delta to get the actual date
        delta = (selected_day.weekday() - today.weekday()) % 7
        selected_date = today + timedelta(days=delta)
    else:
        selected_date = date.today()

    days_of_week = [(today + timedelta(days=i)).strftime('%A') for i in range(7)]
    screens = Screen.objects.prefetch_related(Prefetch('show_times', queryset=ShowTime.objects.filter(start_time__date=selected_date).order_by('start_time'))).order_by('screen_number')
    
    # Calculate the duration of each film
    for screen in screens:
        for show_time in screen.show_times.all():
            duration = int((show_time.end_time - show_time.start_time).total_seconds() // 60)
            show_time.film.duration = duration

    # Get the films playing on the selected date
    films = [show.film for screen in screens for show in screen.show_times.all()]


    context = {
        'days_of_week': days_of_week,
        'screens': screens,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'films': films,
    }

    return render(request, "Booking_System/now_showing.html", context)

def book_specific_dates(request):
    selected_date = request.GET.get('selected_date')

    if selected_date:
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            selected_date = datetime.now().date()
    else:
        selected_date = datetime.now().date()

    screens = Screen.objects.prefetch_related(Prefetch('show_times', queryset=ShowTime.objects.filter(start_time__date=selected_date).order_by('start_time'))).order_by('screen_number')

    if selected_date:
        show_times = ShowTime.objects.filter(start_time__date=selected_date)
        screens = Screen.objects.prefetch_related(Prefetch('show_times', queryset=ShowTime.objects.filter(start_time__date=selected_date).order_by('start_time'))).order_by('screen_number')

    if show_times:
        durations = int((show_times[0].end_time - show_times[0].start_time).total_seconds() // 60)
    else:
        durations = 0

    title = f"Now Showing on {selected_date.strftime('%B %d, %Y')}"
    return render(request, 'Booking_System/book_specific_date.html',
    {
        'screens': screens,
        'selected_date': selected_date,
        'title': title,
        'durations' : durations,
    })

@login_required
@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
def ticket_selection_booking(request, showtime_id):
    show_time = get_object_or_404(ShowTime, id=showtime_id)
    film = show_time.film
    screen = show_time.screen

    # Check if the showtime has already passed
    if show_time.start_time <= timezone.now():
        messages.error(request, "This showtime has already started. Please select another show time.")
        return redirect('home')  

    if request.method == 'POST':
        form = GuestTicketBookingForm(request.POST)
        if form.is_valid():
            adult_tickets = form.cleaned_data['adult_tickets']
            student_tickets = form.cleaned_data['student_tickets']
            senior_tickets = form.cleaned_data['senior_tickets']

            # Redirect to the receipt page
            return redirect('receipt', booking_id=booking.id)

    else:
        form = GuestTicketBookingForm()

    return render(request, 'Booking_System/ticket_booking.html', {
        'form': form,
        'film': film,
        'show_time': show_time,
        'screen': screen,
        'is_club_rep': is_club_rep(request.user), 
    })

@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def confirm_booking(request):
    if request.method == 'POST':
        try:
            # Retrieve the form data from the POST request
            adult_tickets = request.POST.get('adults', 0)
            student_tickets = request.POST.get('student', 0)
            senior_tickets = request.POST.get('senior', 0)
            showtime_id = request.POST.get('showtime_id')
        
            # Retrieve the showtime object from the database
            showtime = ShowTime.objects.get(id=showtime_id)
            
            total_tickets = int(student_tickets) + int(adult_tickets) + int(senior_tickets) 
        
            # Getting user account to check the discount they have
            try:
                user_account = Account.objects.get(student__user=request.user)
            except Account.DoesNotExist:
                try:
                    user_account = Account.objects.get(club_rep__user=request.user)
                except Account.DoesNotExist:
                    user_account = None
                    messages.error(request, 'No Account Found For This User. Please Request an Account.')
                    return redirect('home')

            discount_rate = user_account.discount_rate

            # Calculate the total amount
            amount = 5 * int(student_tickets) + 10 * int(adult_tickets) + 7 * int(senior_tickets)
            amount = amount * (1 - discount_rate / 100)

            # Check if selected seats are available
            unavailable_seats = Seat.objects.filter(screen_id=showtime.screen.id, film_id=showtime.film.film_id, show_time_id=showtime_id, is_available=False)
            unavailable_seat_numbers = [seat.seat_number for seat in unavailable_seats]

            # Check if all of the ticket quantities are zero
            if total_tickets == 0:
                messages.error(request, 'Please select at least one ticket for each category.')
                return redirect('ticket_selection_booking', showtime_id=showtime_id)
            
            if showtime.screen.social_distancing:
                # Check if there are enough available seats for the selected tickets
                if len(unavailable_seats) + total_tickets > showtime.screen.seats / 2:
                    messages.error(request, 'Not enough seats available. Please select fewer tickets.')
                    return redirect('ticket_selection_booking', showtime_id=showtime_id)
            else:
                # Check if there are enough available seats for the selected tickets
                if len(unavailable_seats) + total_tickets > showtime.screen.seats:
                    messages.error(request, 'Not enough seats available. Please select fewer tickets.')
                    return redirect('ticket_selection_booking', showtime_id=showtime_id)

            # Create a new booking object and save it to the database
            booking = Booking.objects.create(
                film=showtime.film,
                screen=showtime.screen,
                user=request.user,
                student_tickets=student_tickets,
                adult_tickets=adult_tickets,
                senior_tickets=senior_tickets,
                showtime_id = showtime_id,
                amount=amount
            )
            
            # return redirect('seat_selection', booking_id=booking.id)
            return render(request, 'Booking_System/seat_selection.html', {
                'booking': booking,
                'student_tickets': student_tickets,
                'adult_tickets': adult_tickets,
                'senior_tickets': senior_tickets,
                'unavailable_seat_numbers': unavailable_seat_numbers,
                'total_tickets': total_tickets,
                'screen_seats': showtime.screen.seats,
                'is_seat_selection': True,
                'social_distancing': showtime.screen.social_distancing,
            })
        except DataError:
            messages.error(request, 'The total amount is too large.')
            return redirect('ticket_selection_booking', showtime_id=showtime_id)

    else:
        messages.error(request, 'Booking Failed')
        return redirect('home')

def save_seat_selection(request, booking_id):
    if request.method == 'POST':
        # Get the booking object from the database
        booking = Booking.objects.get(id=booking_id)
        showtime_id = booking.showtime_id
        film_id = booking.film
        screen_id = booking.screen
        user_id = booking.user.id
        
        total_tickets = int(request.POST.get('total_tickets', 0))
        
        # Check if there is enough credit left in the account
        account = request.user.get_account()
        if account.credit_left < booking.amount:
            messages.error(request, 'You do not have enough credit in your account. Please top up your account.')
            booking.delete()
            return redirect('topup')

        # Deduct the amount from the account's credit
        account.credit_left -= booking.amount
        account.save()

        # Get the selected seats from the POST data
        selected_seats = request.POST.get('selected_seats')
        selected_seat_numbers = selected_seats.split(',')
        # Check if any seats were selected
        if not selected_seats:
            messages.error(request, 'Booking Failed! Please select a seat.')
            booking.delete()
            account.credit_left += booking.amount
            account.save()
            return redirect('home')

        # Check if the number of selected seats matches the number of tickets
        if len(selected_seat_numbers) != total_tickets:
            messages.error(request, 'Please select {} seats to match the number of tickets selected.'.format(total_tickets))
            booking.delete()
            account.credit_left += booking.amount
            account.save()
            return redirect('home')

        # Create new Seat objects for each selected seat and save them to the database
        new_seats = []
        for seat_number in selected_seat_numbers:
            seat = Seat(seat_number=seat_number, is_available=False, film=film_id, screen=screen_id, user_id=user_id, show_time_id=showtime_id)
            seat.save()
            new_seats.append(seat)  

        # Create a new SeatSelection object for each selected seat and save it to the database
        for seat in new_seats:
            seat_selection = SeatSelection(seat=seat, booking=booking)
            seat_selection.save()

        # Create a new AccountStatement object for this transaction and save it to the database
        statement = AccountStatement.objects.create(
            user=request.user,
            statement_date=timezone.now().date(),
            film_name=booking.film.title,
            ticket_quantity=total_tickets,
            amount=booking.amount,
            credit_balance=account.credit_left,
            transaction_type='B'
        )

        # Redirect the user to the booking confirmation page
        return redirect('receipt', booking_id=booking.id)

    else:
        messages.error(request, 'Booking Failed')
        return redirect('home')

@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def view_monthly_statement_manager(request, account_id):
    account = Account.objects.get(pk=account_id)

    if request.method == "POST":
        selected_month = int(request.POST['selected_month'])
        month_name = calendar.month_name[selected_month]

        if account.student:
            user = account.student.user
        elif account.club_rep:
            user = account.club_rep.user

        monthly_statement = AccountStatement.objects.filter(user=user, statement_date__month=selected_month)
        return render(request, 'Booking_System/view_monthly_statement_manager.html', {'account': account, 'statement_list': monthly_statement, 'month': month_name})
    else:
        return render(request, 'Booking_System/view_monthly_statement_manager.html', {'account': account})

@user_passes_test_custom(is_club_rep, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def month_select(request):
    error = request.GET.get('error')
    if error == 'club_uniq_num':
        messages.error(request, 'Incorrect club representative number. Please try again.')
    if request.method == 'POST':
        selected_month = request.POST.get('selected_month')
        club_rep_num = request.POST.get('club_rep_num')
        if club_rep_num != request.user.username:
            return redirect('month_select' + '?error=club_uniq_num')
        else:
            return redirect('monthly_account_statement' + '?selected_month=' + selected_month)

    return render(request, 'Booking_System/month_select.html')

@user_passes_test_custom(is_club_rep, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def monthly_account_statement(request):
    if request.method == 'POST':
        selected_month = request.POST.get('selected_month')
        club_rep_num = request.GET.get('club_rep_num')
        statement_list = AccountStatement.objects.filter(user=request.user, statement_date__month=selected_month)
        month = datetime.strptime(selected_month, '%m').strftime('%B')
        return render(request, 'Booking_System/club_monthly.html', {'statement_list': statement_list, 'month': month})
    else:
        return redirect('month_select')

@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        try:
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            messages.info(request, 'Booking Cancelled Successfully.')
            return redirect('manage_booking')
        
        # Check if the user is the owner of the booking
        if request.user != booking.user:
            messages.error(request, 'You do not have permission to cancel this booking.')
            return redirect('manage_booking')

        is_seat_selection = request.POST.get('is_seat_selection', False) == 'True'
        if is_seat_selection:
            # Add the booking amount back to the user's account credit_left
            try:
                user_account = Account.objects.get(student__user=request.user)
                user_account.credit_left += booking.amount
                user_account.save()

                seat_selections = SeatSelection.objects.filter(booking=booking)
                total_tickets = seat_selections.count()

                amount = booking.amount

                # Create a Account Statement object and save it to the database
                statement = AccountStatement.objects.create(
                    user=request.user,
                    statement_date=timezone.now().date(),
                    film_name=booking.film.title,
                    ticket_quantity=total_tickets,
                    amount=amount,
                    credit_balance=user_account.credit_left,
                    transaction_type='C'
                )

            except Account.DoesNotExist:
                try:
                    user_account = Account.objects.get(club_rep__user=request.user)
                    user_account.credit_left += booking.amount
                    user_account.save()

                    seat_selections = SeatSelection.objects.filter(booking=booking)
                    total_tickets = seat_selections.count()

                    amount = booking.amount
                    
                    # Create a Account Statement object and save it to the database
                    statement = AccountStatement.objects.create(
                    user=request.user,
                    statement_date=timezone.now().date(),
                    film_name=booking.film.title,
                    ticket_quantity=total_tickets,
                    amount=amount,
                    credit_balance=user_account.credit_left,
                    transaction_type='C'
                    )
                    
                except Account.DoesNotExist:
                    user_account = None
                    messages.error(request, 'No Account Found For This User. Please Request an Account.')
                    return redirect('home')

        # Delete the associated SeatSelection and Seat objects
        seat_selections = SeatSelection.objects.filter(booking=booking)
        if seat_selections.exists():
            for seat_selection in seat_selections:
                seat = seat_selection.seat
                seat_selection.delete()
                seat.delete()

        # Delete the booking
        booking.delete()

        messages.success(request, 'Booking Cancelled Successfully.')
        return redirect('manage_booking')
    else:
        return redirect('manage_booking')

@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    seat_selections = SeatSelection.objects.filter(booking=booking)

    seats = [seat_selection.seat.seat_number for seat_selection in seat_selections]

    return render(request, 'Booking_System/receipt.html', {'booking': booking, 'seats': seats})

@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def manage_booking(request):
    # Get the user's bookings
    user_bookings = request.user.bookings.all()
    
    # Get the current time
    current_time = timezone.now()
    print(current_time)
    # Pass the user's bookings and the current time to the template context
    context = {'user_bookings': user_bookings, 'current_time': current_time}
    
    return render(request, "Booking_System/manage_booking.html", context)

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def manage_student_account(request):
    try:
        students = Student.objects.all().exclude(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'No student account recorded yet')
        return redirect('home')
    
    other_students = Student.objects.exclude(user=request.user)
    return render(request, "Booking_System/manage_student_account.html", {'students': other_students})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def edit_account(request, student_id):
    customuser = CustomUser.objects.get(id=student_id)

    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=customuser)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully')
            return redirect('manage_student_account')
    else:
        form = EditAccountForm(instance=customuser)
        context = {'form': form}
        return render(request, 'Booking_System/edit_account.html', context)

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def provide_discount(request,student_id):
    user = CustomUser.objects.get(id=student_id)
    student = Student.objects.get(user=user)
    student.has_discount = True
    student.save()
    messages.success(request, 'Discount allocated successfully')
    return redirect('manage_student_account')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def remove_discount(request,student_id):
    user = CustomUser.objects.get(id=student_id)
    student = Student.objects.get(user=user)
    student.has_discount = False
    student.save()
    messages.success(request, 'Removed discount successfully')
    return redirect('manage_student_account')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def delete_account(request, student_id):
    user = CustomUser.objects.get(id=student_id)
    student = Student.objects.get(user=user)
    student.delete()
    user.delete()
    messages.success(request, 'Account deleted successfully')
    return redirect('manage_student_account')

@login_required
@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
def edit_screen(request, screen_id):
    try:
        screens = Screen.objects.all()
        screen = Screen.objects.get(id=screen_id)

        if request.method == 'POST':
            form = EditScreenForm(request.POST, instance=screen)
            if form.is_valid():
                form.save()
                messages.success(request, 'Screen Updated Successfully')
                return redirect('manage_screen')
        else:
            form = EditScreenForm(instance=screen)
            context = {'form': form}

            return render(request, 'Booking_System/edit_screen.html', context)

    except Screen.DoesNotExist:
        messages.error(request, 'No Screen Recorded Yet')
        return redirect('home')

    return render(request, 'Booking_System/edit_screen.html', {'form': form})

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def edit_showing(request, showing_id):
    try:
        showings = ShowTime.objects.all()
        showing = ShowTime.objects.get(id=showing_id)

        if request.method == 'POST':
            form = EditShowingForm(request.POST, instance=showing)
            if form.is_valid():
                form.save()
                messages.success(request, 'Showing Updated Successfully')
                return redirect('manage_showing')
        else:
            form = EditShowingForm(instance=showing)
            context = {'form': form}

            return render(request, 'Booking_System/edit_showing.html', context)

    except Screen.DoesNotExist:
        messages.error(request, 'No Showing Recorded Yet')
        return redirect('home')

    return render(request, 'Booking_System/edit_showing.html', {'form': form})  

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def delete_screen(request, screen_id):
    screen = Screen.objects.get(id=screen_id)
    screen.delete()
    messages.success(request, 'Screen Deleted Successfully')
    return redirect('manage_screen')

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def delete_showing(request, showing_id):
    showing = ShowTime.objects.get(id=showing_id)
    film = showing.film
    film.now_showing = False
    film.save()
    showing.delete()
    messages.success(request, 'Showing Removed Successfully')
    return redirect('manage_showing')

@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def view_all_account(request):
    accounts = Account.objects.all()
    for account in accounts:
        if account.student:
            account.account_holder_name = f"{account.student.user.first_name} {account.student.user.last_name}"
        elif account.club_rep:
            account.account_holder_name = f"{account.club_rep.representative.first_name} {account.club_rep.representative.last_name}"
    return render(request, "Booking_System/view_all_account.html", {'accounts': accounts})

@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def account_statement(request, user_id):
    user = get_object_or_404(User, id=user_id)
    transactions = Transaction.objects.filter(account=user.account, timestamp__month=timezone.now().month-1)
    return render(request, 'Booking_System/account_statement.html', {'user': user, 'transactions': transactions})

@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def edit_account_statement(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    
    if request.method == 'POST':
        form = EditStatementAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account details updated successfully')
            return redirect('view_all_account')
        else:
            messages.error(request, 'Account details updated failed')
            return redirect('view_all_account')
    else:
        form = EditStatementAccountForm(instance=account)

    return render(request, 'Booking_System/edit_statement_account.html', {'form': form})

@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def topup(request):
    if request.method == 'POST':
        amount = int(request.POST.get('topup_amount'))
        account = request.user.get_account()

        # Check if the account exists
        if account is None:
            messages.error(request, "You do not have a statement account. Please contact the account manager and send a request.")
            return redirect('home')

        account.credit_left += amount
        account.save()
        
        topup = "Top Up"
        # Create a new AccountStatement object for this transaction and save it to the database
        statement = AccountStatement.objects.create(
            user=request.user,
            statement_date=timezone.now().date(),
            film_name=topup,
            ticket_quantity=0,
            amount=amount,
            credit_balance=account.credit_left,
            transaction_type='C'
        )

        messages.success(request, f"You've topped up £{amount}. Your new balance is £{account.credit_left}.")
        return redirect('home')
    else:
        amounts = [1, 5, 10, 50, 100]
        return render(request, 'Booking_System/payment.html', {'amounts': amounts})
   
@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def create_statement_account(request):
    if request.method == 'POST':
        form = CreateStatementAccountForm(user=request.user, data=request.POST)
        payment_form = PaymentForm(request.POST)

        account_title = request.POST.get('account_title')
        if Account.objects.filter(account_title=account_title).exists():
            messages.error(request, 'Account title already exists. Please choose a different title.')
            return redirect('create_statement_account')

        if form.is_valid() and payment_form.is_valid():
            account = form.save()
            account.user = request.user

            # Assign the club rep instance to the account
            if request.user.user_type == 4 and hasattr(request.user, 'club_rep'):
                account.club_rep = request.user.club_rep

            account.save()

            # Add account to the club rep's account list
            if account.student is not None:
                # Add account to the student's account list
                account.student.accounts.add(account)
            elif account.club_rep is not None:
                # Add account to the club rep's account list
                account.club_rep.accounts.add(account)

            payment = PaymentDetail(
                account=account,
                cardholder_name=payment_form.cleaned_data['cardholder_name'],
                card_number=payment_form.cleaned_data['card_number'],
                expiration_month=payment_form.cleaned_data['expiration_date'][:2],
                expiration_year=payment_form.cleaned_data['expiration_date'][-4:],
                cvv=payment_form.cleaned_data['cvv']
            )
            payment.save()
                
            # Do something with the newly created account object
            messages.success(request, 'Statement Account Created Successfully')

            return redirect('home')
    else:
        form = CreateStatementAccountForm(user=request.user)
        payment_form = PaymentForm()
    return render(request, 'Booking_System/create_statement_account.html', {'form': form, 'payment_form': payment_form})

@user_passes_test_custom(is_club_rep_or_student, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def request_statement_account(request):
    if request.method == 'POST':

        payment_form = PaymentForm(request.POST)

        if payment_form.is_valid():
            cardholder_name = payment_form.cleaned_data['cardholder_name']
            card_number = payment_form.cleaned_data['card_number']

            # Check if card number and card holder name combination already exists
            if StatementAccountRequest.objects.filter(cardholder_name=cardholder_name, card_number=card_number).exists():
                messages.error(request, "You already sent a request, Please wait for Approval.")
            else:
                account_request = StatementAccountRequest(
                    user=request.user,
                    cardholder_name=cardholder_name,
                    card_number=card_number,
                    expiration_month=payment_form.cleaned_data['expiration_date'][:2],
                    expiration_year=payment_form.cleaned_data['expiration_date'][-4:],
                    cvv=payment_form.cleaned_data['cvv']
                )
                account_request.save()

                messages.success(request, 'Statement Account Request Sent Successfully')

            return redirect('home')
        else:
            messages.error(request, 'Invalid Details, Please Try Again!')
            return redirect('request_statement_account')
    else:
        payment_form = PaymentForm()
    return render(request, 'Booking_System/request_statement_account.html', {'payment_form': payment_form})

@user_passes_test_custom(is_account_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def delete_statement_account(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    account.delete()
    messages.success(request, 'Account Deleted Successfully.')
    return redirect('view_all_account')  



def fetch_film_data(film_id, api_key):
    film_url = f'https://api.themoviedb.org/3/movie/{film_id}?api_key={api_key}&append_to_response=credits,release_dates'  
    response = requests.get(film_url) # Sends HTTP request to the API using the request library
    film_data = response.json() # Converts the JSON response from the TMDb API to a python dictionary

    # Getting the age rating (certification)
    certification = None
    for release in film_data['release_dates']['results']:
        if release['iso_3166_1'] == 'US':
            certification = release['release_dates'][0]['certification']
            break

    return {
        'title': film_data['title'],
        'release_date': film_data['release_date'],
        'overview': film_data['overview'],
        'rating': film_data['vote_average'],
        'poster_path': film_data['poster_path'],
        'director': film_data['credits']['crew'][0]['name'],
        'cast': [cast['name'] for cast in film_data['credits']['cast'][:5]],
        'age_rating': certification
    }

@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")
@login_required
def search_film(request):
    query = request.GET.get('query', '') # Retrieves the value of the query parameter from the search bar GET request
    api_key = '9ca66987cac35cb481faa3f84b01cf97'

    film = None
    if query:
        search_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}' # Constructs the api endpoint URL for searching films using the TMDb api
        response = requests.get(search_url) # Sends an HTTP request to the TMDb api using the request library 

        search_data = response.json() # Converts the JSON response from the TMDb api to a python dictionary
        search_results = search_data['results']

        if search_results:
            film_id = search_results[0]['id']
            film = fetch_film_data(film_id, api_key)

    context = {'film': film, 'query': query, 'film_id': film_id if film else None}
    return render(request, 'Booking_System/search_film.html', context)

        
@user_passes_test_custom(is_cinema_manager, login_url='home', message="You don't have permission to access the requested page.")   
@login_required
def add_film_api(request):
    film_id = request.POST.get('film_id') # Retrieves the value of the film id parameter from the POST request
    api_key = '9ca66987cac35cb481faa3f84b01cf97'  # API key required to make request to the TMDb API

    if film_id:
        film_data = fetch_film_data(film_id, api_key)

        # Check if film with the same title already exists in the database
        if Film.objects.filter(title=film_data['title']).exists():
            messages.error(request, 'A film with this title already exists.')
            return redirect('search_film')

        # Save the film's image to the image field
        response = requests.get(f'https://image.tmdb.org/t/p/w200{film_data["poster_path"]}')
        image_file = io.BytesIO(response.content)
        image_filename = f'{film_data["title"]}.jpg'
        film_image = InMemoryUploadedFile(
            image_file,
            None,
            image_filename,
            'image/jpeg',
            len(response.content),
            None
        )

        # Create new Film instance and save to database
        film = Film.objects.create(
            title=film_data['title'],
            release_date=datetime.strptime(film_data['release_date'], '%Y-%m-%d').date(),
            description=film_data['overview'],
            age_rating=film_data['age_rating'],
            image=film_image
        )

        # Add directors to the film
        director_names = [film_data['director']]
        directors = [Director.objects.get_or_create(name=name)[0] for name in director_names]
        film.directors.set(directors)

        # Add cast to the film
        cast_names = film_data['cast']
        cast = [Cast.objects.get_or_create(name=name)[0] for name in cast_names]
        film.cast.set(cast)

        messages.success(request, 'Film added successfully.')

    return redirect('search_film')


def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test_custom(is_superuser, login_url='home', message="You don't have permission to access the requested page.")
@user_passes_test(is_superuser)
def create_manager(request):
    if request.method == 'POST':
        form = ManagerUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Registered Successfully.')
            return redirect('home')
    else:
        form = ManagerUserCreationForm()

    return render(request, 'Booking_System/create_manager.html', {'form': form})    

    