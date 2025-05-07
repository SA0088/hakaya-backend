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
from rest_framework.decorators import api_view, permission_classes

from .models import Category, Experience, Review
from .serializers import (
    CategorySerializer,
    ExperienceSerializer,
    ExperienceCreateSerializer,
    ReviewSerializer,
    UserSerializer,
    CategoryWithExperiencesSerializer
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

# class UserProfileView(APIView):
#     permission_classes = [IsAuthenticated]  # التأكد من أن المستخدم مسجل دخوله

#     def get(self, request):
#         try:
#             # الحصول على المستخدم بناءً على الجلسة الحالية
#             user = request.user
#             # تسلسل بيانات المستخدم باستخدام UserSerializer
#             serializer = UserSerializer(user)
#             return Response(serializer.data)
#         except Exception as err:
#             return Response({'error': str(err)}, status=500)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Serialize user data
        user_data = UserSerializer(user).data

        # Experiences created by the user
        created_experiences = Experience.objects.filter(creator=user)
        created_data = ExperienceSerializer(created_experiences, many=True).data

        # Experiences liked by the user (correct field used here)
        liked_experiences = Experience.objects.filter(liked_by=user)
        liked_data = ExperienceSerializer(liked_experiences, many=True).data

        return Response({
            'user': user_data,
            'created_experiences': created_data,
            'liked_experiences': liked_data
        })
    # def delete(self, request, *args, **kwargs):
    #     experience = self.get_object()
    #     if experience.owner != request.user:
    #         return Response({"error": "You do not have permission to delete this experience."}, status=403)
    #     return super().delete(request, *args, **kwargs)


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
            print(serializer.data)
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
    def delete(self, request, exp_id):
        try:
            exp = get_object_or_404(Experience, id=exp_id)
            exp.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def put(self, request, exp_id):
        try:
            experience = get_object_or_404(Experience, id=exp_id)

            # تحقق من أن المستخدم هو المنشئ
            if experience.creator != request.user:
                return Response({"error": "You do not have permission to update this experience."}, status=403)

            serializer = ExperienceCreateSerializer(experience, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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


# class CreateReviewAPIView(CreateAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthenticated]

#     # def perform_create(self, serializer):
#     #     serializer.save(user=self.request.user)

#     def post(self, request, exp_id):
#         try:
#             serializer = self.serializer_class(data=request.data)
#             # if not serializer.is_valid():
#             #     print(serializer.errors)
#             #     return Response(serializer.errors, status=400)
            
#             if serializer.is_valid():
#                 exp = Experience.objects.get(id=exp_id)
#                 print("checking the experience object", exp)
#                 serializer.save(experience=exp, user=request.user)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as err:
#             print(str(err))
#             return Response({"error": err}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateReviewAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # نحصل على الـ experience بناءً على الـ exp_id من الـ URL
        exp = Experience.objects.get(id=self.kwargs['exp_id'])
        print(exp)
        # نقوم بحفظ المراجعة مع ربط الـ user الحالي بـ request.user
        serializer.save(experience=exp, user=self.request.user)
        print(serializer.errors)

    def post(self, request, *args, **kwargs):
        try:
            # نقوم بمعالجة البيانات باستخدام perform_create
            return super().post(request, *args, **kwargs)
        except Experience.DoesNotExist:
            return Response({"error": "Experience not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print(str(err))
            return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
class CategoryWithExperiencesView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoryWithExperiencesSerializer(category)
        return Response(serializer.data)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def liked_experiences(request):
    user = request.user
    liked = user.liked_experiences.all()  # تأكد من وجود العلاقة
    data = [{'id': exp.id, 'title': exp.title, 'summary': exp.summary} for exp in liked]
    return Response(data)