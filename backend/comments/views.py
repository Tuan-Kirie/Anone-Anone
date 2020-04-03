from rest_framework import generics, mixins, permissions, status, viewsets
from .serializer import CommentSerializer, CommentCreateSerializer, CommentUpdateDestroySerializer

from .models import Comments


# Create your views here.
class CommentView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Comments.objects.filter(ranobe_id=self.kwargs['pk'])
        return queryset


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comments.objects.all()


class UpdateDestroyCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentUpdateDestroySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comments.objects.all()
    lookup_url_kwarg = 'comment_id'



