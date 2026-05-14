# Multi-Model AI Workflow for Myntra Dataset

## 🚀 Overview

This project orchestrates **multiple AI models** (GPT, Claude, Gemini) to process and analyze the **Myntra Products Dataset** from Kaggle.

**Key Features:**
- ✅ Multi-model orchestration (GPT-4, Claude-3, Gemini-Pro)
- ✅ 3 execution modes: Parallel, Sequential, Ensemble
- ✅ GitHub Actions CI/CD automation
- ✅ Comprehensive reporting (JSON + HTML)
- ✅ Async processing for performance

---

## 📊 Dataset

**Source:** [Myntra Products Dataset](https://www.kaggle.com/datasets/ronakbokaria/myntra-products-dataset)

**Columns:**
- ProductName
- Brand
- Price
- Category
- Reviews
- Description
- etc.

---

## 🛠️ Quick Start

### 1️⃣ Clone Repository
```bash
git clone https://github.com/krish25269-svg/Summer_2026.git
cd Summer_2026
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure API Keys
```bash
cp .env.example .env
# Edit .env with your API keys:
# - OpenAI: https://platform.openai.com/api-keys
# - Anthropic: https://console.anthropic.com
# - Google: https://makersuite.google.com/app/apikey
```

### 4️⃣ Download Dataset
```bash
# Option A: Using Kaggle CLI
kaggle datasets download -d ronakbokaria/myntra-products-dataset -p data/ --unzip

# Option B: Manual download from Kaggle website
# Place myntra_products.csv in the data/ folder
```

### 5️⃣ Run Workflow
```bash
python multi_model_workflow.py
```

### 6️⃣ View Results
```bash
# JSON results
cat results/report.json

# HTML report (open in browser)
open results/report.html
```

---

## 🔄 Execution Modes

| Mode | Speed | Use Case |
|------|-------|----------|
| **Parallel** | ⚡ 5-10s | Fast independent analysis from all models |
| **Sequential** | ⏱️ 15-20s | Cascading refinement (Model A → B → C) |
| **Ensemble** | 🗳️ 5-10s | Consensus voting across models |

---

## 📁 Project Structure

```
Summer_2026/
├── multi_model_workflow.py         # Main orchestration engine
├── generate_report.py              # Report generation utility
├── workflow_config.json            # Configuration file
├── requirements.txt                # Python dependencies
├── .env.example                    # API key template
├── .gitignore                      # Git ignore rules
├── .github/workflows/
│   └── multi-model-workflow.yml    # GitHub Actions CI/CD
├── tests/
│   └── test_models.py              # Unit tests
├── data/                           # Dataset (to download from Kaggle)
├── results/                        # Output reports
├── logs/                           # Workflow logs
└── README.md                       # This file
```

---

## 🔐 GitHub Secrets Setup

To enable GitHub Actions automation:

1. Go to **Settings → Secrets and variables → Actions**
2. Add these secrets:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `GOOGLE_API_KEY`

---

## 📝 Usage Examples

### Example 1: Analyze a Product
```python
from multi_model_workflow import MultiModelWorkflow
import asyncio

async def analyze():
    workflow = MultiModelWorkflow()
    
    product = {
        "ProductName": "Premium Cotton T-Shirt",
        "Brand": "Nike",
        "Price": 1499,
        "Category": "Apparel"
    }
    
    results = await workflow.ensemble_voting(
        f"Analyze product: {product}"
    )
    
    print(results)

asyncio.run(analyze())
```

### Example 2: Parallel Model Processing
```python
results = await workflow.run_all_models_parallel(
    "What are the top e-commerce trends in fashion?"
)

print(f"GPT: {results['gpt']}")
print(f"Claude: {results['claude']}")
print(f"Gemini: {results['gemini']}")
```

### Example 3: Sequential Pipeline
```python
results = await workflow.run_models_sequential(
    "Analyze Myntra's pricing strategy"
)

print(f"Step 1 (GPT): {results['step_1_gpt']}")
print(f"Step 2 (Claude): {results['step_2_claude']}")
print(f"Step 3 (Gemini): {results['step_3_gemini']}")
```

---

## 🚀 GitHub Actions Workflow

The `.github/workflows/multi-model-workflow.yml` file:
- ✅ Runs daily (midnight UTC)
- ✅ Can be triggered manually
- ✅ Downloads dataset
- ✅ Processes with all models
- ✅ Generates reports
- ✅ Uploads artifacts

**Trigger manually:**
```
Go to Actions → Multi-Model AI Workflow → Run workflow
```

---

## 📊 Output Format

### JSON Report (`results/report.json`)
```json
{
  "generated_at": "2026-05-12T18:30:00",
  "results": {
    "gpt": "Analysis from GPT...",
    "claude": "Analysis from Claude...",
    "gemini": "Analysis from Gemini..."
  },
  "summary": {
    "total_models": 3,
    "models": ["GPT", "Claude", "Gemini"]
  }
}
```

### HTML Report (`results/report.html`)
- Visual dashboard
- Model comparison
- Execution metrics
- Interactive tables

---

## 🧪 Testing

```bash
pytest tests/
pytest -v tests/test_models.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit a Pull Request

---

## 📚 Additional Resources

- **GPT API Docs:** https://platform.openai.com/docs
- **Claude API Docs:** https://docs.anthropic.com
- **Gemini API Docs:** https://ai.google.dev
- **Myntra Dataset:** https://www.kaggle.com/datasets/ronakbokaria/myntra-products-dataset

---

## 📄 License

MIT License - Feel free to use this project for your own purposes.

---

## 🤖 Built With

- Python 3.10+
- OpenAI API (GPT-4)
- Anthropic API (Claude-3)
- Google Generative AI (Gemini)
- GitHub Actions
- Async/Await for performance

---

**Last Updated:** 2026-05-12  
**Status:** ✅ Active Development
