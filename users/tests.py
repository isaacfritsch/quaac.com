from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        name = 'Test Name Test'        
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name            
        )

        self.assertEqual(user.email, email)  
        self.assertEqual(user.name, name)       
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123', 'Test Name Test') # noqa
            self.assertEqual(user.email, expected)
    
    def test_create_user_with_invalid_name_raises_error(self):
        """Test creating a user with an invalid name raises a ValidationError."""        
        invalid_names = ['Test123', '123Test', 'Test@Name Test@Name', 'Test Name123']
        
        for name in invalid_names:
            with self.assertRaises(ValidationError):
                get_user_model().objects.create_user('test1@example.com', 'sample123', name)            

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123', 'Test Name Test')
            
    def test_new_user_without_name_raises_error(self):
        """Test that creating a user without an name raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('test1@example.com', 'test123', '')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',            
            'test123',
            'Test Name Test',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)