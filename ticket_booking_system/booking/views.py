from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Show, Booking
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
    def get(self, request):
        return render(request, 'booking/home.html')

class RegisterView(View):
    def get(self, request):
        return render(request, 'booking/register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'booking/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('events')
        return render(request, 'booking/login.html', {'error': 'Invalid credentials'})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class EventListView(LoginRequiredMixin, View):
    def get(self, request):
        shows = Show.objects.all()
        return render(request, 'booking/events.html', {'shows': shows})
class BookTicketView(LoginRequiredMixin, View):
    def get(self, request, pk):
        show = Show.objects.get(pk=pk)
        return render(request, 'booking/book_ticket.html', {'show': show})

    def post(self, request, pk):
        show = Show.objects.get(pk=pk)
        seats = int(request.POST['seats'])

        if show.available_seats >= seats:
            Booking.objects.create(user=request.user, show=show, seats=seats)
            show.available_seats -= seats
            show.save()
            return redirect('history')
        else:
            return render(request, 'booking/book_ticket.html', {
                'show': show,
                'error': 'Not enough seats available.'
            })
class BookingHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        bookings = Booking.objects.filter(user=request.user).select_related('show')
        return render(request, 'booking/history.html', {'bookings': bookings})
class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('home')
        shows = Show.objects.all()
        return render(request, 'booking/admin_dashboard.html', {'shows': shows})

class AddEditShowView(LoginRequiredMixin, View):
    def get(self, request, pk=None):
        if not request.user.is_staff:
            return redirect('home')
        show = Show.objects.get(pk=pk) if pk else None
        return render(request, 'booking/add_edit_show.html', {'show': show})

    def post(self, request, pk=None):
        title = request.POST['title']
        desc = request.POST['description']
        date = request.POST['date']
        seats = request.POST['available_seats']
        if pk:
            show = Show.objects.get(pk=pk)
            show.title = title
            show.description = desc
            show.date = date
            show.available_seats = seats
            show.save()
        else:
            Show.objects.create(title=title, description=desc, date=date, available_seats=seats)
        return redirect('admin_dashboard')

class DeleteShowView(LoginRequiredMixin, View):
    def get(self, request, pk):
        if not request.user.is_staff:
            return redirect('home')
        Show.objects.get(pk=pk).delete()
        return redirect('admin_dashboard')
