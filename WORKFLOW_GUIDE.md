# Complete Setup Guide - Multi-Model AI Workflow

## Phase 1: Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with WSL
- **Python:** 3.10 or higher
- **Git:** Latest version
- **Internet:** Stable connection for API calls

### Check Python Installation
```bash
python --version  # Should be 3.10+
pip --version
```

---

## Phase 2: Repository Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/krish25269-svg/Summer_2026.git
cd Summer_2026
```

### Step 2: Create Virtual Environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed pandas-2.0.3 python-dotenv-1.0.0 openai-1.3.5 ...
```

---

## Phase 3: API Key Configuration

### Get OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. Copy the key (format: `sk-...`)
4. Save it safely

### Get Anthropic Claude API Key
1. Go to: https://console.anthropic.com
2. Navigate to API settings
3. Create new API key
4. Copy the key (format: `sk-ant-...`)
5. Save it safely

### Get Google Gemini API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Get API Key"**
3. Create new project (if needed)
4. Copy the API key
5. Save it safely

---

## Phase 4: Environment Configuration

### Create .env File
```bash
cp .env.example .env
```

### Edit .env File
```bash
# Using nano editor (macOS/Linux)
nano .env

# Using Notepad (Windows)
notepad .env
```

### Add Your API Keys
```env
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
GOOGLE_API_KEY=your-actual-google-key-here

# Keep other settings as default for now
EXECUTION_MODE=parallel
LOG_LEVEL=INFO
```

### Verify .env File
```bash
cat .env  # Display contents to verify
```

⚠️ **Important:** Never commit `.env` to Git! It's in `.gitignore`

---

## Phase 5: Dataset Setup

### Option A: Using Kaggle CLI (Recommended)

#### Install Kaggle CLI
```bash
pip install kaggle
```

#### Configure Kaggle Credentials
1. Go to: https://www.kaggle.com/account
2. Scroll to **API** section
3. Click **"Create New API Token"**
4. This downloads `kaggle.json`
5. Move it to correct location:

```bash
# macOS / Linux
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Windows
mkdir %USERPROFILE%\.kaggle
move %USERPROFILE%\Downloads\kaggle.json %USERPROFILE%\.kaggle\
```

#### Download Dataset
```bash
mkdir -p data
kaggle datasets download -d ronakbokaria/myntra-products-dataset -p data/
unzip data/myntra-products-dataset.zip -d data/
rm data/myntra-products-dataset.zip
```

### Option B: Manual Download

1. Go to: https://www.kaggle.com/datasets/ronakbokaria/myntra-products-dataset
2. Click **"Download"** button
3. Extract the ZIP file
4. Move `myntra_products.csv` to `data/` folder

### Verify Dataset
```bash
ls -lh data/myntra_products.csv
wc -l data/myntra_products.csv  # Count rows
```

**Expected:** CSV file with ~13,000 rows

---

## Phase 6: Local Testing

### Test Individual Components

#### Test 1: Verify Imports
```bash
python -c "import openai; import anthropic; import google.generativeai; print('✓ All APIs imported successfully')"
```

#### Test 2: Test Environment Loading
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'✓ OpenAI key loaded: {bool(os.getenv(\"OPENAI_API_KEY\"))}')"
```

#### Test 3: Test Dataset Loading
```python
import pandas as pd

df = pd.read_csv('data/myntra_products.csv')
print(f"✓ Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
print(df.head())
```

### Run Full Workflow
```bash
python multi_model_workflow.py
```

**Expected Output:**
```
INFO:__main__:✓ Dataset loaded: 13000 products
INFO:__main__:🔄 Running all models in parallel...
INFO:__main__:✓ GPT processed successfully
INFO:__main__:✓ Claude processed successfully
INFO:__main__:✓ Gemini processed successfully
INFO:__main__:✓ Workflow completed!
```

### View Results
```bash
# JSON results
cat results/report.json

# HTML report
open results/report.html  # macOS
xdg-open results/report.html  # Linux
start results/report.html  # Windows
```

---

## Phase 7: GitHub Secrets Setup (For CI/CD)

### Add Secrets to Repository

1. Go to: https://github.com/krish25269-svg/Summer_2026
2. Click **Settings** tab
3. Navigate to: **Secrets and variables → Actions**
4. Click **"New repository secret"**

### Add Each Secret

#### Secret 1: OPENAI_API_KEY
- **Name:** `OPENAI_API_KEY`
- **Value:** Your OpenAI API key
- Click **"Add secret"**

#### Secret 2: ANTHROPIC_API_KEY
- **Name:** `ANTHROPIC_API_KEY`
- **Value:** Your Anthropic API key
- Click **"Add secret"**

#### Secret 3: GOOGLE_API_KEY
- **Name:** `GOOGLE_API_KEY`
- **Value:** Your Google API key
- Click **"Add secret"**

#### Secret 4 (Optional): KAGGLE_USERNAME & KAGGLE_KEY
- For automatic dataset downloads

### Verify Secrets
Go to **Settings → Secrets** to confirm all 3 are added.

---

## Phase 8: Running GitHub Actions Workflow

### Manual Trigger

1. Go to your repository
2. Click **Actions** tab
3. Select **"Multi-Model AI Workflow"**
4. Click **"Run workflow"** button
5. Select branch (keep as `main`)
6. Click **"Run workflow"**

### Monitor Execution

1. Wait for workflow to start (~5 seconds)
2. Click on the running workflow
3. Click on the **"workflow"** job
4. Watch logs in real-time
5. Check for ✅ (success) or ❌ (failure)

### Download Results

1. Once complete, scroll down to **Artifacts**
2. Download:
   - `workflow-results` (JSON/HTML reports)
   - `workflow-logs` (execution logs)

### Automatic Schedule

The workflow runs **daily at midnight UTC** automatically!

---

## Phase 9: Troubleshooting

### Issue 1: "API Key Not Found"
```
Error: OpenAI API key not found
```
**Solution:**
```bash
# Verify .env file exists
ls -la .env

# Check key is set
grep OPENAI_API_KEY .env

# Reload environment
source venv/bin/activate
```

### Issue 2: "Module Not Found"
```
ModuleNotFoundError: No module named 'openai'
```
**Solution:**
```bash
pip install -r requirements.txt
pip list | grep openai  # Verify installation
```

### Issue 3: "Dataset Not Found"
```
FileNotFoundError: data/myntra_products.csv not found
```
**Solution:**
```bash
mkdir -p data
# Download dataset using steps above
ls -la data/myntra_products.csv
```

### Issue 4: "API Rate Limit"
```
RateLimitError: Rate limit exceeded
```
**Solution:**
- Wait 1-2 minutes before retrying
- Reduce sample size in `.env`
- Upgrade API plan

### Issue 5: "Timeout Error"
```
TimeoutError: Request timed out
```
**Solution:**
- Increase `TIMEOUT_SECONDS` in `.env`
- Check internet connection
- Retry the request

---

## Phase 10: Verification Checklist

Before considering setup complete:

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file created with API keys
- [ ] Dataset downloaded to `data/` folder
- [ ] Local test successful (`python multi_model_workflow.py`)
- [ ] Results generated (`results/report.json` exists)
- [ ] GitHub secrets added (3 secrets visible in Settings)
- [ ] GitHub Actions workflow accessible
- [ ] Test workflow run successful

---

## Quick Reference Commands

### Activate Environment
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### Run Workflow
```bash
python multi_model_workflow.py
```

### View Logs
```bash
tail -f logs/workflow.log
```

### Check Dataset
```bash
wc -l data/myntra_products.csv
head -5 data/myntra_products.csv
```

### Clear Results
```bash
rm -rf results/*
```

### Deactivate Environment
```bash
deactivate
```

---

## Support & Resources

- **Repository:** https://github.com/krish25269-svg/Summer_2026
- **Dataset:** https://www.kaggle.com/datasets/ronakbokaria/myntra-products-dataset
- **OpenAI Docs:** https://platform.openai.com/docs
- **Claude Docs:** https://docs.anthropic.com
- **Gemini Docs:** https://ai.google.dev

---

**Status:** ✅ Complete Setup Guide  
**Last Updated:** 2026-05-14  
**Version:** 1.0
