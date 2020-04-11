from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from ranobe.views import RanobeList, RanobeDetailView, ChapterPageView, DetailChapterPage
from users.views import MainProfileView, CreateUserView, ProfileView, ShortUserView, BookmarkUpdateView, \
    BookmarkCheckView, BookStatusUpdateView, ProfileStatisticView, ProfileCommentsView, ProfileRanobesView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from comments.views import CommentView, CommentCreateView, UpdateDestroyCommentView

from ranobe.views import TagsView, GenresView
from blog.views import BlogListView, DetailBlogView

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'), permanent=True)),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    path('ranobe/', RanobeList.as_view()),
    url(r'^ranobe/(?P<pk>[0-9]+)/$', RanobeDetailView.as_view()),
    url(r'^ranobe/(?P<pk>[0-9]+)/bookmark/$', BookmarkUpdateView.as_view()),
    url(r'^ranobe/(?P<pk>[0-9]+)/readstatus/$', BookStatusUpdateView.as_view()),
    url(r'^ranobe/(?P<pk>[0-9]+)/chapters/', ChapterPageView.as_view()),
    url(r'^ranobe/chapters/read/(?P<chapter_id>[0-9]+)/$', DetailChapterPage.as_view()),
    path('user/register/', CreateUserView.as_view()),
    path('user/profile/', ProfileView.as_view()),
    path('user/profile/bookmark', BookmarkCheckView.as_view()),
    path('user/profile/statistic', ProfileStatisticView.as_view()),
    path('user/profile/comments', ProfileCommentsView.as_view()),
    path('user/profile/ranobes', ProfileRanobesView.as_view()),
    path('admin/', admin.site.urls),
    url(r'^ranobe/(?P<pk>[0-9]+)/comments/$', CommentView.as_view()),
    url(r'^ranobe/(?P<pk>[0-9]+)/comments/post/$', CommentCreateView.as_view()),
    url(r'^ranobe/(?P<pk>[0-9]+)/comments/(?P<comment_id>[0-9]+)/$', UpdateDestroyCommentView.as_view()),
    path('user/short/', ShortUserView.as_view()),
    path('tags/list/', TagsView.as_view()),
    path('genres/list/', GenresView.as_view()),
    path('blog/', BlogListView.as_view()),
    url(r'^blog/(?P<post_id>[0-9]+)/$', DetailBlogView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
