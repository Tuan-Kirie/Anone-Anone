from math import ceil

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, FieldError
from django.http import Http404
from rest_framework import permissions, status, mixins, generics
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView, ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from comments.serializer import CommentSerializer, ShortCommentSerializer, ProfileCommentSerializer
from ranobe.serializer import RanobeSerializer
from .permission import ProfileOwnPermission
from .serializer import UserSerializer, ProfileSerializer, ShortUserSerializer, BookmarkSerializer, \
    UpdateBookmarkSerializer, ProfileBookmarkSerializer, BookStatusSerializer, BookReadingStatusSerializer, \
    UpdateBookReadingStatusSerializer, BookreadingStatusProfileSerializer, AnotherProfileSerializer, \
    ProfileUpdateSerializer, ReadHistorySerializer, UserLikesSerializer
from .models import Profile, BookReadingStatus, ReadHistory, RanobeLikes
from django.shortcuts import get_object_or_404
from comments.models import Comments
from ranobe.models import Chapters, Ranobe
from django.forms.models import model_to_dict
from django.db.models import Sum


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

    # Deactivated comments list
    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        comments = Comments.objects.all().filter(author_id=request.user.id)
        # last_comments = ShortCommentSerializer(comments[:5], many=True)
        planned_books = obj.read_status.filter(bookreadingstatus__choices="PL", bookreadingstatus__profile_id=obj.id)
        reading_books = obj.read_status.filter(bookreadingstatus__profile_id=obj.id, bookreadingstatus__choices="RDG")
        read_books = obj.read_status.filter(bookreadingstatus__profile_id=obj.id, bookreadingstatus__choices="RD")
        comments_amount = len(comments)
        read_books_amount = len(read_books)
        reading_books_amount = len(reading_books)
        planned_books_amount = len(planned_books)
        return Response({'comments_amount': comments_amount,
                         # 'last_comments': last_comments.data,
                         'planned_books_amount': planned_books_amount,
                         'reading_books_amount': reading_books_amount,
                         'read_books_amount': read_books_amount}, status=status.HTTP_200_OK)


class ProfileCommentsView(generics.RetrieveAPIView):
    # Do not forget to add pagination
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission,
    )

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def retrieve(self, request, *args, **kwargs):
        comments = Comments.objects.all().filter(author_id=request.user.id)
        data = ProfileCommentSerializer(comments, many=True).data
        # bug with queryset if response serializer data without dict moustaches
        return Response({"comments": data}, status=status.HTTP_200_OK)


class ProfileRanobesView(generics.RetrieveAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission,
    )

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def retrieve(self, request, *args, **kwargs):
        # Need try for prevent key error
        try:
            if state := request.GET["Rtype"]:
                resp = self.get_object().read_status.filter(bookreadingstatus__choices=state)
                data = RanobeSerializer(resp, many=True).data
                return Response({"ranobes": data}, status=status.HTTP_200_OK)
            else:
                return Response({'ranobes': RanobeSerializer(self.get_object().read_status.all(), many=True).data},
                                status.HTTP_200_OK)
        except KeyError:
            return Response({'ranobes': RanobeSerializer(self.get_object().read_status.all(), many=True).data},
                            status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView, mixins.DestroyModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission,
    )
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        obj = get_object_or_404(User, id=user.id)
        return obj

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProfileUpdateView(UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, ProfileOwnPermission)
    serializer_class = ProfileUpdateSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        obj = get_object_or_404(Profile, user=self.request.user)
        return obj


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


class BookmarkCheckView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, ProfileOwnPermission)
    serializer_class = ProfileBookmarkSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        bookmarks = obj.bookmarked.all()
        response_data = RanobeSerializer(bookmarks, many=True)
        return Response(response_data.data, status=status.HTTP_200_OK)


class UserLikesView(generics.RetrieveAPIView, mixins.UpdateModelMixin):
    permission_classes = (permissions.IsAuthenticated, ProfileOwnPermission)
    serializer_class = UserLikesSerializer

    def get_object(self):
        try:
            like = RanobeLikes.objects.get(user=self.request.user, ranobe=self.kwargs['pk'])
            return like
        except RanobeLikes.DoesNotExist:
            return False
        except RanobeLikes.MultipleObjectsReturned:
            likes = RanobeLikes.objects.all().filter(user=self.request.user, ranobe=self.kwargs['pk'])
            [x.delete() for x in likes[:len(likes) - 1]]
            return self.get_object()

    def calculate_likes(self):
        likes_of_ranobe = RanobeLikes.objects.all().filter(ranobe_id=self.kwargs['pk'])
        return likes_of_ranobe.aggregate(Sum('like'))

    def retrieve(self, request, *args, **kwargs):
        like = self.get_object()
        if like is not False:
            return Response({'res': self.serializer_class(like, many=False).data,
                             'all': self.calculate_likes()}, status=status.HTTP_200_OK)
        else:
            return Response({'resp': False,
                             'all': self.calculate_likes()})

    def post(self, request, *args, **kwargs):
        like = self.get_object()
        sent_like = RanobeLikes.LIKE if request.data['like'] == str(1) else RanobeLikes.UNLIKE
        print(sent_like)
        if like is False:
            RanobeLikes.objects.create(user=request.user,
                                       ranobe=Ranobe.objects.get(id=self.kwargs['pk']),
                                       like=sent_like)
            like = self.get_object()
            return Response({'res': self.serializer_class(like, many=False).data}, status=status.HTTP_201_CREATED)
        else:
            like.like = sent_like
            like.save()
            return Response({'res': self.serializer_class(like, many=False).data}, status=status.HTTP_201_CREATED)



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


class ControlReadHistoryView(generics.RetrieveAPIView, mixins.CreateModelMixin):
    permission_classes = (
        permissions.IsAuthenticated,
        ProfileOwnPermission
    )
    serializer_class = ReadHistorySerializer

    def get_object(self):
        try:
            obj = ReadHistory.objects.get(
                user=self.request.user,
                ranobe_chapter__ranobe__id=self.kwargs['pk']
            )
            return obj
        except ReadHistory.MultipleObjectsReturned:
            _objects = ReadHistory.objects.all().filter(
                user=self.request.user,
                ranobe_chapter__ranobe__id=self.kwargs['pk']
            )
            [x.delete() for x in _objects[1:]]
            return self.get_object()
        except ReadHistory.DoesNotExist:
            return None

    def get_page_of_chapter(self):
        """
        Checking existing page of required chapter
        :return: page number int  > 0
        """
        chapters_count = [x.id for x in Chapters.objects.all().filter(ranobe_id=self.kwargs['pk'])]
        l_chapters_count = len(chapters_count)
        if l_chapters_count > 100:
            position_of_required_chapter = chapters_count.index(self.get_object().ranobe_chapter.id)
            return ceil(position_of_required_chapter / 100)
        else:
            return 1

    def retrieve(self, request, *args, **kwargs):
        resp = self.get_object()
        if resp is not None:
            return Response({'res': self.serializer_class(resp, many=False).data, 'page': self.get_page_of_chapter()},
                            status=status.HTTP_200_OK)
        else:
            return Response({"res": False})

    def post(self, request, *args, **kwargs):
        exist_obj = self.get_object()
        if exist_obj is None:
            obj = ReadHistory(user=request.user,
                              ranobe_chapter=Chapters.objects.get(id=request.data['chapter_id']))
            obj.save()
            resp = self.get_object()
            return Response({'res': self.serializer_class(resp, many=False).data}, status=status.HTTP_201_CREATED)
        else:
            exist_obj.ranobe_chapter = Chapters.objects.get(id=request.data['chapter_id'])
            exist_obj.save()
            resp = self.get_object()
            return Response({'res': self.serializer_class(resp, many=False).data}, status=status.HTTP_201_CREATED)


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
        elif len(filter_exist) == 1:
            obj = filter_exist.update(profile_id=profile,
                                      ranobe_id=kwargs['pk'],
                                      choices=request.data['choice'])
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
        data = BookReadingStatus.objects.filter(profile_id=profile_id, ranobe_id=ranobe)
        if len(data) > 0:
            data.delete()
            return Response({"result": True}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"result": False}, status=status.HTTP_204_NO_CONTENT)


class AnotherUserView(generics.RetrieveAPIView):
    permission_classes = (
        permissions.BasePermission,
    )
    serializer_class = AnotherProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        obj = get_object_or_404(User, id=kwargs['user_id'])
        user_data = self.serializer_class(obj, many=False, read_only=True)

        return Response({'user': user_data.data}, status=status.HTTP_200_OK)


class AnotherUserMarkedRanobesView(ProfileRanobesView):
    permission_classes = (
        permissions.BasePermission,
    )

    def get_object(self):
        obj = get_object_or_404(Profile, user__id=self.kwargs['user_id'])
        return obj
