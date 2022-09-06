from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from .forms import NewTicketForm, UpdateTicketForm, SignupForm, RespondTicketForm, UpdateUserForm, NewUserForm
from .models import Ticket, CustomUser


def signup_request(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request, "signup.html", {"register_form": form})


def login_request(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request=request, template_name="login.html", context={"login_form": form})


@login_required
def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("/")


@login_required
def home_tickets(request):
    if request.user.is_authenticated:
        if request.user.role in [CustomUser.ADMIN_ROLE, CustomUser.REGULAR_ROLE]:
            tickets = Ticket.objects.all().order_by('-status', '-date_created')
        else:
            tickets = Ticket.objects.filter(customer=request.user)
        return render(request, 'home_tickets.html', {'tickets': tickets})
    else:
        return HttpResponseRedirect('/login')


@login_required
def create_ticket(request):
    form = NewTicketForm()
    if request.method == 'POST':
        form = NewTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.customer = request.user
            ticket.save()
            return HttpResponseRedirect('/')
    return render(request, 'new_ticket.html', {'form': form})


@login_required
def update_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, f"Ticket #{ticket.id} was successfully updated!")
            return HttpResponseRedirect('/')
        else:
            messages.error(request, f"An error occurred updating Ticket #{ticket.id}")
    else:
        form = UpdateTicketForm(instance=ticket)
    return render(request, 'new_ticket.html', {'form': form})


@login_required
def delete_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    ticket.delete()
    messages.success(request, f"Ticket #{id} was successfully deleted!")
    return redirect("/")


@login_required
def respond_ticket(request, id):
    ticket = Ticket.objects.get(id=id)
    if request.method == 'POST':
        form = RespondTicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            ticket.worker = request.user
            ticket.save()
            messages.success(request, f"Ticket #{ticket.id} responded successfully")
            return HttpResponseRedirect('/')
        else:
            messages.error(request, f"An error occurred responding to Ticket #{ticket.id}")
    else:
        form = RespondTicketForm(instance=ticket)
        if request.user.role == CustomUser.CUSTOMER_ROLE:
            form.fields['response'].widget.attrs['disabled'] = True

    return render(request, 'respond_ticket.html', {'form': form, 'ticket': ticket})


# Users CRUD
@login_required
def home_users(request):
    users = CustomUser.objects.all()
    return render(request, 'home_users.html', {'users': users})


@login_required
def create_user(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User #{user.id} created successfully!")
            return redirect("/home_users")
        else:
            messages.error(request, f"An error occurred creating the user")
    return render(request, "new_user.html", {"form": form})


@login_required
def update_user(request, id):
    user = CustomUser.objects.get(id=id)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User #{user.id} was successfully updated!")
            return HttpResponseRedirect('/home_users')
        else:
            messages.error(request, f"An error occurred updating user #{user.id}")
    else:
        form = UpdateUserForm(instance=user)
    return render(request, 'new_user.html', {'form': form})


@login_required
def delete_user(request, id):
    worker = CustomUser.objects.get(id=id)
    worker.delete()
    messages.success(request, f"Ticket #{id} was successfully deleted!")
    return redirect("/home_users")


@login_required
def download_ticket_files(request, id):
    ticket = Ticket.objects.get(id=id)
    return FileResponse(ticket.files, as_attachment=True)
