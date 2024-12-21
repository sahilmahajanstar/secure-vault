# Create your tests here.
from django.test import TestCase
from .models.users import Users


class UserModelTests(TestCase):
    def setUp(self):
        self.user = Users.objects.create(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )

    def test_user_creation(self):
        """Test that a user can be created with the expected attributes"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")

    def test_string_representation(self):
        """Test the string representation of the User model"""
        self.assertEqual(str(self.user), "testuser")

    def test_unique_constraints(self):
        """Test that username and email must be unique"""
        with self.assertRaises(Exception):
            Users.objects.create(
                username="testuser",  # Duplicate username
                email="another@example.com",
                password="testpass123",
            )

        with self.assertRaises(Exception):
            Users.objects.create(
                username="anotheruser",
                email="test@example.com",  # Duplicate email
                password="testpass123",
            )
