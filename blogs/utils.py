import random

from django.utils.text import slugify


def generate_unique_slug(model, title, slug_field):
    """
    Generate a unique slug for a model instance.
    Creates a slug from the title and appends a random number between 1,000,000 and
    9,999,999 to ensure uniqueness.

    Args:
        model: The Django model class
        title: The title to create slug from
        slug_field: The field name that stores the slug

    Returns:
        str: A unique slug
    """
    base_slug = slugify(title)

    slug = f"{base_slug}"

    # Check if slug already exists and regenerate if needed
    while model.objects.filter(**{slug_field: slug}).exists():
        random_number = random.randint(1_000_000, 9_999_999)
        slug = f"{base_slug}-{random_number}"

    return slug
