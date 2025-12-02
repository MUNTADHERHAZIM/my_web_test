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



---

<div align="center">

**صُنع بـ ❤️ في العراق | Made with ❤️ in Iraq**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=muntazir.personal-website)
![GitHub stars](https://img.shields.io/github/stars/muntazir/personal-website?style=social)
![GitHub forks](https://img.shields.io/github/forks/muntazir/personal-website?style=social)

</div>
