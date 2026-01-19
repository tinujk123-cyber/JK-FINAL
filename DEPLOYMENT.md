# Streamlit Cloud Deployment Guide

## Quick Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Your code pushed to a GitHub repository

---

## Option 1: Deploy from GitHub (Recommended)

### Step 1: Push Code to GitHub

If you haven't already pushed your code to GitHub:

```bash
# Make sure you're on the Veer branch
git branch

# Push to GitHub
git push -u origin Veer
```

### Step 2: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click "New app"
4. Fill in the details:
   - **Repository**: Select your repository (e.g., `tinujk123-cyber/JK-FINAL`)
   - **Branch**: `Veer`
   - **Main file path**: `streamlit_app.py`
5. Click "Deploy!"

### Step 3: Configure Secrets (If Needed)

If you need to add secrets (API keys, passwords):
1. Go to your app settings
2. Click "Secrets"
3. Add your secrets in TOML format:
```toml
ACCESS_PASSWORD = "JK2026"
```

---

## Option 2: Deploy Without GitHub Link Exposure

### Using Private Repository

1. **Make your GitHub repository private**:
   - Go to repository Settings
   - Scroll to "Danger Zone"
   - Click "Change visibility" → "Make private"

2. **Deploy from Streamlit Cloud**:
   - Streamlit Cloud can access private repositories
   - The GitHub link won't be publicly visible
   - Only you (the owner) can see the repository

### Using Streamlit Community Cloud Settings

The `.streamlit/config.toml` file we created will:
- ✅ Minimize the toolbar
- ✅ Hide detailed error messages
- ✅ Disable usage statistics
- ✅ Configure security settings

**Note**: Streamlit Cloud may still show a menu button, but the configuration minimizes what's exposed.

---

## Option 3: Self-Hosting (Complete Control)

For complete control over deployment without any GitHub links:

### Using Docker

1. **Create Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run**:
```bash
docker build -t jk-trinetra .
docker run -p 8501:8501 jk-trinetra
```

### Using Cloud Platforms

Deploy to:
- **Heroku**: Free tier available
- **AWS EC2**: Full control
- **Google Cloud Run**: Serverless
- **Azure App Service**: Enterprise-ready
- **DigitalOcean**: Simple and affordable

---

## Configuration Files Explained

### `.streamlit/config.toml`
This file controls:
- **UI Settings**: Minimizes toolbar and menu options
- **Security**: Enables XSRF protection
- **Privacy**: Disables usage statistics
- **Error Handling**: Hides detailed errors from users

### Key Settings for Privacy
```toml
[client]
toolbarMode = "minimal"          # Minimal toolbar
showErrorDetails = false         # Hide error details

[browser]
gatherUsageStats = false         # No telemetry

[server]
enableXsrfProtection = true      # Security enabled
```

---

## Post-Deployment Checklist

After deployment, verify:
- [ ] Application loads correctly
- [ ] Authentication works (password: JK2026)
- [ ] Stock data fetches properly
- [ ] All features work (scanners, analysis, etc.)
- [ ] GitHub link is not prominently displayed
- [ ] Menu is minimal
- [ ] Performance is acceptable

---

## Updating Your Deployment

### Streamlit Cloud
Automatically redeploys when you push to GitHub:
```bash
git add .
git commit -m "Update application"
git push origin Veer
```

### Self-Hosted
Rebuild and restart:
```bash
# Docker
docker build -t jk-trinetra .
docker stop <container-id>
docker run -p 8501:8501 jk-trinetra

# Direct
git pull origin Veer
streamlit run streamlit_app.py
```

---

## Troubleshooting

### Issue: GitHub Link Still Visible
**Solution**: 
- Use a private repository
- Self-host the application
- Contact Streamlit support for enterprise options

### Issue: Deployment Fails
**Solution**:
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility
- Check Streamlit Cloud logs

### Issue: Data Not Loading
**Solution**:
- Verify internet connection on server
- Check yfinance API is accessible
- Review application logs

---

## Security Best Practices

1. **Use Environment Variables** for sensitive data
2. **Enable HTTPS** in production
3. **Keep dependencies updated**
4. **Monitor access logs**
5. **Use strong passwords**
6. **Regular security audits**

---

## Cost Considerations

### Streamlit Cloud (Free Tier)
- ✅ Free for public apps
- ✅ 1 private app free
- ✅ Community support
- ❌ Limited resources
- ❌ May show Streamlit branding

### Self-Hosting
- 💰 Server costs ($5-50/month)
- ✅ Full control
- ✅ No branding
- ✅ Custom domain
- ❌ Requires maintenance

---

## Next Steps

1. Choose your deployment method
2. Push code to GitHub (if using Streamlit Cloud)
3. Deploy the application
4. Test all functionality
5. Share the URL with users
6. Monitor performance

---

## Support

For deployment issues:
- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Community: https://discuss.streamlit.io/
- GitHub Issues: Your repository issues page

---

**Your application is ready for deployment!** 🚀
