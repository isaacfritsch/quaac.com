from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .views import user_register, user_login
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm, CustomAuthenticationForm


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
        
        
class UserRegistrationTestCase(TestCase):
    def test_user_registration_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Test registration with valid data
        data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'password1': 'password123',
            'password2': 'password123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)  

        # Test registration with invalid data
        invalid_data = {
            'email': 'invalid-email',
            'name': '',
            'password1': 'short',
            'password2': 'different',
        }
        response = self.client.post(reverse('register'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Stays on the registration page

class UserLoginTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            name='Test User',
            password='password123',
        )

    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # Test login with valid data
        data = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 204)  

        # Test login with invalid data
        invalid_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }
        response = self.client.post(reverse('login'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Stays on the login page

class CustomUserCreationFormTestCase(TestCase):
    def test_clean_email(self):
        # Test clean_email method of CustomUserCreationForm
        form = CustomUserCreationForm(data={'name': 'Name Test',
                                            'email': 'test@example.com',
                                            'password1': 'passwordtest', 
                                            'password2': 'passwordtest',
                                            })
        self.assertTrue(form.is_valid())

        # Attempt to register a user with an existing email
        existing_user = get_user_model().objects.create_user(
            email='test@example.com',
            name='Existing User',
            password='password123',
        )
        form = CustomUserCreationForm(data={'name': 'Name Test',
                                            'email': 'test@example.com',
                                            'password1': 'passwordtest', 
                                            'password2': 'passwordtest',
                                            })
        self.assertFalse(form.is_valid())
        self.assertIn('Email test@example.com is already in use', form.errors['email'])

class CustomAuthenticationFormTestCase(TestCase):
    def test_clean(self):
        # Test clean method of CustomAuthenticationForm
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            name='Test User',
            password='password123',
        )
        
        form = CustomAuthenticationForm(data={'email': 'test@example.com', 'password': 'password123'})
        self.assertTrue(form.is_valid())

        # Attempt to login with invalid email or password
        form = CustomAuthenticationForm(data={'email': 'test@example.com', 'password': 'wrongpassword'})
        self.assertFalse(form.is_valid())
        self.assertIn('Invalid email or password.', form.non_field_errors())