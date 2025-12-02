"""Tests for the blog application."""

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from django.utils import timezone
from datetime import timedelta

from blog.models import Category, Post, Comment
from blog.forms import CommentForm

User = get_user_model()


class BlogViewsTestCase(TestCase):
    """Test cases for blog views."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.category = Category.objects.create(
            name_en="Technology",
            name_ar="التكنولوجيا",
            slug="technology",
            description_en="Technology posts",
            description_ar="مقالات التكنولوجيا"
        )
        
        self.published_post = Post.objects.create(
            title_en="Published Post",
            title_ar="مقال منشور",
            slug="published-post",
            content_en="This is published content.",
            content_ar="هذا محتوى منشور.",
            excerpt_en="Published excerpt",
            excerpt_ar="مقتطف منشور",
            author=self.user,
            category=self.category,
            status="published",
            featured=True
        )
        
        self.draft_post = Post.objects.create(
            title_en="Draft Post",
            title_ar="مقال مسودة",
            slug="draft-post",
            content_en="This is draft content.",
            content_ar="هذا محتوى مسودة.",
            excerpt_en="Draft excerpt",
            excerpt_ar="مقتطف مسودة",
            author=self.user,
            category=self.category,
            status="draft"
        )
    
    def test_post_list_view(self):
        """Test blog post list view."""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_post.title_en)
        self.assertNotContains(response, self.draft_post.title_en)
    
    def test_post_detail_view_published(self):
        """Test blog post detail view for published post."""
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': self.published_post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.published_post)
    
    def test_post_detail_view_draft_anonymous(self):
        """Test blog post detail view for draft post (anonymous user)."""
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': self.draft_post.slug})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_post_detail_view_draft_author(self):
        """Test blog post detail view for draft post (author)."""
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('blog:post_detail', kwargs={'slug': self.draft_post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], self.draft_post)
    
    def test_category_list_view(self):
        """Test category list view."""
        response = self.client.get(reverse('blog:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name_en)
    
    def test_category_posts_view(self):
        """Test category posts view."""
        response = self.client.get(
            reverse('blog:category_posts', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_post.title_en)
        self.assertNotContains(response, self.draft_post.title_en)
    
    def test_search_view(self):
        """Test search view."""
        response = self.client.get(reverse('blog:search'), {'q': 'Published'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.published_post.title_en)
    
    def test_search_view_empty_query(self):
        """Test search view with empty query."""
        response = self.client.get(reverse('blog:search'), {'q': ''})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.published_post.title_en)


class PostModelTestCase(TestCase):
    """Test cases for Post model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.category = Category.objects.create(
            name_en="Technology",
            name_ar="التكنولوجيا",
            slug="technology",
            description_en="Technology posts",
            description_ar="مقالات التكنولوجيا"
        )
        
        self.post = Post.objects.create(
            title_en="Test Post",
            title_ar="مقال تجريبي",
            slug="test-post",
            content_en="This is test content.",
            content_ar="هذا محتوى تجريبي.",
            excerpt_en="Test excerpt",
            excerpt_ar="مقتطف تجريبي",
            author=self.user,
            category=self.category,
            status="published",
            featured=True
        )
    
    def test_post_str_representation(self):
        """Test post string representation."""
        activate('en')
        self.assertEqual(str(self.post), "Test Post")
        
        activate('ar')
        self.assertEqual(str(self.post), "مقال تجريبي")
    
    def test_post_get_absolute_url(self):
        """Test post get_absolute_url method."""
        expected_url = reverse('blog:post_detail', kwargs={'slug': self.post.slug})
        self.assertEqual(self.post.get_absolute_url(), expected_url)
    
    def test_post_reading_time(self):
        """Test post reading time calculation."""
        # Create a post with known word count
        long_content = ' '.join(['word'] * 250)  # 250 words
        self.post.content_en = long_content
        self.post.save()
        
        # Should be approximately 1 minute (250 words / 200 words per minute)
        self.assertEqual(self.post.reading_time, 1)
    
    def test_post_slug_uniqueness(self):
        """Test post slug uniqueness."""
        with self.assertRaises(Exception):
            Post.objects.create(
                title_en="Another Post",
                title_ar="مقال آخر",
                slug="test-post",  # Same slug
                content_en="Another content",
                content_ar="محتوى آخر",
                excerpt_en="Another excerpt",
                excerpt_ar="مقتطف آخر",
                author=self.user,
                category=self.category,
                status="published"
            )
    
    def test_post_published_manager(self):
        """Test post published manager."""
        # Create a draft post
        draft_post = Post.objects.create(
            title_en="Draft Post",
            title_ar="مقال مسودة",
            slug="draft-post",
            content_en="Draft content",
            content_ar="محتوى مسودة",
            excerpt_en="Draft excerpt",
            excerpt_ar="مقتطف مسودة",
            author=self.user,
            category=self.category,
            status="draft"
        )
        
        # Test published manager only returns published posts
        published_posts = Post.published.all()
        self.assertIn(self.post, published_posts)
        self.assertNotIn(draft_post, published_posts)


class CategoryModelTestCase(TestCase):
    """Test cases for Category model."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name_en="Technology",
            name_ar="التكنولوجيا",
            slug="technology",
            description_en="Technology related posts",
            description_ar="مقالات متعلقة بالتكنولوجيا"
        )
    
    def test_category_str_representation(self):
        """Test category string representation."""
        activate('en')
        self.assertEqual(str(self.category), "Technology")
        
        activate('ar')
        self.assertEqual(str(self.category), "التكنولوجيا")
    
    def test_category_get_absolute_url(self):
        """Test category get_absolute_url method."""
        expected_url = reverse('blog:category_posts', kwargs={'slug': self.category.slug})
        self.assertEqual(self.category.get_absolute_url(), expected_url)
    
    def test_category_slug_uniqueness(self):
        """Test category slug uniqueness."""
        with self.assertRaises(Exception):
            Category.objects.create(
                name_en="Another Category",
                name_ar="فئة أخرى",
                slug="technology",  # Same slug
                description_en="Another description",
                description_ar="وصف آخر"
            )


class CommentModelTestCase(TestCase):
    """Test cases for Comment model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.category = Category.objects.create(
            name_en="Technology",
            name_ar="التكنولوجيا",
            slug="technology",
            description_en="Technology posts",
            description_ar="مقالات التكنولوجيا"
        )
        
        self.post = Post.objects.create(
            title_en="Test Post",
            title_ar="مقال تجريبي",
            slug="test-post",
            content_en="Test content",
            content_ar="محتوى تجريبي",
            excerpt_en="Test excerpt",
            excerpt_ar="مقتطف تجريبي",
            author=self.user,
            category=self.category,
            status="published"
        )
        
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a test comment.",
            is_approved=True
        )
    
    def test_comment_str_representation(self):
        """Test comment string representation."""
        expected_str = f"Comment by {self.user.username} on {self.post.title_en}"
        self.assertEqual(str(self.comment), expected_str)
    
    def test_comment_approved_manager(self):
        """Test comment approved manager."""
        # Create an unapproved comment
        unapproved_comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Unapproved comment",
            is_approved=False
        )
        
        # Test approved manager only returns approved comments
        approved_comments = Comment.approved.all()
        self.assertIn(self.comment, approved_comments)
        self.assertNotIn(unapproved_comment, approved_comments)


class CommentFormTestCase(TestCase):
    """Test cases for CommentForm."""
    
    def test_comment_form_valid_data(self):
        """Test comment form with valid data."""
        form_data = {
            'content': 'This is a test comment.'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_comment_form_missing_content(self):
        """Test comment form with missing content."""
        form_data = {
            'content': ''
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)


@pytest.mark.django_db
class TestBlogViews:
    """Pytest-style tests for blog views."""
    
    def test_post_list_view_status_code(self, client):
        """Test post list view returns 200 status code."""
        response = client.get(reverse('blog:post_list'))
        assert response.status_code == 200
    
    def test_post_detail_view_with_post(self, client, post):
        """Test post detail view displays post."""
        response = client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200
        assert post.title_en in response.content.decode()
    
    def test_category_list_view_with_category(self, client, category):
        """Test category list view displays category."""
        response = client.get(reverse('blog:category_list'))
        assert response.status_code == 200
        assert category.name_en in response.content.decode()
    
    def test_search_functionality(self, client, post):
        """Test search functionality."""
        response = client.get(reverse('blog:search'), {'q': post.title_en[:10]})
        assert response.status_code == 200
        assert post.title_en in response.content.decode()
    
    def test_comment_submission(self, client, post, user):
        """Test comment submission."""
        client.force_login(user)
        data = {
            'content': 'This is a test comment.'
        }
        response = client.post(
            reverse('blog:post_detail', kwargs={'slug': post.slug}),
            data
        )
        assert response.status_code == 302
        assert Comment.objects.filter(post=post, author=user).exists()


@pytest.mark.django_db
class TestBlogModels:
    """Pytest-style tests for blog models."""
    
    def test_post_creation(self, user, category):
        """Test post creation."""
        post = Post.objects.create(
            title_en="Test Post",
            title_ar="مقال تجريبي",
            slug="test-post",
            content_en="Test content",
            content_ar="محتوى تجريبي",
            excerpt_en="Test excerpt",
            excerpt_ar="مقتطف تجريبي",
            author=user,
            category=category,
            status="published"
        )
        assert post.title_en == "Test Post"
        assert post.author == user
        assert post.category == category
        assert post.status == "published"
    
    def test_category_creation(self):
        """Test category creation."""
        category = Category.objects.create(
            name_en="Test Category",
            name_ar="فئة تجريبية",
            slug="test-category",
            description_en="Test description",
            description_ar="وصف تجريبي"
        )
        assert category.name_en == "Test Category"
        assert category.slug == "test-category"
    
    def test_comment_creation(self, user, post):
        """Test comment creation."""
        comment = Comment.objects.create(
            post=post,
            author=user,
            content="Test comment",
            is_approved=True
        )
        assert comment.post == post
        assert comment.author == user
        assert comment.content == "Test comment"
        assert comment.is_approved is True