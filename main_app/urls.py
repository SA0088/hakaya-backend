from django.urls import path
from .views import ExperienceList, CreateExperienceAPIView, LikeExperienceAPIView, CategoryListView, LikeReviewAPIView, CreateReviewAPIView

urlpatterns = [
    path('experience/', ExperienceList.as_view(), name='exp-index'),
    path('experiences/create/', CreateExperienceAPIView.as_view(), name='create-experience'),
    path('experiences/<int:pk>/like/', LikeExperienceAPIView.as_view(), name='like-experience'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('reviews/create/', CreateReviewAPIView.as_view(), name='create-review'),
    path('reviews/<int:pk>/like-toggle/', LikeReviewAPIView.as_view(), name='like-review'),
]
