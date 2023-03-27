import os
import uuid

from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import CustomUsernameValidator

User = get_user_model()


def rename_profile_image(instance, filename):
    # get file extension
    ext = filename.split('.')[-1]

    # Generate a unique file name based on a random string
    random_string = str(uuid.uuid4().hex)[:6]

    # Get the user's email address (if available) or generate a unique identifier
    email = instance.user.email if instance.user else 'test'

    # Use the email address or unique identifier to create a separate directory for each user
    user_dir = os.path.join('profile_images', email)

    # Create the directory if it doesn't already exist
    if not default_storage.exists(user_dir):
        os.mkdir(os.path.join(default_storage.location, user_dir))

    # Generate a unique file name based on the random string, the user's email address or unique identifier,
    # and the file extension
    new_file_name = f"{random_string}.{ext}"

    # Return the new file path relative to the media root
    return os.path.join(user_dir, new_file_name)


class Profile(models.Model):
    """
        This model stores additional info about users.
    """
    username_validator = CustomUsernameValidator()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        unique=True,
        validators=[username_validator, MinLengthValidator(3)],
    )

    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    bio = models.CharField(max_length=256, blank=True)
    image = models.ImageField(verbose_name="profile image", upload_to=rename_profile_image,
                              default='profile_images/default/default_profile_image.png')

    def __str__(self):
        return self.user.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
