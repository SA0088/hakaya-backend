from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Define the home view
class Home(APIView):
  def get(self, request):
    content = [
                {
                    "name": "Adventure",
                    "description": "Thrilling outdoor and travel experiences full of excitement and discovery."
                },
                {
                    "name": "Cooking",
                    "description": "Delicious homemade recipes and personal kitchen adventures."
                },
                {
                    "name": "Culture",
                    "description": "Traditions, arts, and celebrations from around the world."
                },
                {
                    "name": "Learning",
                    "description": "Experiences about gaining knowledge, courses, and workshops."
                },
                {
                    "name": "Volunteering",
                    "description": "Heartwarming stories of giving back to communities."
                }
                ]
    return Response(content)
  
class Experience(APIView):
  def get(self, request):
    print("should be hitting api view")
    content = [
  {
    "title": "Skydiving in Dubai",
    "summary": "My first skydiving experience over the Palm Jumeirah! Absolutely breathtaking.",
    "image_path": "experiences/skydiving.jpg",
    "category": "Adventure",
    "creator_id": 1,
    "likes_count": 12,
    "created_at": "2025-04-29T10:00:00Z"
  },
  {
    "title": "Grandma's Traditional Maqluba",
    "summary": "I cooked my grandmother's famous Maqluba recipe and shared it with friends — turned out delicious!",
    "image_path": "experiences/maqluba.jpg",
    "category": "Cooking",
    "creator_id": 2,
    "likes_count": 8,
    "created_at": "2025-04-28T15:45:00Z"
  },
  {
    "title": "Lantern Festival in Chiang Mai",
    "summary": "Witnessed thousands of lanterns lighting up the sky in Thailand's annual celebration.",
    "image_path": "experiences/lantern.jpg",
    "category": "Culture",
    "creator_id": 3,
    "likes_count": 20,
    "created_at": "2025-04-27T19:30:00Z"
  },
  {
    "title": "Learning Sign Language",
    "summary": "I joined a course to learn basic sign language. It's a beautiful and essential way to communicate.",
    "image_path": "experiences/sign_language.jpg",
    "category": "Learning",
    "creator_id": 4,
    "likes_count": 5,
    "created_at": "2025-04-26T13:20:00Z"
  },
  {
    "title": "Planting Trees with Local School",
    "summary": "Spent the weekend helping students plant trees in our neighborhood. Inspiring and fun!",
    "image_path": "experiences/tree_planting.jpg",
    "category": "Volunteering",
    "creator_id": 5,
    "likes_count": 15,
    "created_at": "2025-04-25T08:10:00Z"
  }
]

    return Response(content)