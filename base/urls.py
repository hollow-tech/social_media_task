from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, CustomLoginView, RegisterPage, AddLike, AddDislike, apiOverview, postCreate, postDelete, postDetail, postList, postUpdate
from django.contrib.auth.views import LogoutView


urlpatterns = [

	path('api/', apiOverview, name='api-overview'),
	path('api/post-list/', postList, name='post-list'),
	path('api/post-detail/<str:pk>/', postDetail, name='post-detail'),
	path('api/post-create/', postCreate, name='post-create'),
	path('api/post-update/<str:pk>/', postUpdate, name='post-update'),
	path('api/post-delete/<str:pk>/', postDelete, name='post-delete'),

	
	path('login/', CustomLoginView.as_view(), name='login'),
	path('logout', LogoutView.as_view(next_page='login'), name="logout"),
	path('register/', RegisterPage.as_view(), name="register"),
	
	path('', PostList.as_view(), name='posts'),
	path('post/<int:pk>/', PostDetail.as_view(), name='post'),
	path('post/<int:pk>/like', AddLike.as_view(), name='like'),
	path('post/<int:pk>/dislike', AddDislike.as_view(), name='dislike'),
	path('post-create/', PostCreate.as_view(), name='post-create'),
	path('post-update/<int:pk>/', PostUpdate.as_view(), name='post-update'),
	path('post-delete/<int:pk>/', PostDelete.as_view(), name='post-delete'),
]