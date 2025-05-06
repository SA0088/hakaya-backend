
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    # path('admin/', admin.site.urls),

    # Auth
    path('users/signup/', views.CreateUserView.as_view(), name='signup'),
    path('users/login/', views.LoginView.as_view(), name='login'),
    path('users/token/refresh/', views.VerifyUserView.as_view(), name='token_refresh'),
    # path('users/profile/', views.user_profile, name='user-profile'),


    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),

    # Experiences
    path('experiences/', ExperienceIndex.as_view(), name='experience-list-create'),
    path('experiences/new/', CreateExperienceAPIView.as_view(), name='experience-create'),
    path('experiences/<int:exp_id>/', ExperienceDetail.as_view(), name='experience-detail'),
    path('experiences/<int:pk>/like/', LikeExperienceAPIView.as_view(), name='experience-like'),

    # Reviews
    path('experiences/<int:exp_id>/reviews/', CreateReviewAPIView.as_view(), name='review-create'),
    path('reviews/<int:pk>/like/', LikeReviewAPIView.as_view(), name='review-like'),
]

