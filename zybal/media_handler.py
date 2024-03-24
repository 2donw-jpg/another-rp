import os
from dev import settings

def create_user_media(user):
    new_directory_path = os.path.join(settings.MEDIA_URL, str(id.pk))
    os.makedirs(new_directory_path)

