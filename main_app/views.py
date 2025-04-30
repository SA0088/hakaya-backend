
# class Home(APIView):
#   def get(self, request):
#     content = [
#                 {
#                     "name": "Adventure",
#                     "description": "Thrilling outdoor and travel experiences full of excitement and discovery."
#                 },
#                 {
#                     "name": "Cooking",
#                     "description": "Delicious homemade recipes and personal kitchen adventures."
#                 },
#                 {
#                     "name": "Culture",
#                     "description": "Traditions, arts, and celebrations from around the world."
#                 },
#                 {
#                     "name": "Learning",
#                     "description": "Experiences about gaining knowledge, courses, and workshops."
#                 },
#                 {
#                     "name": "Volunteering",
#                     "description": "Heartwarming stories of giving back to communities."
#                 }
#                 ]
#     return Response(content)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Category, Experience, Review
from .serializers import CategorySerializer, ExperienceCreateSerializer, ReviewCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView

# عرض الفئات
class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]  # إذا كنت تريد التحقق من المصادقة

    def get(self, request):
        categories = Category.objects.all()  # استرجاع جميع الفئات من قاعدة البيانات
        serializer = CategorySerializer(categories, many=True)  # تسلسل الفئات
        return Response(serializer.data)

# عرض التجارب
class ExperienceList(APIView):
    def get(self, request):
        experiences = Experience.objects.all()  # جلب جميع التجارب
        experience_data = [{"id": exp.id, "title": exp.title, "summary": exp.summary, "likes_count": exp.likes_count()} for exp in experiences]
        return Response(experience_data)

# إنشاء تجربة جديدة
class CreateExperienceAPIView(CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # نستخدم perform_create لتخصيص الـ creator بالـ user الحالي
        serializer.save(creator=self.request.user)

# إضافة أو إزالة الإعجاب لتجربة معينة
class LikeExperienceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk)
        user = request.user

        if user in experience.liked_by.all():
            experience.liked_by.remove(user)
            message = "Like removed."
        else:
            experience.liked_by.add(user)
            message = "Experience liked."

        return Response({
            "message": message,
            "likes_count": experience.likes_count()
        }, status=status.HTTP_200_OK)

# إنشاء مراجعة جديدة
class CreateReviewAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# إضافة أو إزالة الإعجاب لمراجعة معينة
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
            "likes_count": review.likes_count()
        }, status=status.HTTP_200_OK)
