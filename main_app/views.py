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

from .models import Category, Experience, Review
from .serializers import (
    CategorySerializer,
    ExperienceSerializer,
    ExperienceCreateSerializer,
    ReviewSerializer,
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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class ExperienceIndex(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            queryset = Experience.objects.all()
            # queryset = Experience.objects.filter(creator=request.user)
            serializer = ExperienceSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as err:
            print(err)
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
    permission_classes = [IsAuthenticated]

    def get(self, request, exp_id):
        try:
            experience = get_object_or_404(Experience, id=exp_id)
            serializer = ExperienceSerializer(experience)
            return Response(serializer.data)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikeExperienceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        message, likes = experience.toggle_like(request.user)
        return Response({
            'message': message,
            'likes_count': likes
        })


class CreateReviewAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def post(self, request, exp_id):
        try:
            serializer = self.serializer_class(data=request.data)
            # if not serializer.is_valid():
            #     print(serializer.errors)
            #     return Response(serializer.errors, status=400)
            
            if serializer.is_valid():
                exp = Experience.objects.get(id=exp_id)
                print("checking the experience object", exp)
                serializer.save(experience=exp, user=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err:
            print(str(err))
            return Response({"error": err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LikeReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
