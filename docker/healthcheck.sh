#!/bin/bash

# Health check script for Django application
set -e

# Configuration
HEALTH_CHECK_URL="http://localhost:8000/health/"
TIMEOUT=10
RETRIES=3
LOG_FILE="/app/logs/healthcheck.log"
PID_FILE="/var/run/healthcheck.pid"

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

# Function to check if process is already running
check_running() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            log_message "WARNING" "Health check already running with PID $pid"
            exit 1
        else
            rm -f "$PID_FILE"
        fi
    fi
}

# Function to create PID file
create_pid_file() {
    echo $$ > "$PID_FILE"
}

# Function to cleanup PID file
cleanup() {
    rm -f "$PID_FILE"
}

# Function to check HTTP endpoint
check_http_endpoint() {
    local url=$1
    local description=$2
    
    log_message "INFO" "Checking $description: $url"
    
    local response_code=$(curl -s -o /dev/null -w "%{http_code}" \
        --max-time "$TIMEOUT" \
        --retry "$RETRIES" \
        --retry-delay 1 \
        "$url" 2>/dev/null || echo "000")
    
    if [ "$response_code" = "200" ]; then
        log_message "SUCCESS" "$description is healthy (HTTP $response_code)"
        return 0
    else
        log_message "ERROR" "$description is unhealthy (HTTP $response_code)"
        return 1
    fi
}

# Function to check database connectivity
check_database() {
    log_message "INFO" "Checking database connectivity"
    
    if python manage.py dbshell --command="SELECT 1;" > /dev/null 2>&1; then
        log_message "SUCCESS" "Database is accessible"
        return 0
    else
        log_message "ERROR" "Database is not accessible"
        return 1
    fi
}

# Function to check Redis connectivity
check_redis() {
    if [ -z "$REDIS_URL" ]; then
        log_message "INFO" "Redis URL not configured, skipping Redis check"
        return 0
    fi
    
    log_message "INFO" "Checking Redis connectivity"
    
    if python -c "import redis; r = redis.from_url('$REDIS_URL'); r.ping()" > /dev/null 2>&1; then
        log_message "SUCCESS" "Redis is accessible"
        return 0
    else
        log_message "ERROR" "Redis is not accessible"
        return 1
    fi
}

# Function to check disk space
check_disk_space() {
    log_message "INFO" "Checking disk space"
    
    local usage=$(df /app | awk 'NR==2 {print $5}' | sed 's/%//')
    local threshold=90
    
    if [ "$usage" -lt "$threshold" ]; then
        log_message "SUCCESS" "Disk space is healthy ($usage% used)"
        return 0
    else
        log_message "ERROR" "Disk space is critical ($usage% used, threshold: $threshold%)"
        return 1
    fi
}

# Function to check memory usage
check_memory() {
    log_message "INFO" "Checking memory usage"
    
    local mem_info=$(free | grep Mem)
    local total=$(echo $mem_info | awk '{print $2}')
    local used=$(echo $mem_info | awk '{print $3}')
    local usage=$((used * 100 / total))
    local threshold=90
    
    if [ "$usage" -lt "$threshold" ]; then
        log_message "SUCCESS" "Memory usage is healthy ($usage% used)"
        return 0
    else
        log_message "ERROR" "Memory usage is critical ($usage% used, threshold: $threshold%)"
        return 1
    fi
}

# Function to check log file sizes
check_log_sizes() {
    log_message "INFO" "Checking log file sizes"
    
    local max_size=104857600  # 100MB in bytes
    local large_logs=()
    
    for log_file in /app/logs/*.log /var/log/nginx/*.log; do
        if [ -f "$log_file" ]; then
            local size=$(stat -f%z "$log_file" 2>/dev/null || stat -c%s "$log_file" 2>/dev/null || echo 0)
            if [ "$size" -gt "$max_size" ]; then
                large_logs+=("$log_file")
            fi
        fi
    done
    
    if [ ${#large_logs[@]} -eq 0 ]; then
        log_message "SUCCESS" "Log file sizes are healthy"
        return 0
    else
        log_message "WARNING" "Large log files detected: ${large_logs[*]}"
        return 1
    fi
}

# Function to check process status
check_processes() {
    log_message "INFO" "Checking critical processes"
    
    local processes=("gunicorn" "nginx" "supervisord")
    local failed_processes=()
    
    for process in "${processes[@]}"; do
        if ! pgrep "$process" > /dev/null; then
            failed_processes+=("$process")
        fi
    done
    
    if [ ${#failed_processes[@]} -eq 0 ]; then
        log_message "SUCCESS" "All critical processes are running"
        return 0
    else
        log_message "ERROR" "Failed processes: ${failed_processes[*]}"
        return 1
    fi
}

# Function to check SSL certificate (if HTTPS is enabled)
check_ssl_certificate() {
    if [ "$ENABLE_HTTPS" != "true" ]; then
        log_message "INFO" "HTTPS not enabled, skipping SSL certificate check"
        return 0
    fi
    
    log_message "INFO" "Checking SSL certificate"
    
    local domain=${DOMAIN:-localhost}
    local cert_file="/etc/ssl/certs/${domain}.crt"
    
    if [ ! -f "$cert_file" ]; then
        log_message "ERROR" "SSL certificate file not found: $cert_file"
        return 1
    fi
    
    # Check certificate expiration
    local expiry_date=$(openssl x509 -enddate -noout -in "$cert_file" | cut -d= -f2)
    local expiry_timestamp=$(date -d "$expiry_date" +%s)
    local current_timestamp=$(date +%s)
    local days_until_expiry=$(( (expiry_timestamp - current_timestamp) / 86400 ))
    
    if [ "$days_until_expiry" -gt 30 ]; then
        log_message "SUCCESS" "SSL certificate is valid ($days_until_expiry days until expiry)"
        return 0
    elif [ "$days_until_expiry" -gt 0 ]; then
        log_message "WARNING" "SSL certificate expires soon ($days_until_expiry days)"
        return 1
    else
        log_message "ERROR" "SSL certificate has expired"
        return 1
    fi
}

# Function to run comprehensive health check
run_health_check() {
    log_message "INFO" "Starting comprehensive health check"
    
    local checks=(
        "check_http_endpoint $HEALTH_CHECK_URL 'Django application'"
        "check_database"
        "check_redis"
        "check_disk_space"
        "check_memory"
        "check_log_sizes"
        "check_processes"
        "check_ssl_certificate"
    )
    
    local failed_checks=0
    local total_checks=${#checks[@]}
    
    for check in "${checks[@]}"; do
        if ! eval "$check"; then
            ((failed_checks++))
        fi
    done
    
    log_message "INFO" "Health check completed: $((total_checks - failed_checks))/$total_checks checks passed"
    
    if [ "$failed_checks" -eq 0 ]; then
        log_message "SUCCESS" "All health checks passed"
        return 0
    else
        log_message "ERROR" "$failed_checks health checks failed"
        return 1
    fi
}

# Function to send notification (placeholder)
send_notification() {
    local status=$1
    local message=$2
    
    # This is a placeholder for notification logic
    # You can integrate with services like Slack, Discord, email, etc.
    log_message "INFO" "Notification: $status - $message"
}

# Main execution
main() {
    # Setup
    check_running
    create_pid_file
    trap cleanup EXIT
    
    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Run health check
    if run_health_check; then
        send_notification "HEALTHY" "All systems operational"
        exit 0
    else
        send_notification "UNHEALTHY" "Some systems are experiencing issues"
        exit 1
    fi
}

# Handle different modes
case "${1:-check}" in
    "check")
        main
        ;;
    "monitor")
        log_message "INFO" "Starting continuous health monitoring"
        while true; do
            main
            sleep 300  # Check every 5 minutes
        done
        ;;
    "quick")
        check_http_endpoint "$HEALTH_CHECK_URL" "Django application"
        ;;
    *)
        echo "Usage: $0 {check|monitor|quick}"
        echo "  check   - Run single health check (default)"
        echo "  monitor - Run continuous health monitoring"
        echo "  quick   - Quick HTTP endpoint check only"
        exit 1
        ;;
esac