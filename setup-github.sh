#!/bin/bash

echo "🚀 Setting up GitHub repository and Railway deployment..."

# Check if we're in the right directory
if [ ! -d "lead-intel-api" ]; then
    echo "❌ Error: lead-intel-api directory not found. Please run this from the language_mapper directory."
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Error: Git not initialized. Please run 'git init' first."
    exit 1
fi

echo "📋 Current status:"
git status

echo ""
echo "🔗 To create a GitHub repository and deploy:"
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create a new repository named 'lead-intel-api'"
echo "3. Make it PUBLIC (Railway needs public repos)"
echo "4. DON'T initialize with README, .gitignore, or license"
echo "5. Click 'Create repository'"
echo ""
echo "6. After creating the repo, run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/lead-intel-api.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "7. Then go to https://railway.app and:"
echo "   - Sign up/Login with GitHub"
echo "   - Click 'New Project'"
echo "   - Select 'Deploy from GitHub repo'"
echo "   - Choose your lead-intel-api repository"
echo "   - Railway will auto-deploy using the railway.json config"
echo ""

echo "✅ Your project is ready for deployment!"
echo "📁 Repository structure:"
ls -la lead-intel-api/

echo ""
echo "🔧 Railway configuration is already set up in lead-intel-api/railway.json"
echo "🐳 Dockerfile is ready for containerized deployment"
echo "📊 Health check endpoint: /health"
echo "🎯 Main API endpoint: /enrich_lead" 