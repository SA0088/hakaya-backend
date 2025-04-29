from django.urls import path
# import Home view from the views file
from .views import Home , Experience

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('/experience', Experience.as_view(), name='exp-index'),
]
