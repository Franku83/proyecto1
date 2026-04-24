# Deployment Guide for Railway

This guide will help you deploy the Joyería API Django project to Railway.

## Prerequisites

1. Railway account ([railway.app](https://railway.app))
2. Railway CLI installed (optional but recommended)
3. Git repository pushed to GitHub/GitLab

## Quick Deploy

### Option 1: Using Railway CLI

1. **Login to Railway:**
   ```bash
   railway login
   ```

2. **Initialize project in Railway:**
   ```bash
   railway init
   ```

3. **Create PostgreSQL Database:**
   ```bash
   railway add --database postgres
   ```

4. **Set environment variables:**
   ```bash
   railway variables set SECRET_KEY='your-secret-key-here'
   railway variables set DEBUG=False
   railway variables set ALLOWED_HOSTS='your-railway-app-domain.com,*.up.railway.app'
   railway variables set CORS_ALLOWED_ORIGINS='your-frontend-domain.com'
   ```

5. **Deploy:**
   ```bash
   railway up
   ```

### Option 2: Using Railway Dashboard

1. **Connect Git Repository:**
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

2. **Add PostgreSQL Database:**
   - In your project dashboard, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway will automatically provision the database

3. **Configure Environment Variables:**
   Go to "Variables" and add:
   
   | Variable | Description | Example |
   |----------|-------------|---------|
   | `SECRET_KEY` | Django secret key | Use `django-admin generate-secret-key` or any 50+ char random string |
   | `DEBUG` | Debug mode | `False` (for production) |
   | `ALLOWED_HOSTS` | Allowed hosts | `*.up.railway.app,your-custom-domain.com` |
   | `CORS_ALLOWED_ORIGINS` | Frontend origins | `https://your-frontend.com,https://www.your-frontend.com` |
   | `GROQ_API_KEY` | Groq AI API key | `your-groq-api-key` |
   | `GROQ_MODEL` | AI Model | `llama3-8b-8192` |

4. **Deploy:**
   - Railway will auto-detect the Dockerfile and build your project
   - Click "Deploy" to trigger the deployment

## Environment Variables Required

Create a `.env` file locally for development (not committed to git):

```bash
# Django Settings
SECRET_KEY=your-secret-key-here-min-50-chars
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Railway will set this automatically in production)
DATABASE_URL=sqlite:///./db.sqlite3

# AI Integration
GROQ_API_KEY=your-groq-api-key-here
GROQ_MODEL=llama3-8b-8192

# CORS (for frontend apps)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Note:** Railway automatically sets `DATABASE_URL` when you add a PostgreSQL database.

## Post-Deployment

1. **Run Migrations (if needed):**
   ```bash
   railway run python manage.py migrate
   ```

2. **Create Superuser:**
   ```bash
   railway run python manage.py createsuperuser
   ```

3. **Access Logs:**
   ```bash
   railway logs
   ```

4. **Visit Your App:**
   - Railway provides a URL like `https://your-app.up.railway.app`
   - **API Root:** `https://your-app.up.railway.app/api/`
   - **Admin Panel:** `https://your-app.up.railway.app/admin/`

5. **Add Custom Domain (Optional):**
   - In Railway dashboard, go to "Settings" → "Custom Domains"
   - Add your domain and follow DNS configuration instructions

## Production Checklist

- [x] Set `DEBUG=False`
- [x] Set strong `SECRET_KEY`
- [x] Configure `ALLOWED_HOSTS`
- [x] Configure `CORS_ALLOWED_ORIGINS`
- [ ] Add custom domain (optional)
- [ ] Set up SSL/TLS certificates (automatic with Railway)
- [ ] Configure monitoring and alerts
- [ ] Test all API endpoints
- [ ] Load test the application

## Security Considerations

1. **Never commit `.env` file** - it's in `.gitignore`
2. **Use environment variables** - all sensitive settings read from env vars
3. **HTTPS only** - Railway provides automatic SSL
4. **Security headers** - configured in Django settings
5. **Database credentials** - managed securely by Railway

## Troubleshooting

### Common Issues

1. **Database connection errors:**
   - Ensure PostgreSQL database is provisioned
   - Check `DATABASE_URL` is set automatically by Railway

2. **Static files not loading:**
   - Run `railway run python manage.py collectstatic --no-input`
   - Check `STATIC_ROOT` is writable

3. **Allowed hosts error:**
   - Update `ALLOWED_HOSTS` variable with Railway-provided domain

4. **Build failures:**
   - Check build logs in Railway dashboard
   - Ensure all dependencies are in `requirements.txt`

### Debugging

```bash
# Check environment variables
railway variables

# Check logs
railway logs

# Run shell in production environment
railway run bash
```

## Scaling

If you need to scale your deployment:

- Upgrade to paid Railway plan for more resources
- Increase workers in Dockerfile's `gunicorn` command
- Consider Django-Q or Celery for background tasks
- Use Railway's horizontal scaling features

## Cost

Railway pricing:
- **Free tier:** Limited hours, good for testing
- **Developer:** ~$5/month per service
- **Team:** ~$19/month per member

Database costs depend on the plan chosen.
