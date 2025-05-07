from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Category, Experience, Review

class ExperienceAppModelsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
        self.category = Category.objects.create(
            name='Adventure',
            description='Exciting outdoor adventures',
            photo='adventure.jpg'
        )
        
        self.experience = Experience.objects.create(
            title='Skydiving',
            summary='Jumping from a plane',
            image_path='skydiving.jpg',
            category=self.category,
            creator=self.user1
        )
        
        self.review = Review.objects.create(
            experience=self.experience,
            user=self.user2,
            comment='Amazing!',
            rate=5
        )
        
        self.experience.liked_by.add(self.user2)
        self.review.liked_by.add(self.user1)

    # --------- Model Creation ---------
    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Adventure')

    def test_experience_creation(self):
        self.assertEqual(str(self.experience), 'Skydiving')

    def test_review_creation(self):
        self.assertEqual(str(self.review), 'Review for Skydiving by user2')

    # --------- Likes Count ---------
    def test_experience_likes_count(self):
        self.assertEqual(self.experience.likes_count, 1)

    def test_review_likes_count(self):
        self.assertEqual(self.review.likes_count, 1)

    # --------- Toggle Like ---------
    def test_toggle_like_experience(self):
        msg, count = self.experience.toggle_like(self.user2)
        self.assertEqual(msg, 'Like removed')
        self.assertEqual(count, 0)
        msg, count = self.experience.toggle_like(self.user2)
        self.assertEqual(msg, 'Experience liked')
        self.assertEqual(count, 1)

    def test_toggle_like_review(self):
        msg, count = self.review.toggle_like(self.user1)
        self.assertEqual(msg, 'Like removed')
        self.assertEqual(count, 0)
        msg, count = self.review.toggle_like(self.user1)
        self.assertEqual(msg, 'Review liked')
        self.assertEqual(count, 1)

    # --------- Cascade Delete ---------
    def test_deleting_user_deletes_experience(self):
        self.assertEqual(Experience.objects.count(), 1)
        self.user1.delete()
        self.assertEqual(Experience.objects.count(), 0)

    def test_deleting_category_deletes_experience(self):
        self.assertEqual(Experience.objects.count(), 1)
        self.category.delete()
        self.assertEqual(Experience.objects.count(), 0)
