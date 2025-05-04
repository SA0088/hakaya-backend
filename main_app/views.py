
# # class Home(APIView):
# #   def get(self, request):
# #     content = [
# #                 {
# #                     "name": "Adventure",
# #                     "description": "Thrilling outdoor and travel experiences full of excitement and discovery."
# #                 },
# #                 {
# #                     "name": "Cooking",
# #                     "description": "Delicious homemade recipes and personal kitchen adventures."
# #                 },
# #                 {
# #                     "name": "Culture",
# #                     "description": "Traditions, arts, and celebrations from around the world."
# #                 },
# #                 {
# #                     "name": "Learning",
# #                     "description": "Experiences about gaining knowledge, courses, and workshops."
# #                 },
# #                 {
# #                     "name": "Volunteering",
# #                     "description": "Heartwarming stories of giving back to communities."
# #                 }
# #                 ]
# #     return Response(content)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics , status , permissions
# from .models import Category, Experience, Review 
# from .serializers import CategorySerializer, ExperienceCreateSerializer, ReviewCreateSerializer, ExperienceSerializer, UserSerializer
# from django.shortcuts import get_object_or_404
# from rest_framework.generics import CreateAPIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from django.contrib.auth.models import User


# class CreateUserView(generics.CreateAPIView):
#   queryset = User.objects.all()
#   serializer_class = UserSerializer

#   def create(self, request, *args, **kwargs):
#     try:
#       response = super().create(request, *args, **kwargs)
#       user = User.objects.get(username=response.data['username'])
#       refresh = RefreshToken.for_user(user)
#       content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
#       return Response(content, status=status.HTTP_201_CREATED)
#     except Exception as err:
#       return Response({ 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# class VerifyUserView(APIView):
#   permission_classes = [permissions.IsAuthenticated]

#   def get(self, request):
#     try:
#       user = User.objects.get(username=request.user.username)
#       try:
#         refresh = RefreshToken.for_user(user)
#         return Response({'refresh': str(refresh),'access': str(refresh.access_token),'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
#       except Exception as token_error:
#         return Response({"detail": "Failed to generate token.", "error": str(token_error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#     except Exception as err:
#       return Response({"detail": "Unexpected error occurred.", "error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# class LoginView(APIView):

#   def post(self, request):
#     try:
#       username = request.data.get('username')
#       password = request.data.get('password')
#       user = authenticate(username=username, password=password)
#       if user:
#         refresh = RefreshToken.for_user(user)
#         content = {'refresh': str(refresh), 'access': str(refresh.access_token),'user': UserSerializer(user).data}
#         return Response(content, status=status.HTTP_200_OK)
#       return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     except Exception as err:
#       return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class CategoryListView(APIView):
#     permission_classes = [IsAuthenticated]  # إذا كنت تريد التحقق من المصادقة

#     def get(self, request):
#         categories = Category.objects.all()  # استرجاع جميع الفئات من قاعدة البيانات
#         serializer = CategorySerializer(categories, many=True)  # تسلسل الفئات
#         return Response(serializer.data)

# # class ExperienceList(APIView):
# #     def get(self, request):
# #         experiences = Experience.objects.all()  # جلب جميع التجارب
# #         experience_data = [{"id": exp.id, "title": exp.title, "summary": exp.summary, "likes_count": exp.likes_count()} for exp in experiences]
# #         return Response(experience_data)

# class ExperienceIndex(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = ExperienceSerializer

#     def get(self, request):
#         try:
#             queryset = Experience.objects.filter(user=request.user)
#             serializer = ExperienceSerializer(queryset, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as err:
#             return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = self.serializer_class(data=request.data, context={'request': request})
#             if serializer.is_valid():
#                 serializer.save(user_id=request.user.id)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as err:
#             return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class CreateExperienceAPIView(CreateAPIView):
#     queryset = Experience.objects.all()
#     serializer_class = ExperienceCreateSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, serializer):
#         serializer.save(creator=self.request.user)

#     # def post(self, request, *args, **kwargs):
#     # try:
#     #   serializer = self.serializer_class(data=request.data)
#     #   if serializer.is_valid():
#     #     serializer.save()
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # except Exception as err:
#     #   return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# class LikeExperienceAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         experience = get_object_or_404(Experience, pk=pk)
#         user = request.user

#         if user in experience.liked_by.all():
#             experience.liked_by.remove(user)
#             message = "Like removed."
#         else:
#             experience.liked_by.add(user)
#             message = "Experience liked."

#         return Response({
#             "message": message,
#             "likes_count": experience.likes_count()
#         }, status=status.HTTP_200_OK)

# class CreateReviewAPIView(CreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewCreateSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class LikeReviewAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, request, pk):
#         review = get_object_or_404(Review, pk=pk)
#         user = request.user

#         if user in review.liked_by.all():
#             review.liked_by.remove(user)
#             message = "Like removed."
#         else:
#             review.liked_by.add(user)
#             message = "Review liked."

#         return Response({
#             "message": message,
#             "likes_count": review.likes_count()
#         }, status=status.HTTP_200_OK)

# class ExperienceDetail(APIView):
#   serializer_class = ExperienceSerializer
#   lookup_field = 'id'

#   def get(self, request, exp_id):
#     try:
#         queryset = Experience.objects.get(id=exp_id)
#         exp = ExperienceSerializer(queryset)
#         return Response(exp.data, status=status.HTTP_200_OK)
#     except Exception as err:
#         return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .serializers import *
# from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes

from .models import Category, Experience, Review
from .serializers import (
    CategorySerializer,
    ExperienceSerializer,
    ExperienceCreateSerializer,
    ReviewCreateSerializer,
    UserSerializer
)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def user_profile(request):
#     serializer = UserSerializer(request.user)
#     return Response(serializer.data) 

class Home(APIView):
  def get(self, request):
    content = {'message': 'Welcome to the Hakaya api home route!'}
    return Response(content)

class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    try:
      response = super().create(request, *args, **kwargs)
      user = User.objects.get(username=response.data['username'])
      refresh = RefreshToken.for_user(user)
      content = {'refresh': str(refresh), 'access': str(refresh.access_token), 'user': response.data }
      return Response(content, status=status.HTTP_201_CREATED)
    except Exception as err:
      return Response({ 'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyUserView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            # TODO: Generate token and send reset link
            send_mail(
                "Reset your password",
                "Click the link to reset your password...",
                "no-reply@hakaya.com",
                [email],
                fail_silently=False,
            )
            return Response({"message": "Email sent"})
        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=404)

class CategoryListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ExperienceIndex(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            queryset = Experience.objects.filter(creator=request.user)
            serializer = ExperienceSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ExperienceCreateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print(err)
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateExperienceAPIView(CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        
class ExperienceDetail(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, exp_id):
        try:
            experience = get_object_or_404(Experience, id=exp_id)
            serializer = ExperienceSerializer(experience)
            return Response(serializer.data)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikeExperienceAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        message, likes = experience.toggle_like(request.user)
        return Response({
            'message': message,
            'likes_count': likes
        })


class CreateReviewAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeReviewAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        user = request.user
        if user in review.liked_by.all():
            review.liked_by.remove(user)
            message = "Like removed."
        else:
            review.liked_by.add(user)
            message = "Review liked."
        return Response({
            "message": message,
            "likes_count": review.likes_count
        })
