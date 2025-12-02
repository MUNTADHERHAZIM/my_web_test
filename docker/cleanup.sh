#!/bin/bash

# Cleanup script for Django application
set -e

# Configuration
LOG_FILE="/app/logs/cleanup.log"
MAX_LOG_AGE=30  # days
MAX_TEMP_AGE=7  # days
MAX_CACHE_AGE=1  # days
MAX_SESSION_AGE=7  # days
MAX_UPLOAD_AGE=90  # days
MAX_BACKUP_AGE=30  # days

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output with timestamp
log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case $level in
        "INFO")
            echo -e "${BLUE}[$timestamp] [INFO]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[$timestamp] [SUCCESS]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        "WARNING")
            echo -e "${YELLOW}[$timestamp] [WARNING]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        "ERROR")
            echo -e "${RED}[$timestamp] [ERROR]${NC} $message" | tee -a "$LOG_FILE"
            ;;
    esac
}

# Function to get human readable size
get_size() {
    local path=$1
    if [ -d "$path" ]; then
        du -sh "$path" 2>/dev/null | cut -f1 || echo "0B"
    elif [ -f "$path" ]; then
        ls -lh "$path" 2>/dev/null | awk '{print $5}' || echo "0B"
    else
        echo "0B"
    fi
}

# Function to clean old log files
clean_old_logs() {
    log_message "INFO" "Cleaning old log files (older than $MAX_LOG_AGE days)"
    
    local cleaned_count=0
    local total_size_before=0
    local total_size_after=0
    
    # Calculate total size before cleanup
    for log_dir in "/app/logs" "/var/log/nginx" "/var/log/supervisor"; do
        if [ -d "$log_dir" ]; then
            local size=$(du -sb "$log_dir" 2>/dev/null | cut -f1 || echo 0)
            total_size_before=$((total_size_before + size))
        fi
    done
    
    # Clean log files
    for log_dir in "/app/logs" "/var/log/nginx" "/var/log/supervisor"; do
        if [ -d "$log_dir" ]; then
            log_message "INFO" "Cleaning logs in $log_dir"
            
            # Find and remove old log files
            while IFS= read -r -d '' file; do
                local file_size=$(get_size "$file")
                rm -f "$file"
                log_message "INFO" "Removed old log file: $file ($file_size)"
                ((cleaned_count++))
            done < <(find "$log_dir" -name "*.log.*" -type f -mtime +$MAX_LOG_AGE -print0 2>/dev/null || true)
            
            # Compress large current log files
            while IFS= read -r -d '' file; do
                if [ -f "$file" ]; then
                    local size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
                    if [ "$size" -gt 10485760 ]; then  # 10MB
                        local file_size=$(get_size "$file")
                        gzip "$file"
                        log_message "INFO" "Compressed large log file: $file ($file_size)"
                    fi
                fi
            done < <(find "$log_dir" -name "*.log" -type f -print0 2>/dev/null || true)
        fi
    done
    
    # Calculate total size after cleanup
    for log_dir in "/app/logs" "/var/log/nginx" "/var/log/supervisor"; do
        if [ -d "$log_dir" ]; then
            local size=$(du -sb "$log_dir" 2>/dev/null | cut -f1 || echo 0)
            total_size_after=$((total_size_after + size))
        fi
    done
    
    local saved_size=$((total_size_before - total_size_after))
    log_message "SUCCESS" "Cleaned $cleaned_count old log files, saved $(numfmt --to=iec $saved_size)"
}

# Function to clean temporary files
clean_temp_files() {
    log_message "INFO" "Cleaning temporary files (older than $MAX_TEMP_AGE days)"
    
    local cleaned_count=0
    local total_size=0
    
    # Directories to clean
    local temp_dirs=(
        "/tmp"
        "/var/tmp"
        "/app/tmp"
        "/app/media/temp"
    )
    
    for temp_dir in "${temp_dirs[@]}"; do
        if [ -d "$temp_dir" ]; then
            log_message "INFO" "Cleaning temporary files in $temp_dir"
            
            while IFS= read -r -d '' file; do
                local file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
                total_size=$((total_size + file_size))
                rm -rf "$file"
                ((cleaned_count++))
            done < <(find "$temp_dir" -type f -mtime +$MAX_TEMP_AGE -print0 2>/dev/null || true)
        fi
    done
    
    log_message "SUCCESS" "Cleaned $cleaned_count temporary files, freed $(numfmt --to=iec $total_size)"
}

# Function to clean cache files
clean_cache_files() {
    log_message "INFO" "Cleaning cache files (older than $MAX_CACHE_AGE days)"
    
    local cleaned_count=0
    local total_size=0
    
    # Cache directories
    local cache_dirs=(
        "/app/cache"
        "/app/.cache"
        "/root/.cache"
        "/var/cache"
    )
    
    for cache_dir in "${cache_dirs[@]}"; do
        if [ -d "$cache_dir" ]; then
            log_message "INFO" "Cleaning cache files in $cache_dir"
            
            while IFS= read -r -d '' file; do
                local file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
                total_size=$((total_size + file_size))
                rm -rf "$file"
                ((cleaned_count++))
            done < <(find "$cache_dir" -type f -mtime +$MAX_CACHE_AGE -print0 2>/dev/null || true)
        fi
    done
    
    # Clean Python cache
    log_message "INFO" "Cleaning Python cache files"
    find /app -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find /app -name "*.pyc" -type f -delete 2>/dev/null || true
    find /app -name "*.pyo" -type f -delete 2>/dev/null || true
    
    log_message "SUCCESS" "Cleaned $cleaned_count cache files, freed $(numfmt --to=iec $total_size)"
}

# Function to clean Django sessions
clean_django_sessions() {
    log_message "INFO" "Cleaning expired Django sessions"
    
    cd /app
    
    # Clean expired sessions
    local session_count_before=$(python manage.py shell -c "from django.contrib.sessions.models import Session; print(Session.objects.count())" 2>/dev/null || echo "0")
    
    python manage.py clearsessions 2>/dev/null || log_message "WARNING" "Failed to clean Django sessions"
    
    local session_count_after=$(python manage.py shell -c "from django.contrib.sessions.models import Session; print(Session.objects.count())" 2>/dev/null || echo "0")
    
    local cleaned_sessions=$((session_count_before - session_count_after))
    log_message "SUCCESS" "Cleaned $cleaned_sessions expired Django sessions"
}

# Function to clean old uploads
clean_old_uploads() {
    log_message "INFO" "Cleaning old upload files (older than $MAX_UPLOAD_AGE days)"
    
    local upload_dir="/app/media/uploads"
    local cleaned_count=0
    local total_size=0
    
    if [ -d "$upload_dir" ]; then
        # Find orphaned upload files (not referenced in database)
        cd /app
        
        # Create a temporary file with all file paths from database
        local db_files="/tmp/db_files.txt"
        python manage.py shell << EOF > "$db_files" 2>/dev/null || true
from django.apps import apps
import os

# Get all models with FileField or ImageField
for model in apps.get_models():
    for field in model._meta.get_fields():
        if hasattr(field, 'upload_to'):
            for obj in model.objects.all():
                file_field = getattr(obj, field.name)
                if file_field and hasattr(file_field, 'path'):
                    try:
                        print(file_field.path)
                    except:
                        pass
EOF
        
        # Find files not in database
        while IFS= read -r -d '' file; do
            if [ -f "$file" ] && ! grep -Fxq "$file" "$db_files" 2>/dev/null; then
                local file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
                total_size=$((total_size + file_size))
                rm -f "$file"
                log_message "INFO" "Removed orphaned upload: $file"
                ((cleaned_count++))
            fi
        done < <(find "$upload_dir" -type f -mtime +$MAX_UPLOAD_AGE -print0 2>/dev/null || true)
        
        # Clean up temporary file
        rm -f "$db_files"
    fi
    
    log_message "SUCCESS" "Cleaned $cleaned_count old upload files, freed $(numfmt --to=iec $total_size)"
}

# Function to clean old backups
clean_old_backups() {
    log_message "INFO" "Cleaning old backup files (older than $MAX_BACKUP_AGE days)"
    
    local backup_dirs=(
        "/app/backups"
        "/app/media/backups"
        "/var/backups"
    )
    
    local cleaned_count=0
    local total_size=0
    
    for backup_dir in "${backup_dirs[@]}"; do
        if [ -d "$backup_dir" ]; then
            log_message "INFO" "Cleaning backups in $backup_dir"
            
            while IFS= read -r -d '' file; do
                local file_size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo 0)
                total_size=$((total_size + file_size))
                rm -f "$file"
                log_message "INFO" "Removed old backup: $file"
                ((cleaned_count++))
            done < <(find "$backup_dir" -type f -mtime +$MAX_BACKUP_AGE -print0 2>/dev/null || true)
        fi
    done
    
    log_message "SUCCESS" "Cleaned $cleaned_count old backup files, freed $(numfmt --to=iec $total_size)"
}

# Function to optimize database
optimize_database() {
    log_message "INFO" "Optimizing database"
    
    cd /app
    
    # Run database optimization commands
    python manage.py shell << EOF 2>/dev/null || log_message "WARNING" "Database optimization failed"
from django.db import connection

# PostgreSQL specific optimizations
if 'postgresql' in connection.vendor:
    with connection.cursor() as cursor:
        cursor.execute("VACUUM ANALYZE;")
        print("PostgreSQL VACUUM ANALYZE completed")

# SQLite specific optimizations
elif 'sqlite' in connection.vendor:
    with connection.cursor() as cursor:
        cursor.execute("VACUUM;")
        cursor.execute("PRAGMA optimize;")
        print("SQLite optimization completed")
EOF
    
    log_message "SUCCESS" "Database optimization completed"
}

# Function to generate cleanup report
generate_report() {
    log_message "INFO" "Generating cleanup report"
    
    local report_file="/app/logs/cleanup_report_$(date +%Y%m%d_%H%M%S).txt"
    
    cat > "$report_file" << EOF
Cleanup Report - $(date)
================================

System Information:
- Hostname: $(hostname)
- Uptime: $(uptime)
- Disk Usage: $(df -h /app | tail -1)
- Memory Usage: $(free -h | grep Mem)

Directory Sizes:
- Application: $(get_size /app)
- Logs: $(get_size /app/logs)
- Media: $(get_size /app/media)
- Static: $(get_size /app/staticfiles)
- Cache: $(get_size /app/cache)

Process Information:
$(ps aux --sort=-%mem | head -10)

Recent Log Entries:
$(tail -20 "$LOG_FILE")
EOF
    
    log_message "SUCCESS" "Cleanup report generated: $report_file"
}

# Function to run comprehensive cleanup
run_cleanup() {
    log_message "INFO" "Starting comprehensive cleanup"
    
    local start_time=$(date +%s)
    
    # Run cleanup functions
    clean_old_logs
    clean_temp_files
    clean_cache_files
    clean_django_sessions
    clean_old_uploads
    clean_old_backups
    optimize_database
    
    # Generate report
    generate_report
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    log_message "SUCCESS" "Cleanup completed in ${duration}s"
}

# Main execution
main() {
    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Run cleanup based on argument
    case "${1:-all}" in
        "logs")
            clean_old_logs
            ;;
        "temp")
            clean_temp_files
            ;;
        "cache")
            clean_cache_files
            ;;
        "sessions")
            clean_django_sessions
            ;;
        "uploads")
            clean_old_uploads
            ;;
        "backups")
            clean_old_backups
            ;;
        "database")
            optimize_database
            ;;
        "report")
            generate_report
            ;;
        "all")
            run_cleanup
            ;;
        *)
            echo "Usage: $0 {logs|temp|cache|sessions|uploads|backups|database|report|all}"
            echo "  logs     - Clean old log files"
            echo "  temp     - Clean temporary files"
            echo "  cache    - Clean cache files"
            echo "  sessions - Clean expired Django sessions"
            echo "  uploads  - Clean old upload files"
            echo "  backups  - Clean old backup files"
            echo "  database - Optimize database"
            echo "  report   - Generate cleanup report"
            echo "  all      - Run all cleanup tasks (default)"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"