from rest_framework import serializers

from .models import Blog, BlogCategory


class BlogCategorySerializer(serializers.ModelSerializer):
    """Serializer for blog category view with basic information"""

    class Meta:
        model = BlogCategory
        fields = ["title", "slug"]


class BlogListSerializer(serializers.ModelSerializer):
    """Serializer for blog list view with basic information"""

    category = serializers.CharField(source="category.title")
    author = serializers.CharField(source="author.get_full_name")
    author_avatar = serializers.URLField(source="author.picture")
    likes = serializers.SerializerMethodField()
    bookmarks = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "author_avatar",
            "published_at",
            "read_time",
            "short_description",
            "image",
            "tags",
            "category",
            "likes",
            "bookmarks",
        ]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_bookmarks(self, obj):
        return obj.bookmarks.count()


class BlogDetailSerializer(serializers.ModelSerializer):
    """Serializer for blog detail view with full information"""

    category = serializers.CharField(source="category.title")
    author = serializers.CharField(source="author.get_full_name")
    author_avatar = serializers.URLField(source="author.picture")
    author_bio = serializers.CharField(source="author.bio")
    likes = serializers.SerializerMethodField()
    bookmarks = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "author",
            "author_avatar",
            "author_bio",
            "short_description",
            "content",
            "image",
            "tags",
            "read_time",
            "views_count",
            "status",
            "published_at",
            "category",
            "likes",
            "bookmarks",
            "is_liked",
            "is_bookmarked",
        ]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_bookmarks(self, obj):
        return obj.bookmarks.count()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False
