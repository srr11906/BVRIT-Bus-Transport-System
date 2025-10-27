# Deployment Guide for BVRIT Transport Management System

## 🚀 Deployment Options

### Option 1: Railway (Recommended - Free & Easy)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your GitHub repository
4. Railway will automatically detect Flask and deploy
5. Set environment variable: `SESSION_SECRET=your-secret-key-here`

### Option 2: Render (Free Tier Available)
1. Go to [render.com](https://render.com)
2. Sign up and create new Web Service
3. Connect your GitHub repository
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: `Python 3`

### Option 3: Heroku (Paid but Reliable)
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`
5. Set config: `heroku config:set SESSION_SECRET=your-secret-key`

## 📁 Files Created for Deployment

- `requirements.txt` - Python dependencies
- `Procfile` - Process configuration for Heroku
- `runtime.txt` - Python version specification
- Updated `app.py` - Production-ready configuration

## 🔧 Environment Variables

Set these in your deployment platform:
- `SESSION_SECRET` - Random secret key for sessions
- `FLASK_ENV` - Set to `production` for production deployment
- `PORT` - Automatically set by the platform

## 🌐 After Deployment

Your app will be available at a public URL like:
- Railway: `https://your-app-name.railway.app`
- Render: `https://your-app-name.onrender.com`
- Heroku: `https://your-app-name.herokuapp.com`

## 🔑 Default Login Credentials

- **Admin**: username: `admin`, password: `admin123`
- **Student**: username: `24211A0538`, password: `student123`
- **Driver**: username: `9876543210`, password: `driver123`

## 📝 Notes

- The SQLite database will be created automatically on first run
- All data is stored in the database file
- For production, consider using PostgreSQL instead of SQLite
- Update default passwords before going live!
