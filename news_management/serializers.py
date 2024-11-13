from rest_framework import serializers
from .models import Staff, Tag, Category, Report, ReportDesk

# Staff Serializer
class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'user', 'department', 'bio']

# Tag Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_category']

# Report Serializer
class ReportSerializer(serializers.ModelSerializer):
    author = StaffSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'title', 'description', 'content', 'created_at', 'updated_at', 'author', 'category', 'tags', 'geo_coordinates', 'is_published', 'attachments']

# ReportDesk Serializer (to handle editorial workflow)
class ReportDeskSerializer(serializers.ModelSerializer):
    report = ReportSerializer(read_only=True)
    desk_head = StaffSerializer(read_only=True)

    class Meta:
        model = ReportDesk
        fields = ['id', 'report', 'desk_head', 'stage', 'review_comments']
