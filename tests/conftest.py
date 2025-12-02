"""Test configuration and fixtures for the project."""

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.core.management import call_command
from django.db import transaction

from blog.models import Category, Post
from core.models import Project

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Set up the test database."""
    with django_db_blocker.unblock():
        call_command("migrate", "--run-syncdb")


@pytest.fixture
def client():
    """Django test client."""
    return Client()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user."""
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass123",
        first_name="Admin",
        last_name="User",
    )


@pytest.fixture
def authenticated_client(client, user):
    """Client with authenticated user."""
    client.force_login(user)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    """Client with authenticated admin user."""
    client.force_login(admin_user)
    return client


@pytest.fixture
def category(db):
    """Create a test blog category."""
    return Category.objects.create(
        name_en="Technology",
        name_ar="التكنولوجيا",
        slug="technology",
        description_en="Technology related posts",
        description_ar="مقالات متعلقة بالتكنولوجيا",
    )


@pytest.fixture
def post(db, user, category):
    """Create a test blog post."""
    return Post.objects.create(
        title_en="Test Post",
        title_ar="مقال تجريبي",
        slug="test-post",
        content_en="This is a test post content.",
        content_ar="هذا محتوى مقال تجريبي.",
        excerpt_en="Test excerpt",
        excerpt_ar="مقتطف تجريبي",
        author=user,
        category=category,
        status="published",
        featured=False,
    )


@pytest.fixture
def project(db):
    """Create a test project."""
    return Project.objects.create(
        title_en="Test Project",
        title_ar="مشروع تجريبي",
        slug="test-project",
        description_en="This is a test project.",
        description_ar="هذا مشروع تجريبي.",
        content_en="Detailed project content.",
        content_ar="محتوى مفصل للمشروع.",
        technologies="Django, Python, PostgreSQL",
        github_url="https://github.com/test/project",
        live_url="https://testproject.com",
        featured=True,
        completed=True,
    )


@pytest.fixture
def multiple_posts(db, user, category):
    """Create multiple test posts."""
    posts = []
    for i in range(5):
        post = Post.objects.create(
            title_en=f"Test Post {i+1}",
            title_ar=f"مقال تجريبي {i+1}",
            slug=f"test-post-{i+1}",
            content_en=f"This is test post {i+1} content.",
            content_ar=f"هذا محتوى المقال التجريبي {i+1}.",
            excerpt_en=f"Test excerpt {i+1}",
            excerpt_ar=f"مقتطف تجريبي {i+1}",
            author=user,
            category=category,
            status="published" if i < 3 else "draft",
            featured=i == 0,
        )
        posts.append(post)
    return posts


@pytest.fixture
def multiple_categories(db):
    """Create multiple test categories."""
    categories = []
    category_data = [
        ("Technology", "التكنولوجيا", "technology"),
        ("Programming", "البرمجة", "programming"),
        ("Web Development", "تطوير الويب", "web-development"),
    ]
    
    for name_en, name_ar, slug in category_data:
        category = Category.objects.create(
            name_en=name_en,
            name_ar=name_ar,
            slug=slug,
            description_en=f"{name_en} related posts",
            description_ar=f"مقالات متعلقة بـ{name_ar}",
        )
        categories.append(category)
    
    return categories


@pytest.fixture
def sample_data(db, user, admin_user, multiple_categories, multiple_posts):
    """Create a complete set of sample data for testing."""
    return {
        "user": user,
        "admin_user": admin_user,
        "categories": multiple_categories,
        "posts": multiple_posts,
    }


@pytest.mark.django_db
class DatabaseTestCase:
    """Base test case for database tests."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        """Set up method for each test."""
        pass


@pytest.mark.django_db(transaction=True)
class TransactionTestCase:
    """Base test case for transaction tests."""
    
    @pytest.fixture(autouse=True)
    def setup_method(self, transactional_db):
        """Set up method for each test."""
        pass