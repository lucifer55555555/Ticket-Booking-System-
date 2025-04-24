from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('events/', EventListView.as_view(), name='events'),
    path('book/<int:pk>/', BookTicketView.as_view(), name='book_ticket'),
    path('history/', BookingHistoryView.as_view(), name='history'),
    path('admin-panel/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/show/add/', AddEditShowView.as_view(), name='add_show'),
    path('admin/show/edit/<int:pk>/', AddEditShowView.as_view(), name='edit_show'),
    path('admin/show/delete/<int:pk>/', DeleteShowView.as_view(), name='delete_show'),
]
