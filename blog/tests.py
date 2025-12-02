from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Post, Category, Comment
from .forms import CommentForm, SearchForm
from taggit.models import Tag


class CategoryModelTest(TestCase):
    """Test cases for Category model."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Technology',
            slug='technology',
            description='Tech related posts',
            color='#3B82F6'
        )
    
    def test_category_creation(self):
        """Test category creation."""
        self.assertEqual(self.category.name, 'Technology')
        self.assertEqual(self.category.slug, 'technology')
        self.assertEqual(str(self.category), 'Technology')
    
    def test_category_get_absolute_url(self):
        """Test category absolute URL."""
        expected_url = reverse('blog:category_posts', args=[self.category.slug])
        self.assertEqual(self.category.get_absolute_url(), expected_url)
    
    def test_category_get_post_count(self):
        """Test category post count method."""
        # Initially no posts
        self.assertEqual(self.category.get_post_count(), 0)
        
        # Create a user and post
        user = User.objects.create_user('testuser', 'test@example.com', 'password')
        Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=user,
            category=self.category,
            is_published=True
        )
        
        # Now should have 1 post
        self.assertEqual(self.category.get_post_count(), 1)


class PostModelTest(TestCase):
    """Test cases for Post model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is a test post content with enough words to calculate reading time.',
            excerpt='Test excerpt',
            author=self.user,
            category=self.category,
            is_published=True,
            published_at=timezone.now()
        )
    
    def test_post_creation(self):
        """Test post creation."""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(str(self.post), 'Test Post')
        self.assertTrue(self.post.is_published)
    
    def test_post_get_absolute_url(self):
        """Test post absolute URL."""
        expected_url = reverse('blog:post_detail', args=[self.post.slug])
        self.assertEqual(self.post.get_absolute_url(), expected_url)
    
    def test_post_calculate_reading_time(self):
        """Test reading time calculation."""
        reading_time = self.post.calculate_reading_time()
        self.assertGreater(reading_time, 0)
        self.assertIsInstance(reading_time, int)
    
    def test_post_get_excerpt(self):
        """Test excerpt generation."""
        # Test with existing excerpt
        self.assertEqual(self.post.get_excerpt(), 'Test excerpt')
        
        # Test without excerpt
        self.post.excerpt = ''
        excerpt = self.post.get_excerpt()
        self.assertLessEqual(len(excerpt), 200)
    
    def test_post_increment_views(self):
        """Test view count increment."""
        initial_views = self.post.views_count
        self.post.increment_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, initial_views + 1)
    
    def test_post_get_related_posts(self):
        """Test related posts functionality."""
        # Create another post in same category
        related_post = Post.objects.create(
            title='Related Post',
            slug='related-post',
            content='Related content',
            author=self.user,
            category=self.category,
            is_published=True
        )
        
        related_posts = self.post.get_related_posts()
        self.assertIn(related_post, related_posts)
    
    def test_post_manager_published(self):
        """Test published posts manager."""
        # Create unpublished post
        unpublished_post = Post.objects.create(
            title='Unpublished Post',
            slug='unpublished-post',
            content='Unpublished content',
            author=self.user,
            is_published=False
        )
        
        published_posts = Post.published.all()
        self.assertIn(self.post, published_posts)
        self.assertNotIn(unpublished_post, published_posts)
    
    def test_post_manager_featured(self):
        """Test featured posts manager."""
        # Mark post as featured
        self.post.is_featured = True
        self.post.save()
        
        featured_posts = Post.featured.all()
        self.assertIn(self.post, featured_posts)


class CommentModelTest(TestCase):
    """Test cases for Comment model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=self.user,
            is_published=True
        )
        self.comment = Comment.objects.create(
            post=self.post,
            name='John Doe',
            email='john@example.com',
            content='Great post!'
        )
    
    def test_comment_creation(self):
        """Test comment creation."""
        self.assertEqual(self.comment.name, 'John Doe')
        self.assertEqual(self.comment.email, 'john@example.com')
        self.assertEqual(self.comment.content, 'Great post!')
        self.assertFalse(self.comment.is_approved)  # Default is False
    
    def test_comment_str_representation(self):
        """Test comment string representation."""
        expected_str = f'Comment by John Doe on {self.post.title}'
        self.assertEqual(str(self.comment), expected_str)


class CommentFormTest(TestCase):
    """Test cases for CommentForm."""
    
    def test_valid_comment_form(self):
        """Test valid comment form."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': 'This is a great post! Thanks for sharing.',
            'honeypot': ''
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_comment_form_honeypot_validation(self):
        """Test honeypot spam protection."""
        form_data = {
            'name': 'Spammer',
            'email': 'spam@example.com',
            'content': 'Spam content',
            'honeypot': 'spam'
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('honeypot', form.errors)
    
    def test_comment_form_name_validation(self):
        """Test name field validation."""
        form_data = {
            'name': 'A',  # Too short
            'email': 'test@example.com',
            'content': 'Valid content here',
            'honeypot': ''
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_comment_form_content_validation(self):
        """Test content field validation."""
        form_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': 'Short',  # Too short
            'honeypot': ''
        }
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)


class SearchFormTest(TestCase):
    """Test cases for SearchForm."""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
    
    def test_valid_search_form(self):
        """Test valid search form."""
        form_data = {
            'query': 'django tutorial',
            'category': self.category.id,
            'tag': 'python'
        }
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_search_form_query_validation(self):
        """Test search query validation."""
        form_data = {
            'query': 'a',  # Too short
        }
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('query', form.errors)
    
    def test_search_form_empty_is_valid(self):
        """Test that empty search form is valid."""
        form = SearchForm(data={})
        self.assertTrue(form.is_valid())


class BlogViewsTest(TestCase):
    """Test cases for blog views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content for the blog post',
            author=self.user,
            category=self.category,
            is_published=True,
            published_at=timezone.now()
        )
        self.post.tags.add('python', 'django')
    
    def test_post_list_view(self):
        """Test post list view."""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_post_detail_view(self):
        """Test post detail view."""
        response = self.client.get(reverse('blog:post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.content)
    
    def test_post_detail_view_increments_views(self):
        """Test that post detail view increments view count."""
        initial_views = self.post.views_count
        self.client.get(reverse('blog:post_detail', args=[self.post.slug]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.views_count, initial_views + 1)
    
    def test_category_posts_view(self):
        """Test category posts view."""
        response = self.client.get(reverse('blog:category_posts', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.category.name)
    
    def test_tag_posts_view(self):
        """Test tag posts view."""
        response = self.client.get(reverse('blog:tag_posts', args=['python']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_search_view(self):
        """Test search view."""
        response = self.client.get(reverse('blog:search'), {'query': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_archive_view(self):
        """Test archive view."""
        response = self.client.get(reverse('blog:archive'))
        self.assertEqual(response.status_code, 200)
    
    def test_archive_year_view(self):
        """Test archive year view."""
        year = self.post.published_at.year
        response = self.client.get(reverse('blog:archive_year', args=[year]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_archive_month_view(self):
        """Test archive month view."""
        year = self.post.published_at.year
        month = self.post.published_at.month
        response = self.client.get(reverse('blog:archive_month', args=[year, month]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
    
    def test_unpublished_post_not_visible(self):
        """Test that unpublished posts are not visible."""
        unpublished_post = Post.objects.create(
            title='Unpublished Post',
            slug='unpublished-post',
            content='Unpublished content',
            author=self.user,
            is_published=False
        )
        
        # Should not appear in list
        response = self.client.get(reverse('blog:post_list'))
        self.assertNotContains(response, unpublished_post.title)
        
        # Should return 404 for direct access
        response = self.client.get(reverse('blog:post_detail', args=[unpublished_post.slug]))
        self.assertEqual(response.status_code, 404)


class BlogFeedsTest(TestCase):
    """Test cases for blog feeds."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=self.user,
            is_published=True,
            published_at=timezone.now()
        )
    
    def test_rss_feed(self):
        """Test RSS feed."""
        response = self.client.get(reverse('blog:rss_feed'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/rss+xml; charset=utf-8')
        self.assertContains(response, self.post.title)


class BlogSitemapsTest(TestCase):
    """Test cases for blog sitemaps."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.category = Category.objects.create(
            name='Technology',
            slug='technology'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test content',
            author=self.user,
            category=self.category,
            is_published=True,
            published_at=timezone.now()
        )
    
    def test_sitemap_contains_posts(self):
        """Test that sitemap contains published posts."""
        from .sitemaps import PostSitemap
        sitemap = PostSitemap()
        self.assertIn(self.post, sitemap.items())
    
    def test_sitemap_contains_categories(self):
        """Test that sitemap contains categories with posts."""
        from .sitemaps import CategorySitemap
        sitemap = CategorySitemap()
        self.assertIn(self.category, sitemap.items())