from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import permissions, status, mixins, generics
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.serializer import CommentSerializer, ShortCommentSerializer
from .permission import ProfileOwnPermission
from .serializer import UserSerializer, ProfileSerializer, ShortUserSerializer, BookmarkSerializer, \
    UpdateBookmarkSerializer, ProfileBookmarkSerializer, BookStatusSerializer, BookReadingStatusSerializer, \
    UpdateBookReadingStatusSerializer
from .models import Profile, BookReadingStatus
from django.shortcuts import get_object_or_404
from comments.models import Comments

class MainProfileView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class ProfileStatisticView(generics.RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission,
    )

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        comments = Comments.objects.all().filter(author_id=request.user.id)
        last_comments = ShortCommentSerializer(comments[:5], data=request.data, many=True)
        planned_books = obj.read_status.filter(bookreadingstatus__choices="PL", bookreadingstatus__profile_id=obj.id)
        reading_books = obj.read_status.filter(bookreadingstatus__profile_id=obj.id, bookreadingstatus__choices="RDG")
        read_books = obj.read_status.filter(bookreadingstatus__profile_id=obj.id, bookreadingstatus__choices="RD")
        comments_amount = len(comments)
        read_books_amount = len(read_books)
        reading_books_amount = len(reading_books)
        planned_books_amount = len(planned_books)
        last_comments.is_valid(raise_exception=True)
        return Response({'comments-amount': comments_amount,
                         'last-comments': last_comments.data,
                         'planned_books_amount': planned_books_amount,
                         'reading_books_amount': reading_books_amount,
                         'read_books_amount': read_books_amount}, status=status.HTTP_200_OK)



class ProfileView(generics.RetrieveAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission,
    )
    serializer_class = ProfileSerializer

    def get_object(self):
        id_user = self.request.user.id
        obj = get_object_or_404(User, id=id_user)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ShortUserView(generics.RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission
    )
    serializer_class = ShortUserSerializer

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(User, username=user)
        return obj


class BookmarkCheckView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileBookmarkSerializer
    queryset = Profile.objects.all()


class BookmarkUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission,
    )
    serializer_class = BookmarkSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.bookmarked.get(id=kwargs['pk']):
                return Response({"bookmarked": True}, status=status.HTTP_200_OK)
            else:
                return Response({"bookmarked": False}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"bookmarked": False}, status=status.HTTP_200_OK)

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user = self.request.user
        instance.ranobe_id = (self.kwargs['pk'])
        instance.save()
        serializer = UpdateBookmarkSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def perform_destroy(self, instance):
        try:
            instance = self.get_object()
            instance.bookmarked.remove(self.kwargs['pk'])
            instance.save()
        except Http404:
            pass
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class BookStatusUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission,
    )
    serializer_class = BookReadingStatusSerializer

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        try:
            if obj.read_status.get(id=kwargs['pk']):
                read_status = BookReadingStatus.objects.get(profile__user=self.request.user,
                                                            ranobe=kwargs['pk']).choices
                return Response({"read_status": read_status}, status=status.HTTP_200_OK)
            else:
                return Response({"read_status": False}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"read_status": False}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        profile = self.get_object().id
        filter_exist = BookReadingStatus.objects.all().filter(ranobe_id=kwargs['pk'], profile_id=profile)
        if len(filter_exist) == 0:
            obj = BookReadingStatus(profile_id=profile,
                                    ranobe_id=kwargs['pk'],
                                    choices=request.data['choice'])
            obj.save()
            return Response({"result": True}, status=status.HTTP_202_ACCEPTED)
        # Additional check for double existing (may be cause not nice related model)
        elif len(filter_exist) == 1:
            obj = filter_exist.update(profile_id=profile,
                                      ranobe_id=kwargs['pk'],
                                      choices=request.data['choice'])
            print(obj)
            return Response({"result": True}, status=status.HTTP_202_ACCEPTED)
        elif len(filter_exist) > 1:
            filter_exist.delete()
            obj = BookReadingStatus(profile_id=profile,
                                    ranobe_id=kwargs['pk'],
                                    choices=request.data['choice'])
            obj.save()
            return Response({"result": True}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"result": False}, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        ranobe = kwargs['pk']
        profile_id = obj.id
        filter = BookReadingStatus.objects.filter(profile_id=profile_id, ranobe_id=ranobe)
        if len(filter) > 0:
            filter.delete()
            return Response({"result": True}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"result": False}, status=status.HTTP_204_NO_CONTENT)
