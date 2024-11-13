from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# User Role Choices
class Role(models.TextChoices):
    REPORTER = 'reporter', _('Reporter')
    EDITOR = 'editor', _('Editor')
    ZONAL_EDITOR = 'zonal_editor', _('Zonal Editor')
    REGIONAL_EDITOR = 'regional_editor', _('Regional Editor')
    NATIONAL_EDITOR = 'national_editor', _('National Editor')
    DESK_HEAD = 'desk_head', _('Desk Head')

# User Model (authentication)
class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.REPORTER
    )

    def __str__(self):
        return self.username

# Staff Model (Related to User for role-based staff management)
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Tags Model
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Categories and Subcategories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

# Report Model
class Report(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Staff, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    geo_coordinates = models.CharField(max_length=100, blank=True, null=True)  # optional geo-coordinates
    is_published = models.BooleanField(default=False)
    attachments = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.title

# ReportDesk Model (Editorial Workflow)
class ReportDesk(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    desk_head = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    stage = models.CharField(
        max_length=100,
        choices=[('draft', 'Draft'), ('under_review', 'Under Review'), ('approved', 'Approved')],
        default='draft'
    )
    review_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.report.title} - {self.stage}"
