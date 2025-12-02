from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db import transaction
import os


class Command(BaseCommand):
    help = 'Load sample data for the website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset database before loading data',
        )
        parser.add_argument(
            '--create-superuser',
            action='store_true',
            help='Create superuser after loading data',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write(
                self.style.WARNING('Resetting database...')
            )
            call_command('flush', '--noinput')
            call_command('migrate')

        self.stdout.write(
            self.style.SUCCESS('Loading sample data...')
        )

        try:
            with transaction.atomic():
                # Load initial data
                fixtures_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    'fixtures',
                    'initial_data.json'
                )
                
                if os.path.exists(fixtures_path):
                    call_command('loaddata', fixtures_path)
                    self.stdout.write(
                        self.style.SUCCESS('✓ Initial data loaded successfully')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('✗ Initial data file not found')
                    )
                    return

                # Create superuser if requested
                if options['create_superuser']:
                    self.create_superuser()

                # Update user password (since fixtures can't store hashed passwords properly)
                self.update_user_passwords()

                self.stdout.write(
                    self.style.SUCCESS('\n🎉 Sample data loaded successfully!')
                )
                self.stdout.write(
                    self.style.SUCCESS('\nYou can now:')
                )
                self.stdout.write('  • Visit the website to see sample content')
                self.stdout.write('  • Login to admin with: muntazir / admin123')
                self.stdout.write('  • Explore the blog posts and projects')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading sample data: {str(e)}')
            )
            raise

    def create_superuser(self):
        """Create a superuser if it doesn't exist"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(
                self.style.SUCCESS('✓ Superuser created: admin / admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('! Superuser already exists')
            )

    def update_user_passwords(self):
        """Update user passwords to proper hashed versions"""
        try:
            user = User.objects.get(username='muntazir')
            user.set_password('admin123')  # Set a proper password
            user.save()
            self.stdout.write(
                self.style.SUCCESS('✓ User passwords updated')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('! User muntazir not found')
            )