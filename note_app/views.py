# users/views.py
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Note
from .serializers import NoteSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)



class NoteCreateView(generics.CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class NoteUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    # GET method for fetching the note's details
    def get(self, request, pk, format=None):
        try:
            note = Note.objects.get(pk=pk)
            # Ensure the user is the one who created the note
            if note.user != request.user:
                return Response({"detail": "You do not have permission to view this note."},
                                status=status.HTTP_403_FORBIDDEN)
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

    # PUT method for updating the note
    def put(self, request, pk, format=None):
        try:
            note = Note.objects.get(pk=pk)
            # Ensure the user is the one who created the note
            if note.user != request.user:
                return Response({"detail": "You do not have permission to update this note."},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = NoteSerializer(note, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Note.DoesNotExist:
            return Response({"detail": "Note not found."}, status=status.HTTP_404_NOT_FOUND)


class NoteDeleteView(generics.DestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



class NoteListView(generics.ListAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
