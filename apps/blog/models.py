import os
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.storage import default_storage
from django.db import models

from apps.common.models import TimeStampedModel


def rename_post_cover(instance, filename):
    ext = filename.split('.')[-1]

    # Generate a unique file name based on a random string
    random_string = str(uuid.uuid4().hex)[:6]

    # Get the user's email address (if available) or generate a unique identifier
    email = instance.owner.user.email if instance.owner.user else 'test'

    # Use the email address or unique identifier to create a separate directory for each user
    user_dir = os.path.join('post_covers', email)

    # Create the directory if it doesn't already exist
    if not default_storage.exists(user_dir):
        default_storage.makedirs(user_dir)

    # Generate a unique file name based on the random string, the user's email address or unique identifier,
    # and the file extension
    new_file_name = f"{random_string}{ext}"

    # Return the new file path relative to the media root
    return os.path.join(user_dir, new_file_name)


class Post(TimeStampedModel):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, allow_unicode=True)
    summary = models.CharField(max_length=256)
    content = RichTextUploadingField()
    post_cover = models.ImageField(verbose_name='post cover image', upload_to=rename_post_cover)
