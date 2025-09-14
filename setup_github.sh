#!/bin/bash

# Setup script for deploying Intent-Based Maps Search to GitHub

echo "🚀 Setting up Intent-Based Maps Search for GitHub deployment..."

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Intent-Based Maps Search MVP

- Natural language query parsing
- Location extraction and geocoding
- Midpoint calculation between locations
- Constraint-based filtering
- Mock data integration
- Streamlit web interface
- Free demo without API keys"

echo "✅ Git repository initialized"

# Create .gitignore
cat > .gitignore << EOF
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
EOF

echo "✅ .gitignore created"

# Add .gitignore
git add .gitignore
git commit -m "Add .gitignore"

echo "✅ Repository ready for GitHub!"

echo ""
echo "📋 Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/intent-maps-search.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy to Streamlit Cloud:"
echo "   - Go to https://share.streamlit.io"
echo "   - Connect your GitHub repository"
echo "   - Set main file: streamlit_demo.py"
echo "   - Deploy!"
echo ""
echo "4. Update LinkedIn post with your deployment URL"
echo ""
echo "🎉 Ready to share your Intent-Based Maps Search demo!"
