from django.urls import path

from .serializers import NoteUpdateView
from .views import RegisterView, LoginView, LogoutView, NoteCreateView, NoteDeleteView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', NoteCreateView.as_view(), name='note-create'),
    path('update/<int:pk>/', NoteUpdateView.as_view(), name='note-update'),
    path('delete/<int:pk>/', NoteDeleteView.as_view(), name='note-delete'),
]