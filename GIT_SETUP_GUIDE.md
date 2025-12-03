# 📦 Complete Git Setup & Repository Guide

This guide will walk you through setting up Git, creating a repository, and pushing your project to GitHub.

## 🔧 Step 1: Install Git

### Windows
1. Download Git from [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Open "Git Bash" from Start menu

### macOS
```bash
# Using Homebrew
brew install git

# Or download from https://git-scm.com/download/mac
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install git
```

### Verify Installation
```bash
git --version
# Should output: git version 2.x.x
```

## 👤 Step 2: Configure Git

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your.email@example.com"

# Set default branch name to 'main'
git config --global init.defaultBranch main

# Verify configuration
git config --list
```

## 🌐 Step 3: Create GitHub Account & Repository

### A. Create GitHub Account
1. Go to [https://github.com](https://github.com)
2. Click "Sign up" and follow the process
3. Verify your email

### B. Create a New Repository
1. Click the "+" icon in top-right corner
2. Select "New repository"
3. Fill in details:
   - **Repository name**: `graph-coloring-frequency-assignment`
   - **Description**: "Advanced graph coloring for network frequency assignment"
   - **Visibility**: Public (or Private)
   - **❌ DO NOT** initialize with README (we'll push our own)
   - **❌ DO NOT** add .gitignore or license yet
4. Click "Create repository"

## 📁 Step 4: Organize Your Project Files

Create the following structure:

```
graph-coloring-frequency-assignment/
├── graph_coloring.py          # Main Python implementation
├── graph_coloring.cpp         # C++ implementation
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── .gitignore                 # Files to ignore
├── LICENSE                    # MIT License
├── tests/
│   ├── test_algorithms.py
│   └── benchmark.py
└── examples/
    └── basic_usage.py
```

## 🚀 Step 5: Initialize Git Repository (Terminal)

Open your terminal/command prompt in your project folder:

```bash
# Navigate to your project directory
cd /path/to/graph-coloring-frequency-assignment

# Initialize Git repository
git init

# Check status
git status
```

## 📝 Step 6: Create .gitignore File

Create a file named `.gitignore`:

```bash
# On Windows (Git Bash or PowerShell)
notepad .gitignore

# On macOS/Linux
nano .gitignore
```

Add this content:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# C++
*.o
*.out
*.exe
*.app
graph_coloring

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Output files
*.json
*.png
*.csv
!sample_networks/*.json

# Testing
.pytest_cache/
.coverage
htmlcov/

# Jupyter
.ipynb_checkpoints/
```

## ✅ Step 7: Stage and Commit Files

```bash
# Add all files to staging area
git add .

# Or add files individually
git add graph_coloring.py
git add README.md
git add requirements.txt

# Check what's staged
git status

# Commit with a message
git commit -m "Initial commit: Advanced graph coloring implementation"
```

## 🔗 Step 8: Connect to GitHub

Replace `USERNAME` with your GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/USERNAME/graph-coloring-frequency-assignment.git

# Verify remote was added
git remote -v
```

## 📤 Step 9: Push to GitHub

```bash
# Push to GitHub (first time)
git push -u origin main

# You may be prompted for GitHub credentials
# Use a Personal Access Token instead of password (see below)
```

### 🔐 Setting Up Authentication

GitHub no longer accepts passwords. Use one of these methods:

#### Method A: Personal Access Token (Recommended)
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: "Git Access"
4. Expiration: 90 days (or your preference)
5. Select scopes: ✅ **repo** (all options)
6. Click "Generate token"
7. **Copy the token immediately** (you won't see it again!)
8. Use this token as your password when pushing

#### Method B: SSH Keys
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Press Enter for default location
# Set a passphrase (or press Enter for none)

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key
# Paste the key and save

# Test connection
ssh -T git@github.com

# Change remote to SSH
git remote set-url origin git@github.com:USERNAME/graph-coloring-frequency-assignment.git
```

## 🔄 Step 10: Regular Git Workflow

### Making Changes

```bash
# 1. Check current status
git status

# 2. Make your changes to files
# (edit graph_coloring.py, etc.)

# 3. See what changed
git diff

# 4. Add changed files
git add graph_coloring.py
# or add all changes
git add .

# 5. Commit with descriptive message
git commit -m "Add Welsh-Powell algorithm optimization"

# 6. Push to GitHub
git push
```

### Useful Commands

```bash
# View commit history
git log
git log --oneline --graph --all

# Undo changes to a file (before staging)
git checkout -- filename.py

# Undo staging (after git add)
git reset filename.py

# Undo last commit (keeps changes)
git reset --soft HEAD~1

# Create a new branch
git branch feature-new-algorithm
git checkout feature-new-algorithm
# or combined:
git checkout -b feature-new-algorithm

# Switch branches
git checkout main

# Merge branch into main
git checkout main
git merge feature-new-algorithm

# Delete branch
git branch -d feature-new-algorithm

# Pull latest changes from GitHub
git pull
```

## 📋 Step 11: Add a LICENSE

Create `LICENSE` file:

```bash
# Download MIT License template
curl -o LICENSE https://raw.githubusercontent.com/licenses/license-templates/master/templates/mit.txt

# Or create manually and add this content:
```

```text
MIT License

Copyright (c) 2024 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Then commit and push:

```bash
git add LICENSE
git commit -m "Add MIT license"
git push
```

## 🎨 Step 12: Make Your Repository Look Professional

### Add Topics to Your Repository
On GitHub repository page:
1. Click the ⚙️ icon next to "About"
2. Add topics: `graph-theory`, `algorithms`, `network-optimization`, `python`, `cpp`, `frequency-assignment`
3. Add description and website URL

### Create CONTRIBUTING.md

```markdown
# Contributing to Graph Coloring Project

We welcome contributions! Here's how you can help:

## How to Contribute

1. Fork the repository
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write tests for your changes
5. Run tests: `pytest tests/`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Code Style

- Python: Follow PEP 8
- C++: Follow Google C++ Style Guide
- Add docstrings to all functions
- Write unit tests for new features

## Questions?

Open an issue on GitHub!
```

## 🚨 Common Issues & Solutions

### Issue: "Permission denied (publickey)"
**Solution**: Set up SSH keys (see Step 9, Method B)

### Issue: "Remote origin already exists"
**Solution**:
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/repo.git
```

### Issue: "Large files won't push"
**Solution**:
```bash
# Use Git LFS for files > 50MB
git lfs install
git lfs track "*.bin"
git add .gitattributes
git commit -m "Add Git LFS"
```

### Issue: "Merge conflicts"
**Solution**:
```bash
# Pull latest changes
git pull

# Manually edit conflicted files
# Look for <<<<<<, =======, >>>>>> markers

# After resolving
git add resolved_file.py
git commit -m "Resolve merge conflicts"
git push
```

## 📊 Step 13: Track Your Repository Stats

Add these badges to your README:

```markdown
![GitHub stars](https://img.shields.io/github/stars/USERNAME/graph-coloring-frequency-assignment)
![GitHub forks](https://img.shields.io/github/forks/USERNAME/graph-coloring-frequency-assignment)
![GitHub issues](https://img.shields.io/github/issues/USERNAME/graph-coloring-frequency-assignment)
![GitHub license](https://img.shields.io/github/license/USERNAME/graph-coloring-frequency-assignment)
```

## 🎯 Quick Reference Card

```bash
# Daily workflow
git status                    # Check what changed
git add .                     # Stage all changes
git commit -m "message"       # Commit changes
git push                      # Push to GitHub
git pull                      # Get latest changes

# Branching
git branch                    # List branches
git checkout -b new-branch    # Create & switch to branch
git checkout main             # Switch to main
git merge branch-name         # Merge branch

# Undo things
git checkout -- file          # Discard changes in file
git reset HEAD file           # Unstage file
git revert commit-hash        # Undo a commit

# Information
git log                       # View history
git diff                      # See changes
git remote -v                 # View remotes
```

## 🎓 Learn More

- **Official Git Docs**: [https://git-scm.com/doc](https://git-scm.com/doc)
- **GitHub Guides**: [https://guides.github.com](https://guides.github.com)
- **Interactive Tutorial**: [https://learngitbranching.js.org](https://learngitbranching.js.org)

---

**Congratulations! 🎉 Your project is now on GitHub!**

Your repository URL will be:
```
https://github.com/USERNAME/graph-coloring-frequency-assignment
```