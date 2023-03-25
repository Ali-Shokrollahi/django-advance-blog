from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class UserManagerTest(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(email="user@gmail.com", password="test123")
        User.objects.create_user(email="nopassworduser@gmail.com")
        User.objects.create_superuser(email="superuser@gmail.com", password="test123")

    def test_user_creation(self):
        user = User.objects.get(email="user@gmail.com")
        self.assertEqual(user.email, "user@gmail.com")
        self.assertEqual(str(user), "user@gmail.com")
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.email_verified)
        self.assertTrue(user.has_usable_password())
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_user_creation_without_password(self):
        user = User.objects.get(email="nopassworduser@gmail.com")
        self.assertFalse(user.has_usable_password())

    def test_user_with_capitalized_email_cannot_be_created(self):
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="NoPASSWORDuser@gmail.com")

        self.assertEqual(1, User.objects.filter(email="nopassworduser@gmail.com").count())

    def test_superuser_creation(self):
        user = User.objects.get(email="superuser@gmail.com")
        self.assertEqual(user.email, "superuser@gmail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.email_verified)
        self.assertTrue(user.has_usable_password())
        try:

            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)
