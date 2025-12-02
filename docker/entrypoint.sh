#!/bin/bash

# Entrypoint script for Django application
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to wait for database
wait_for_db() {
    print_status "Waiting for database connection..."
    
    while ! python manage.py dbshell --command="SELECT 1;" > /dev/null 2>&1; do
        print_status "Database is unavailable - sleeping"
        sleep 2
    done
    
    print_success "Database is available!"
}

# Function to wait for Redis
wait_for_redis() {
    print_status "Waiting for Redis connection..."
    
    while ! python -c "import redis; r = redis.from_url('$REDIS_URL'); r.ping()" > /dev/null 2>&1; do
        print_status "Redis is unavailable - sleeping"
        sleep 2
    done
    
    print_success "Redis is available!"
}

# Function to run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    python manage.py makemigrations --noinput
    python manage.py migrate --noinput
    
    print_success "Database migrations completed!"
}

# Function to collect static files
collect_static() {
    print_status "Collecting static files..."
    
    python manage.py collectstatic --noinput --clear
    
    print_success "Static files collected!"
}

# Function to compile translation files
compile_messages() {
    print_status "Compiling translation files..."
    
    if command -v msgfmt > /dev/null 2>&1; then
        python manage.py compilemessages
        print_success "Translation files compiled!"
    else
        print_warning "msgfmt not found, skipping translation compilation"
    fi
}

# Function to create superuser
create_superuser() {
    print_status "Creating superuser..."
    
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@muntazir.com',
        password='admin123',
        first_name='Muntazir',
        last_name='Hazim Thamir'
    )
    print('Superuser created successfully!')
else:
    print('Superuser already exists!')
EOF
    
    print_success "Superuser setup completed!"
}

# Function to load initial data
load_initial_data() {
    print_status "Loading initial data..."
    
    # Load fixtures if they exist
    if [ -f "/app/fixtures/initial_data.json" ]; then
        python manage.py loaddata /app/fixtures/initial_data.json
        print_success "Initial data loaded!"
    else
        print_warning "No initial data fixtures found"
    fi
}

# Function to setup cron jobs
setup_cron() {
    print_status "Setting up cron jobs..."
    
    # Create crontab file
    cat > /tmp/crontab << EOF
# Django management commands
0 2 * * * cd /app && python manage.py clearsessions
0 3 * * * cd /app && python manage.py cleanup_uploads
0 4 * * * cd /app && python manage.py update_index
30 4 * * 0 cd /app && python manage.py dbbackup
0 5 * * * cd /app && python manage.py send_mail

# Log rotation
0 6 * * * /usr/sbin/logrotate -f /etc/logrotate.conf

# Health checks
*/5 * * * * curl -f http://localhost/health/ || echo "Health check failed at \$(date)" >> /app/logs/health_failures.log
EOF
    
    # Install crontab
    crontab /tmp/crontab
    rm /tmp/crontab
    
    print_success "Cron jobs setup completed!"
}

# Function to setup log rotation
setup_logrotate() {
    print_status "Setting up log rotation..."
    
    cat > /etc/logrotate.d/django << EOF
/app/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        supervisorctl restart django
    endscript
}

/var/log/nginx/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        supervisorctl restart nginx
    endscript
}
EOF
    
    print_success "Log rotation setup completed!"
}

# Function to check environment variables
check_environment() {
    print_status "Checking environment variables..."
    
    required_vars=("SECRET_KEY" "DATABASE_URL")
    missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -ne 0 ]; then
        print_error "Missing required environment variables: ${missing_vars[*]}"
        exit 1
    fi
    
    print_success "Environment variables check passed!"
}

# Function to setup directories
setup_directories() {
    print_status "Setting up directories..."
    
    # Create necessary directories
    mkdir -p /app/logs
    mkdir -p /app/staticfiles
    mkdir -p /app/media
    mkdir -p /var/log/supervisor
    mkdir -p /var/log/nginx
    
    # Set permissions
    chmod 755 /app/logs
    chmod 755 /app/staticfiles
    chmod 755 /app/media
    
    print_success "Directories setup completed!"
}

# Function to run health check
health_check() {
    print_status "Running health check..."
    
    # Check if Django can start
    python manage.py check --deploy
    
    print_success "Health check passed!"
}

# Main execution
main() {
    print_status "Starting Django application setup..."
    
    # Setup
    check_environment
    setup_directories
    
    # Wait for dependencies
    wait_for_db
    if [ -n "$REDIS_URL" ]; then
        wait_for_redis
    fi
    
    # Django setup
    run_migrations
    collect_static
    compile_messages
    
    # Initial data and user
    create_superuser
    load_initial_data
    
    # System setup
    setup_cron
    setup_logrotate
    
    # Final checks
    health_check
    
    print_success "Django application setup completed!"
    print_status "Starting services..."
    
    # Execute the main command
    exec "$@"
}

# Handle signals
trap 'print_status "Received SIGTERM, shutting down gracefully..."; exit 0' TERM
trap 'print_status "Received SIGINT, shutting down gracefully..."; exit 0' INT

# Run main function
main "$@"