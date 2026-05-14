# Architecture - Multi-Model AI Workflow System

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────────┐
│              Myntra Dataset (Kaggle)                        │
│         13,000+ e-commerce products                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           Data Pipeline & Preprocessing                     │
│  - Load CSV → Clean → Normalize → Sample                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    ┌────────┐   ┌────────┐   ┌────────┐
    │  GPT   │   │ Claude │   │ Gemini │
    │ Model  │   │ Model  │   │ Model  │
    └────────┘   └────────┘   └────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
   ┌──────────────┐        ┌──────────────────┐
   │ Aggregation  │◄──────►│ Comparison       │
   │ Module       │        │ Engine           │
   └──────────────┘        └──────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│          Report Generation                                  │
│    JSON (Machine) + HTML (Human)                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   Results/     Logs/        GitHub
   report.json  workflow.log  Artifacts
```

---

## 🔄 Execution Modes

### 1. Parallel Mode (Default)
```
Start: 0ms
├─ GPT:    0ms → 8000ms
├─ Claude: 0ms → 8000ms
└─ Gemini: 0ms → 8000ms
End: 8000ms (all concurrent)

Speed: ⚡ 5-10 seconds
Use: Fast independent analysis
```

**Pseudocode:**
```python
async def parallel():
    tasks = [
        process_with_gpt(prompt),
        process_with_claude(prompt),
        process_with_gemini(prompt)
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### 2. Sequential Mode
```
Start: 0ms
├─ GPT:    0ms → 5000ms (Analysis)
├─ Claude: 5000ms → 10000ms (Refinement)
└─ Gemini: 10000ms → 15000ms (Validation)
End: 15000ms (sequential)

Speed: ⏱️ 15-20 seconds
Use: Cascading refinement
```

**Pseudocode:**
```python
async def sequential():
    step1 = await process_with_gpt(prompt)
    step2 = await process_with_claude(refine_prompt(step1))
    step3 = await process_with_gemini(validate_prompt(step2))
    return [step1, step2, step3]
```

### 3. Ensemble Mode
```
Start: 0ms
├─ GPT:    0ms → 8000ms
├─ Claude: 0ms → 8000ms
└─ Gemini: 0ms → 8000ms
├─ Voting: 8000ms → 9000ms
└─ Consensus: Aggregate
End: 9000ms

Speed: 🗳️ 5-10 seconds
Use: Consensus voting
```

**Pseudocode:**
```python
async def ensemble():
    results = await parallel()
    consensus = aggregate_responses(results)
    return {
        "individual": results,
        "consensus": consensus
    }
```

---

## 🧩 Component Architecture

### 1. Data Layer
```python
class DataPipeline:
    ├── load_myntra_dataset()      # CSV ingestion
    ├── preprocess()               # Cleaning
    ├── normalize()                # Standardization
    └── sample()                   # Subset selection
```

**Responsibilities:**
- Load Myntra CSV from Kaggle
- Handle missing values
- Normalize text/numeric fields
- Create batches for processing

### 2. Model Layer
```python
class ModelOrchestrator:
    ├── GPTModel
    │   ├── process_with_gpt()
    │   └── gpt_client (OpenAI API)
    │
    ├── ClaudeModel
    │   ├── process_with_claude()
    │   └── claude_client (Anthropic API)
    │
    └── GeminiModel
        ├── process_with_gemini()
        └── genai_model (Google API)
```

**Responsibilities:**
- Initialize API clients
- Handle authentication
- Format prompts per model
- Execute requests
- Handle timeouts/retries

### 3. Execution Layer
```python
class ExecutionEngine:
    ├── run_parallel()       # All models async
    ├── run_sequential()     # Cascading pipeline
    └── run_ensemble()       # Vote aggregation
```

**Responsibilities:**
- Route to execution mode
- Manage async tasks
- Handle concurrency
- Collect results
- Manage timeouts

### 4. Aggregation Layer
```python
class ResultAggregator:
    ├── aggregate_responses()
    ├── compare_models()
    ├── extract_consensus()
    └── rank_responses()
```

**Responsibilities:**
- Merge model outputs
- Find common themes
- Weight responses
- Generate consensus
- Calculate confidence

### 5. Reporting Layer
```python
class ReportGenerator:
    ├── generate_json_report()   # Machine readable
    ├── generate_html_report()   # Human readable
    ├── create_comparison()      # Side-by-side
    └── metrics()                # Performance stats
```

**Responsibilities:**
- Format results
- Create visualizations
- Calculate metrics
- Store artifacts
- Upload to GitHub

---

## 📊 Data Flow Diagram

```
Input Prompt
     │
     ▼
┌─────────────────────┐
│  Data Preprocessing │
│  - Extract product  │
│  - Format prompt    │
│  - Add context      │
└────────┬────────────┘
         │
    ┌────┴────┐
    │ Execution Mode?
    └────┬────┘
         │
    ┌────┴─────────────────────────────┐
    │                                  │
    ▼ (Parallel)                       ▼ (Sequential/Ensemble)
┌──────────────────────────────────────┐
│ Model Layer - Parallel Execution     │
├──────────────────────────────────────┤
│ • API Call 1 (GPT)                  │
│ • API Call 2 (Claude)               │
│ • API Call 3 (Gemini)               │
│ • All concurrent (async/await)      │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Response Collection                  │
├──────────────────────────────────────┤
│ • Collect from all models            │
│ • Handle timeouts/errors             │
│ • Normalize format                   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Aggregation & Analysis               │
├──────────────────────────────────────┤
│ • Compare outputs                    │
│ • Extract common themes              │
│ • Generate consensus                 │
│ • Calculate confidence               │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Report Generation                    │
├──────────────────────────────────────┤
│ • JSON Report (machine readable)     │
│ • HTML Report (human readable)       │
│ • Metrics & Statistics               │
└────────┬─────────────────────────────┘
         │
         ▼
    Output Reports
    (results/report.*)
```

---

## 🔐 Security Architecture

### API Key Management
```
.env (Local) ──────► Not committed (in .gitignore)
     │
     └──► GitHub Secrets (In repo settings)
          ├─ OPENAI_API_KEY
          ├─ ANTHROPIC_API_KEY
          └─ GOOGLE_API_KEY
```

### Execution Contexts
```
Local Execution:
├─ Reads from .env file
├─ Secrets in environment
└─ No GitHub access needed

GitHub Actions:
├─ Reads from Secrets
├─ Encrypted by GitHub
├─ Never logged or exposed
└─ Only accessible in workflow
```

---

## ⚙️ Configuration Management

### hierarchy (Highest to Lowest Priority)
```
1. Environment Variables (OPENAI_API_KEY=xxx python main.py)
2. .env File (python-dotenv)
3. workflow_config.json (Configuration defaults)
4. Code Defaults (Fallback values)
```

### workflow_config.json Structure
```json
{
  "execution": {
    "mode": "parallel",
    "timeout": 30,
    "retries": 3
  },
  "models": {
    "gpt": {
      "enabled": true,
      "model": "gpt-4",
      "max_tokens": 500
    },
    "claude": {
      "enabled": true,
      "model": "claude-3-sonnet",
      "max_tokens": 500
    },
    "gemini": {
      "enabled": true,
      "model": "gemini-pro",
      "max_tokens": 500
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/workflow.log"
  }
}
```

---

## 🚀 Deployment Architecture

### Local Development
```
Developer Machine
├─ Python venv
├─ Local .env
├─ Direct API calls
└─ Local results storage
```

### GitHub Actions (CI/CD)
```
GitHub Repository
├─ Workflow file (.github/workflows/*)
├─ Secrets storage
├─ Scheduled triggers (cron)
├─ Artifact storage
└─ Manual run capability
```

### Scalable Cloud Deployment
```
AWS / GCP / Azure
├─ Containerized (Docker)
├─ Managed secrets (KMS/Vault)
├─ Scheduled jobs (Lambda/Cloud Functions)
├─ S3/GCS storage (results)
└─ CloudWatch/StackDriver (monitoring)
```

---

## 📈 Performance Characteristics

### Model Processing Time
| Model | Cold Start | Average | Max |
|-------|-----------|---------|-----|
| GPT-4 | 2-3s | 3-5s | 10s |
| Claude | 2-3s | 3-5s | 10s |
| Gemini | 2-3s | 3-5s | 10s |

### Execution Mode Performance
| Mode | Serial Time | Actual Time | Speedup |
|------|------------|------------|---------|
| Sequential | 15s | 15s | 1x |
| Parallel | 15s | 5-8s | 2-3x |
| Ensemble | 15s + vote | 6-9s | 2-3x |

### Scalability
```
Single Prompt:
  - Local execution: ~8 seconds
  - GitHub Actions: ~30 seconds (including setup)
  
Multiple Prompts (1000):
  - Batch processing: ~2-3 hours
  - Cost: $3-10 (depending on model usage)
  
Myntra Full Dataset (13,000):
  - Full analysis: ~24-48 hours
  - Cost: $100-500 (depending on depth)
```

---

## 🔄 Error Handling Strategy

### Fault Tolerance
```
┌─ API Call
│  ├─ Success ──► Return Result
│  ├─ Timeout ──► Retry (max 3x) ──► Fallback/Log
│  ├─ Rate Limit ──► Wait & Retry ──► Fallback/Log
│  └─ Error ──► Log & Continue (other models)
│
└─ Graceful Degradation:
   - Single model failure ≠ workflow failure
   - Continue with other models
   - Report which models succeeded/failed
```

### Logging Strategy
```
logs/
├── workflow.log        # Main workflow logs
├── gpt.log            # Model-specific logs
├── claude.log
├── gemini.log
└── errors.log         # Error-specific logs

Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

---

## 📊 Monitoring & Observability

### Key Metrics
```
1. Model Response Time
   └─ Track latency per model per request

2. Success Rate
   └─ Percentage of successful API calls

3. Cost Tracking
   └─ API calls × model pricing

4. Error Frequency
   └─ Rate limits, timeouts, failures

5. Dataset Progress
   └─ Rows processed, completion %
```

---

## 🔗 Integration Points

### External Systems
```
Workflow ◄─► OpenAI API
        ◄─► Anthropic API
        ◄─► Google Generative AI
        ◄─► Kaggle Datasets
        ◄─► GitHub Actions
        ◄─► GitHub Artifacts
```

---

## 📚 Design Patterns Used

1. **Async/Await Pattern** - Concurrent execution
2. **Factory Pattern** - Model instantiation
3. **Observer Pattern** - Event logging
4. **Strategy Pattern** - Execution modes
5. **Adapter Pattern** - API standardization
6. **Decorator Pattern** - Error handling/retries
7. **Repository Pattern** - Result storage

---

**Architecture Version:** 1.0  
**Last Updated:** 2026-05-14  
**Status:** ✅ Production Ready
