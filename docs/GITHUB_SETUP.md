# GitHub Setup Guide

## Step 1: Create GitHub Repository

### Option A: Via GitHub Website (Recommended)

1. Go to [GitHub](https://github.com/)
2. Click "+" in top right → "New repository"
3. Fill in:
   - **Repository name**: `flight-search-wro-israel` (or your preferred name)
   - **Description**: "Automated flight search from Wrocław to Israel with smart constraint filtering"
   - **Visibility**: 
     - ✅ **Private** (recommended - contains your search patterns)
     - ⚠️ Public (only if you want to share publicly)
   - ✅ **Do NOT** initialize with README (we already have one)
4. Click "Create repository"

### Option B: Via GitHub CLI

```bash
# Install GitHub CLI first: https://cli.github.com/
gh repo create flight-search-wro-israel --private --source=. --remote=origin
```

## Step 2: Link Local Repository to GitHub

After creating the repository on GitHub, you'll see instructions. Use these commands:

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/flight-search-wro-israel.git

# Or if using SSH:
git remote add origin git@github.com:YOUR_USERNAME/flight-search-wro-israel.git

# Verify remote is added
git remote -v
```

## Step 3: Push Your Code

```bash
# Push to GitHub
git push -u origin master

# Or if you prefer main as branch name:
git branch -M main
git push -u origin main
```

## Step 4: Verify on GitHub

1. Go to your repository page
2. You should see all files uploaded
3. README.md should display automatically
4. Check that .gitignore is working (no .env files, etc.)

## Step 5: Set Up Secrets (for Phase 3)

For automated monitoring in Phase 3:

1. Go to your repository on GitHub
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret"
4. Add:
   - Name: `SERPAPI_KEY`
   - Value: Your actual SerpApi key
5. Click "Add secret"

**Important**: NEVER commit API keys directly in code!

## Project Structure on GitHub

Your repository should look like this:

```
flight-search-wro-israel/
├── .github/
│   └── workflows/
│       └── daily-search.yml     # Automated monitoring (Phase 3)
├── docs/
│   ├── QUICKSTART.md            # 5-minute setup guide
│   └── README_DETAILED.md       # Original detailed README
├── results/                     # Search results (gitignored)
├── .env.example                 # Example environment file
├── .gitignore                   # Git ignore rules
├── CHANGELOG.md                 # Version history
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # MIT License
├── README.md                    # Main GitHub README
├── config.ini                   # Configuration file
├── flight_search_poc.py         # Main search script
├── requirements.txt             # Python dependencies
└── test_setup.py                # Setup verification
```

## Managing Your Repository

### Daily Workflow

```bash
# Make changes to files
# ...

# Check what changed
git status

# Add changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push
```

### Creating Branches for Features

```bash
# Create new branch for Phase 2 work
git checkout -b phase2-date-range-search

# Make changes...
git add .
git commit -m "Add date range search functionality"

# Push branch to GitHub
git push -u origin phase2-date-range-search

# On GitHub, create Pull Request to merge into main
```

### Tagging Releases

```bash
# Tag current version
git tag -a v1.0.0 -m "Phase 1 POC Release"

# Push tag to GitHub
git push origin v1.0.0

# On GitHub, create Release from this tag
```

## Security Best Practices

### ✅ DO:
- Use `.env.example` as template
- Store actual keys in `.env` (gitignored)
- Use GitHub Secrets for automated workflows
- Keep repository private if it contains personal search patterns
- Review commits before pushing

### ❌ DON'T:
- Commit API keys to git
- Commit `.env` files
- Commit `results/` directory with personal data
- Make repository public with sensitive info

## Useful Git Commands

```bash
# View commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename

# Pull latest from GitHub
git pull

# Create .gitignore entry
echo "*.key" >> .gitignore

# View branches
git branch -a

# Switch branches
git checkout branch-name
```

## GitHub Features to Enable

### 1. Issues
Enable for:
- Bug tracking
- Feature requests
- To-do lists

### 2. Projects
Create project board for:
- Phase 2 tasks
- Phase 3 tasks
- Future enhancements

### 3. Wiki (Optional)
Document:
- API comparison results
- Price tracking insights
- Best booking time findings

### 4. GitHub Actions (Phase 3)
Enable for:
- Automated daily searches
- Price monitoring
- Email alerts

## Cloning to Another Machine

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/flight-search-wro-israel.git
cd flight-search-wro-israel

# Create .env from example
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_setup.py

# Run search
python flight_search_poc.py
```

## Troubleshooting

### Problem: "Permission denied (publickey)"
**Solution**: Set up SSH keys for GitHub
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH Keys → New SSH key
```

### Problem: "Remote origin already exists"
**Solution**: 
```bash
# Remove old remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/YOUR_USERNAME/repo.git
```

### Problem: ".env file got committed"
**Solution**:
```bash
# Remove from git (but keep file locally)
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from git"

# Push
git push
```

### Problem: "Large files slow down git"
**Solution**:
```bash
# Add to .gitignore
echo "results/*.json" >> .gitignore
echo "*.log" >> .gitignore

# Remove from git tracking
git rm --cached results/*.json

# Commit
git commit -m "Stop tracking result files"
```

## Next Steps

1. ✅ Repository created and pushed
2. ⏭️ Start working on Phase 2 features
3. ⏭️ Create issues for planned features
4. ⏭️ Set up project board for task tracking

## Resources

- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Docs](https://docs.github.com/)
- [GitHub CLI](https://cli.github.com/)
- [SSH Key Setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

**Ready to push to GitHub?** Follow Step 1-3 above!
