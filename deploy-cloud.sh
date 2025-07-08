#!/bin/bash

# Cloud Deployment Helper Script
# This script helps you prepare and deploy to cloud platforms

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}☁️  Lead Intel API - Cloud Deployment Helper${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    print_error "Please run this script from the lead-intel-api directory"
    exit 1
fi

# Pre-deployment checks
print_status "Running pre-deployment checks..."

# Check if tests pass
if python -m pytest tests/ -v > /dev/null 2>&1; then
    print_status "All tests passing"
else
    print_error "Tests are failing. Please fix them before deployment."
    exit 1
fi

# Check if Docker builds
if docker build -t lead-intel-api . > /dev/null 2>&1; then
    print_status "Docker build successful"
else
    print_error "Docker build failed. Please check your Dockerfile."
    exit 1
fi

# Check if code is committed
if git status --porcelain | grep -q .; then
    print_warning "You have uncommitted changes. Consider committing them before deployment."
    echo "Uncommitted files:"
    git status --porcelain
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    print_status "All changes committed"
fi

echo ""
echo -e "${BLUE}🚀 Choose your deployment platform:${NC}"
echo ""
echo "1. Railway (Recommended - Easiest)"
echo "2. Render (Free tier available)"
echo "3. Heroku (Industry standard)"
echo "4. Manual deployment instructions"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}🚂 Railway Deployment${NC}"
        echo ""
        echo "1. Go to https://railway.app"
        echo "2. Sign up/Login with GitHub"
        echo "3. Click 'Deploy from GitHub repo'"
        echo "4. Select this repository"
        echo "5. Railway will automatically detect the Dockerfile"
        echo "6. Wait for deployment to complete"
        echo "7. Get your public URL from the dashboard"
        echo ""
        print_status "Railway will handle everything automatically!"
        ;;
    2)
        echo ""
        echo -e "${BLUE}🎨 Render Deployment${NC}"
        echo ""
        echo "1. Go to https://render.com"
        echo "2. Sign up/Login with GitHub"
        echo "3. Click 'New Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Configure:"
        echo "   - Name: lead-intel-api"
        echo "   - Environment: Python"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port \$PORT"
        echo "6. Click 'Create Web Service'"
        echo ""
        print_status "Render will deploy your app automatically!"
        ;;
    3)
        echo ""
        echo -e "${BLUE}🦸 Heroku Deployment${NC}"
        echo ""
        echo "1. Install Heroku CLI: brew install heroku/brew/heroku"
        echo "2. Login: heroku login"
        echo "3. Create app: heroku create lead-intel-api"
        echo "4. Deploy: git push heroku main"
        echo "5. Open app: heroku open"
        echo ""
        print_status "Heroku will deploy your app!"
        ;;
    4)
        echo ""
        echo -e "${BLUE}📖 Manual Instructions${NC}"
        echo ""
        echo "See CLOUD_DEPLOYMENT.md for detailed instructions"
        echo "See POSTMAN_CLOUD.md for cURL commands"
        echo ""
        ;;
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}📋 Post-Deployment Checklist:${NC}"
echo ""
echo "1. Get your app URL from the platform dashboard"
echo "2. Test health check: curl https://YOUR_APP_URL/health"
echo "3. Test API: Use commands from POSTMAN_CLOUD.md"
echo "4. Update your Postman collection with the new URL"
echo "5. Share the URL with your team"
echo ""

print_status "Your Lead Intel API will be accessible from anywhere! 🌍"

echo ""
echo -e "${YELLOW}💡 Pro Tips:${NC}"
echo "- Set up environment variables in your cloud platform"
echo "- Monitor logs for any issues"
echo "- Set up alerts for downtime"
echo "- Consider setting up a custom domain"
echo "" 