# موقع منتظر حازم ثامر الشخصي
# Muntazir Hazim Thamir Personal Website

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

</div>

## 📋 نظرة عامة | Overview

**العربية:**
موقع شخصي متطور لمنتظر حازم ثامر مبني بـ Django مع دعم كامل للغتين العربية والإنجليزية. يتضمن الموقع مدونة شخصية، معرض للمشاريع، ونظام إدارة محتوى متقدم.

**English:**
A modern personal website for Muntazir Hazim Thamir built with Django featuring full Arabic and English language support. The website includes a personal blog, project portfolio, and advanced content management system.

## ✨ المميزات | Features

### 🌐 متعدد اللغات | Multilingual
- دعم كامل للعربية والإنجليزية | Full Arabic and English support
- تبديل اللغة الديناميكي | Dynamic language switching
- دعم RTL/LTR | RTL/LTR support
- ترجمة شاملة للواجهات | Complete UI translation

### 🎨 التصميم | Design
- تصميم متجاوب بالكامل | Fully responsive design
- دعم الوضع الليلي/النهاري | Dark/Light mode support
- واجهة مستخدم حديثة مع Tailwind CSS | Modern UI with Tailwind CSS
- تحسين لمحركات البحث (SEO) | SEO optimized
- دعم Open Graph و Twitter Cards | Open Graph & Twitter Cards support

### 📝 المدونة | Blog
- نظام مقالات متقدم | Advanced article system
- دعم Markdown | Markdown support
- نظام التصنيفات والعلامات | Categories and tags system
- نظام التعليقات | Comments system
- البحث المتقدم | Advanced search
- أرشيف زمني | Time-based archive

### 👤 إدارة المستخدمين | User Management
- نظام تسجيل دخول متقدم | Advanced authentication system
- لوحة تحكم المستخدم | User dashboard
- إدارة الملف الشخصي | Profile management
- استعادة كلمة المرور | Password recovery
- نظام الأذونات | Permissions system

### 🚀 الأداء | Performance
- تخزين مؤقت متقدم مع Redis | Advanced caching with Redis
- ضغط الملفات الثابتة | Static files compression
- تحسين الصور | Image optimization
- CDN جاهز | CDN ready
- مراقبة الأداء | Performance monitoring

### 🔒 الأمان | Security
- حماية CSRF | CSRF protection
- تشفير كلمات المرور | Password encryption
- حماية من هجمات XSS | XSS protection
- رؤوس أمان HTTP | Security HTTP headers
- تسجيل العمليات الأمنية | Security logging

### 📊 المراقبة | Monitoring
- نظام السجلات المتقدم | Advanced logging system
- مراقبة الصحة | Health monitoring
- إحصائيات الاستخدام | Usage analytics
- تنبيهات النظام | System alerts
- نسخ احتياطية تلقائية | Automatic backups

## 🛠️ التقنيات المستخدمة | Technologies Used

### Backend
- **Django 4.2+** - إطار العمل الرئيسي | Main framework
- **Python 3.11+** - لغة البرمجة | Programming language
- **PostgreSQL** - قاعدة البيانات | Database
- **Redis** - التخزين المؤقت | Caching
- **Celery** - المهام غير المتزامنة | Asynchronous tasks
- **Gunicorn** - خادم WSGI | WSGI server

### Frontend
- **Tailwind CSS** - إطار عمل CSS | CSS framework
- **Alpine.js** - JavaScript framework
- **Chart.js** - الرسوم البيانية | Charts
- **Prism.js** - تمييز الكود | Code highlighting

### DevOps & Deployment
- **Docker & Docker Compose** - الحاويات | Containerization
- **Nginx** - الخادم العكسي | Reverse proxy
- **Supervisor** - إدارة العمليات | Process management
- **Elasticsearch** - البحث المتقدم | Advanced search
- **Prometheus & Grafana** - المراقبة | Monitoring

## 📦 متطلبات النظام | System Requirements

### الحد الأدنى | Minimum
- **CPU:** 1 core
- **RAM:** 1GB
- **Storage:** 10GB
- **Python:** 3.11+
- **PostgreSQL:** 13+
- **Redis:** 6+

### الموصى به | Recommended
- **CPU:** 2+ cores
- **RAM:** 4GB+
- **Storage:** 50GB+ SSD
- **Python:** 3.11+
- **PostgreSQL:** 15+
- **Redis:** 7+

## 🚀 التثبيت والتشغيل | Installation & Setup

### 1. استنساخ المشروع | Clone Repository

```bash
git clone https://github.com/muntazir/personal-website.git
cd personal-website
```

### 2. التشغيل باستخدام Docker (الطريقة الموصى بها) | Docker Setup (Recommended)

#### التطوير | Development

```bash
# إنشاء ملف البيئة | Create environment file
cp .env.example .env

# تحرير متغيرات البيئة | Edit environment variables
nano .env

# بناء وتشغيل الحاويات | Build and run containers
docker-compose up -d

# تشغيل الترحيلات | Run migrations
docker-compose exec web python manage.py migrate

# إنشاء مستخدم إداري | Create superuser
docker-compose exec web python manage.py createsuperuser

# جمع الملفات الثابتة | Collect static files
docker-compose exec web python manage.py collectstatic
```

#### الإنتاج | Production

```bash
# استخدام ملف الإنتاج | Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# أو استخدام النص البرمجي | Or use the script
./scripts/deploy.sh
```

### 3. التثبيت اليدوي | Manual Installation

#### إعداد البيئة الافتراضية | Virtual Environment Setup

```bash
# إنشاء البيئة الافتراضية | Create virtual environment
python -m venv venv

# تفعيل البيئة الافتراضية | Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# تثبيت المتطلبات | Install requirements
pip install -r requirements.txt
```

#### إعداد قاعدة البيانات | Database Setup

```bash
# PostgreSQL
sudo -u postgres createdb muntazir_portfolio
sudo -u postgres createuser muntazir_user
sudo -u postgres psql -c "ALTER USER muntazir_user PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE muntazir_portfolio TO muntazir_user;"
```

#### إعداد متغيرات البيئة | Environment Variables

```bash
# إنشاء ملف .env | Create .env file
cp .env.example .env

# تحرير المتغيرات | Edit variables
nano .env
```

#### تشغيل التطبيق | Run Application

```bash
# تشغيل الترحيلات | Run migrations
python manage.py migrate

# إنشاء مستخدم إداري | Create superuser
python manage.py createsuperuser

# جمع الملفات الثابتة | Collect static files
python manage.py collectstatic

# تشغيل الخادم | Run server
python manage.py runserver
```

## ⚙️ التكوين | Configuration

### متغيرات البيئة الأساسية | Essential Environment Variables

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SETTINGS_MODULE=muntazir_portfolio.settings.prod

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Media & Static
STATIC_URL=/static/
MEDIA_URL=/media/
STATIC_ROOT=/app/staticfiles
MEDIA_ROOT=/app/media

# Internationalization
LANGUAGE_CODE=ar
TIME_ZONE=Asia/Baghdad
USE_I18N=True
USE_L10N=True
USE_TZ=True

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/django.log

# Monitoring
SENTRY_DSN=your-sentry-dsn
GOOGLE_ANALYTICS_ID=your-ga-id
```

### إعدادات Nginx | Nginx Configuration

```nginx
# ملف /etc/nginx/sites-available/muntazir-portfolio
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /app/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /app/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

## 🔧 أوامر الإدارة | Management Commands

### أوامر Django المخصصة | Custom Django Commands

```bash
# تنظيف الملفات المؤقتة | Clean temporary files
python manage.py cleanup_temp_files

# تحديث فهرس البحث | Update search index
python manage.py update_search_index

# إنشاء نسخة احتياطية | Create backup
python manage.py create_backup

# استعادة النسخة الاحتياطية | Restore backup
python manage.py restore_backup backup_file.sql

# تحديث الإحصائيات | Update statistics
python manage.py update_stats

# إرسال رسائل البريد المؤجلة | Send queued emails
python manage.py send_queued_mail

# تحسين قاعدة البيانات | Optimize database
python manage.py optimize_db

# تنظيف السجلات القديمة | Clean old logs
python manage.py clean_old_logs
```

### أوامر Docker | Docker Commands

```bash
# عرض السجلات | View logs
docker-compose logs -f web

# الدخول إلى الحاوية | Enter container
docker-compose exec web bash

# إعادة تشغيل الخدمات | Restart services
docker-compose restart

# تحديث الصور | Update images
docker-compose pull
docker-compose up -d

# تنظيف الحاويات القديمة | Clean old containers
docker system prune -a

# نسخ احتياطية | Backup
docker-compose exec db pg_dump -U postgres muntazir_portfolio > backup.sql

# استعادة النسخة الاحتياطية | Restore backup
docker-compose exec -T db psql -U postgres muntazir_portfolio < backup.sql
```

## 📊 المراقبة والصيانة | Monitoring & Maintenance

### فحص صحة النظام | Health Checks

```bash
# فحص صحة التطبيق | Application health check
curl http://localhost:8000/health/

# فحص قاعدة البيانات | Database health check
python manage.py dbshell --command="SELECT 1;"

# فحص Redis | Redis health check
redis-cli ping

# فحص مساحة القرص | Disk space check
df -h

# فحص استخدام الذاكرة | Memory usage check
free -h

# فحص العمليات | Process check
ps aux | grep python
```

### السجلات | Logs

```bash
# سجلات Django | Django logs
tail -f /app/logs/django.log

# سجلات Nginx | Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# سجلات PostgreSQL | PostgreSQL logs
tail -f /var/log/postgresql/postgresql-*.log

# سجلات Redis | Redis logs
tail -f /var/log/redis/redis-server.log
```

### النسخ الاحتياطية | Backups

```bash
# نسخة احتياطية يومية | Daily backup
#!/bin/bash
BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# قاعدة البيانات | Database
pg_dump -U postgres muntazir_portfolio > $BACKUP_DIR/database.sql

# الملفات | Files
tar -czf $BACKUP_DIR/media.tar.gz /app/media/
tar -czf $BACKUP_DIR/static.tar.gz /app/staticfiles/

# تنظيف النسخ القديمة | Clean old backups
find /backups/ -type d -mtime +30 -exec rm -rf {} \;
```

## 🔍 استكشاف الأخطاء | Troubleshooting

### مشاكل شائعة | Common Issues

#### 1. خطأ في الاتصال بقاعدة البيانات | Database Connection Error

```bash
# فحص حالة PostgreSQL | Check PostgreSQL status
sudo systemctl status postgresql

# إعادة تشغيل PostgreSQL | Restart PostgreSQL
sudo systemctl restart postgresql

# فحص الاتصال | Test connection
psql -h localhost -U muntazir_user -d muntazir_portfolio
```

#### 2. مشاكل الملفات الثابتة | Static Files Issues

```bash
# إعادة جمع الملفات الثابتة | Recollect static files
python manage.py collectstatic --clear --noinput

# فحص الأذونات | Check permissions
ls -la /app/staticfiles/
chmod -R 755 /app/staticfiles/
```

#### 3. مشاكل Redis | Redis Issues

```bash
# فحص حالة Redis | Check Redis status
sudo systemctl status redis

# إعادة تشغيل Redis | Restart Redis
sudo systemctl restart redis

# فحص الاتصال | Test connection
redis-cli ping
```

#### 4. مشاكل الأذونات | Permission Issues

```bash
# إصلاح أذونات الملفات | Fix file permissions
sudo chown -R www-data:www-data /app/
sudo chmod -R 755 /app/
sudo chmod -R 644 /app/logs/
```

### سجلات الأخطاء | Error Logs

```bash
# عرض آخر الأخطاء | Show recent errors
tail -100 /app/logs/django.log | grep ERROR

# البحث عن أخطاء محددة | Search for specific errors
grep -r "500 Internal Server Error" /app/logs/

# تحليل أخطاء Nginx | Analyze Nginx errors
tail -100 /var/log/nginx/error.log
```

## 🚀 النشر | Deployment

### النشر على خادم Ubuntu | Ubuntu Server Deployment

```bash
# تحديث النظام | Update system
sudo apt update && sudo apt upgrade -y

# تثبيت المتطلبات | Install requirements
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx git

# تثبيت Docker | Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# تثبيت Docker Compose | Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# استنساخ المشروع | Clone project
git clone https://github.com/muntazir/personal-website.git
cd personal-website

# إعداد البيئة | Setup environment
cp .env.example .env
nano .env

# تشغيل التطبيق | Run application
docker-compose -f docker-compose.prod.yml up -d
```

### النشر على AWS | AWS Deployment

```bash
# إنشاء EC2 instance
# - Ubuntu 22.04 LTS
# - t3.medium أو أكبر
# - 20GB+ storage
# - Security groups: 80, 443, 22

# الاتصال بالخادم | Connect to server
ssh -i your-key.pem ubuntu@your-server-ip

# تشغيل نص التثبيت | Run installation script
wget https://raw.githubusercontent.com/muntazir/personal-website/main/scripts/aws-deploy.sh
chmod +x aws-deploy.sh
./aws-deploy.sh
```

### النشر على DigitalOcean | DigitalOcean Deployment

```bash
# إنشاء Droplet
# - Ubuntu 22.04 LTS
# - 2GB RAM أو أكبر
# - 50GB+ storage

# استخدام Docker One-Click App أو التثبيت اليدوي
# Manual installation similar to Ubuntu deployment
```

## 📈 تحسين الأداء | Performance Optimization

### تحسين قاعدة البيانات | Database Optimization

```sql
-- إنشاء فهارس | Create indexes
CREATE INDEX CONCURRENTLY idx_blog_post_published ON blog_post(published_date) WHERE is_published = true;
CREATE INDEX CONCURRENTLY idx_blog_post_slug ON blog_post(slug);
CREATE INDEX CONCURRENTLY idx_blog_post_category ON blog_post(category_id);

-- تحليل الجداول | Analyze tables
ANALYZE;

-- تنظيف قاعدة البيانات | Vacuum database
VACUUM ANALYZE;
```

### تحسين Redis | Redis Optimization

```redis
# إعدادات Redis | Redis settings
maxmemory 1gb
maxmemory-policy allkeys-lru
save 900 1
save 300 10
save 60 10000
```

### تحسين Nginx | Nginx Optimization

```nginx
# ضغط الملفات | File compression
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

# التخزين المؤقت | Caching
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# حد معدل الطلبات | Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

## 🔐 الأمان | Security

### قائمة فحص الأمان | Security Checklist

- [ ] تحديث جميع المكتبات | Update all dependencies
- [ ] استخدام HTTPS | Use HTTPS
- [ ] تفعيل CSRF protection
- [ ] تفعيل XSS protection
- [ ] إعداد Security Headers
- [ ] تشفير كلمات المرور | Encrypt passwords
- [ ] تحديد الأذونات بدقة | Set precise permissions
- [ ] مراقبة السجلات | Monitor logs
- [ ] نسخ احتياطية منتظمة | Regular backups
- [ ] فحص الثغرات الأمنية | Security vulnerability scanning

### أوامر الأمان | Security Commands

```bash
# فحص الثغرات الأمنية | Security audit
pip-audit

# فحص إعدادات Django | Django security check
python manage.py check --deploy

# تحديث المكتبات | Update dependencies
pip list --outdated
pip install --upgrade package_name

# فحص الملفات المشبوهة | Check suspicious files
find /app -name "*.php" -o -name "*.jsp" -o -name "*.asp"

# مراقبة محاولات الدخول | Monitor login attempts
grep "Failed password" /var/log/auth.log
```

## 📚 الوثائق الإضافية | Additional Documentation

### روابط مفيدة | Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### ملفات التكوين | Configuration Files

```
project/
├── .env.example              # مثال متغيرات البيئة
├── docker-compose.yml        # تكوين Docker للتطوير
├── docker-compose.prod.yml   # تكوين Docker للإنتاج
├── Dockerfile               # ملف بناء الحاوية
├── requirements.txt         # متطلبات Python
├── nginx.conf              # تكوين Nginx
├── supervisord.conf        # تكوين Supervisor
└── scripts/                # نصوص الأتمتة
    ├── deploy.sh           # نص النشر
    ├── backup.sh           # نص النسخ الاحتياطية
    └── health-check.sh     # نص فحص الصحة
```

## 🤝 المساهمة | Contributing

### كيفية المساهمة | How to Contribute

1. **Fork المشروع | Fork the project**
2. **إنشاء فرع جديد | Create a new branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **إضافة التغييرات | Commit changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **رفع التغييرات | Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **إنشاء Pull Request | Create Pull Request**

### معايير الكود | Code Standards

- استخدام Black لتنسيق الكود | Use Black for code formatting
- اتباع PEP 8 | Follow PEP 8
- كتابة اختبارات للميزات الجديدة | Write tests for new features
- توثيق الكود | Document code
- استخدام رسائل commit واضحة | Use clear commit messages

```bash
# تنسيق الكود | Format code
black .
isort .
flake8 .

# تشغيل الاختبارات | Run tests
python manage.py test
pytest

# فحص التغطية | Check coverage
coverage run --source='.' manage.py test
coverage report
```

## 📄 الترخيص | License

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 التواصل | Contact

**منتظر حازم ثامر | Muntazir Hazim Thamir**

- 📧 Email: muntazir@example.com
- 🌐 Website: [muntazir.com](https://muntazir.com)
- 💼 LinkedIn: [muntazir-hazim-thamir](https://linkedin.com/in/muntazir-hazim-thamir)
- 🐙 GitHub: [muntazir](https://github.com/muntazir)

---

<div align="center">

**صُنع بـ ❤️ في العراق | Made with ❤️ in Iraq**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=muntazir.personal-website)
![GitHub stars](https://img.shields.io/github/stars/muntazir/personal-website?style=social)
![GitHub forks](https://img.shields.io/github/forks/muntazir/personal-website?style=social)

</div>