from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Experience, Review

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ['id', 'username', 'email' , 'password']  # تم تعديل الحقول لتكون أكثر توافقًا مع نموذج المستخدم الافتراضي

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  
        )
      
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'photo', 'name', 'description']

class ExperienceSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    liked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True, source='likes')  # العودة إلى PrimaryKeyRelatedField كما كان

    class Meta:
        model = Experience
        fields = [
            'id', 'title', 'summary', 'image_path', 'category',
            'creator', 'likes_count', 'liked_by', 'created_at'
        ]

class ExperienceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['title', 'summary', 'category', 'image_path']  

    def create(self, validated_data):
        user = self.context['request'].user
        experience = Experience.objects.create(creator=user, **validated_data)
        return experience

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    experience = serializers.PrimaryKeyRelatedField(queryset=Experience.objects.all())
    likes_count = serializers.IntegerField(read_only=True)
    liked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'experience', 'user', 'comment',
            'likes_count', 'liked_by', 'created_at'
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'experience', 'comment']  # لا نطلب user لأنه يؤخذ من request.user

    def create(self, validated_data):
        user = self.context['request'].user
        experience = validated_data['experience']
        if not Experience.objects.filter(id=experience.id).exists():
            raise serializers.ValidationError("Experience not found")
        return Review.objects.create(user=user, **validated_data)
