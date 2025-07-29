# 🚀 EthicCompanion - Real API Setup Guide

Complete guide for setting up and testing all your APIs for hackathon deployment.

## 🔧 Environment Setup

### 1. Create `.env` file in your project root:

```bash
# Create .env file
touch /Users/catiamachado/Documents/Ethicompanion/Ethicompanion/.env
```

### 2. Add the following to your `.env` file:

```env
# Google Cloud Platform
GOOGLE_CLOUD_PROJECT=your-project-id
GEMINI_API_KEY=your-gemini-api-key

# Kaggle for Gemma 3n access
KAGGLE_USERNAME=your-kaggle-username
KAGGLE_KEY=your-kaggle-key

# Anthropic Claude
ANTHROPIC_API_KEY=your-anthropic-api-key

# Firebase (if using separate service account)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Optional: Specific model preferences
GEMMA_MODEL_SIZE=2b
DEFAULT_LLM_PROVIDER=gemini
```

## 🎯 Getting Your API Keys

### 1. Google Cloud & Gemini API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable these APIs:
   - Vertex AI API
   - Generative AI API
   - Firestore API
   - Cloud Storage API
4. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
5. Create Gemini API key
6. Copy your project ID and API key

### 2. Kaggle for Gemma 3n Access
1. Go to [Kaggle Account Settings](https://www.kaggle.com/settings/account)
2. Scroll to "API" section
3. Click "Create New API Token"
4. Download `kaggle.json` 
5. Extract username and key from the file

### 3. Anthropic Claude API
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create account and get API key
3. Copy the API key starting with `sk-ant-`

### 4. Google Cloud Service Account (for Firestore)
1. In Google Cloud Console, go to IAM & Admin → Service Accounts
2. Create new service account
3. Add roles: Firestore User, Vertex AI User
4. Create JSON key and download
5. Save path to GOOGLE_APPLICATION_CREDENTIALS

## 🚀 Quick Setup Commands

```bash
# Navigate to your project
cd /Users/catiamachado/Documents/Ethicompanion/Ethicompanion

# Install all required packages
pip install -r ethiccompanion-mvp/backend/requirements.txt

# Set up Kaggle credentials (alternative to .env)
mkdir -p ~/.kaggle
# Copy your kaggle.json to ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

# Test your setup
python -c "import os; print('✅' if os.getenv('GEMINI_API_KEY') else '❌', 'GEMINI_API_KEY')"
```

## 📱 Testing Your Setup

### Option 1: Run the comprehensive notebook
1. Open `notebooks/ethical_classifiers_training.ipynb`
2. Run all cells in order
3. Check the final test report

### Option 2: Quick CLI tests

```python
# Test individual services
import asyncio
import os
from datetime import datetime

# Test Gemini API
async def test_gemini():
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Hello, test message")
    print("✅ Gemini working:", response.text[:100])

# Test Kaggle/Gemma access
async def test_kaggle():
    import kagglehub
    print("✅ Kaggle authenticated:", kagglehub.login())

# Run tests
asyncio.run(test_gemini())
asyncio.run(test_kaggle())
```

## 🎯 Deployment Checklist

### ✅ Pre-deployment
- [ ] All API keys configured in `.env`
- [ ] Google Cloud project set up with required APIs
- [ ] Kaggle authentication working
- [ ] Service account JSON downloaded
- [ ] All packages installed from requirements.txt

### ✅ Testing Complete
- [ ] Gemma 3n model loads successfully
- [ ] Gemini API responds correctly
- [ ] Vertex AI embeddings working
- [ ] Firestore connection established
- [ ] Claude API accessible (optional)
- [ ] Enhanced backend services running

### ✅ Production Ready
- [ ] Error handling tested
- [ ] Rate limits understood
- [ ] Monitoring set up
- [ ] Security reviewed
- [ ] Flutter frontend connected

## 🔥 Hackathon Specific Tips

### Gemma 3n Competitive Advantages
1. **Efficiency**: 2B model runs fast on standard hardware
2. **Multimodal**: Supports text, images, and audio
3. **Ethical Focus**: Perfect for EthicCompanion use case
4. **Open Source**: Can fine-tune for specific ethics scenarios

### Demo-Ready Features
1. **Real-time ethical guidance**: Fast response times
2. **Multi-provider fallback**: Never fails during demo
3. **Content moderation**: Blocks harmful requests
4. **Knowledge base**: Curated ethical guidance
5. **Conversation memory**: Maintains context

### Performance Benchmarks
- Gemma 3n E2B: ~1-2s response time
- Gemini Pro: ~1-3s response time
- Claude Sonnet: ~2-4s response time
- RAG retrieval: ~0.5-1s
- Total pipeline: ~2-5s end-to-end

## 🆘 Troubleshooting

### Common Issues

**"Quota exceeded" errors:**
- Switch to different API provider
- Implement rate limiting
- Use model fallback logic

**Kaggle authentication fails:**
- Check `~/.kaggle/kaggle.json` permissions
- Verify username/key in .env
- Try manual login: `kaggle datasets list`

**Google Cloud errors:**
- Verify project ID is correct
- Check API enablement
- Confirm service account permissions

**Model loading slow:**
- Use smaller model variant (2B instead of 4B)
- Implement model caching
- Pre-load models on startup

### Getting Help
1. Check the comprehensive testing notebook
2. Review error logs in terminal
3. Test individual components separately
4. Join Google Cloud Discord for Gemma support

## 🏆 Success Metrics

Your EthicCompanion is ready when:
- ✅ All tests pass in the notebook
- ✅ Response times under 5 seconds
- ✅ Error rate under 5%
- ✅ All fallback providers work
- ✅ Ethical guardrails active
- ✅ Flutter frontend connected

Good luck with your hackathon! 🚀
gcloud projects add-iam-policy-binding ethiccompanion-hackathon \
    --member="serviceAccount:ethiccompanion-sa@ethiccompanion-hackathon.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding ethiccompanion-hackathon \
    --member="serviceAccount:ethiccompanion-sa@ethiccompanion-hackathon.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
gcloud iam service-accounts keys create ./service-account-key.json \
    --iam-account=ethiccompanion-sa@ethiccompanion-hackathon.iam.gserviceaccount.com
```

## 🔑 Step 2: API Keys Setup

### 2.1 Get Required API Keys

#### Google AI Studio (for Gemini)
1. Go to https://makersuite.google.com/app/apikey
2. Create API key for Gemini
3. Copy the key

#### Anthropic (for Claude)
1. Go to https://console.anthropic.com/
2. Create account and get API key
3. Copy the key

#### Hugging Face (for Gemma 3n)
1. Go to https://huggingface.co/settings/tokens
2. Create access token with read permissions
3. Accept Gemma 3n license at https://huggingface.co/google/gemma-3n-e2b

#### Google Perspective API (for content moderation)
1. Go to Google Cloud Console
2. Enable Perspective API
3. Create API key

### 2.2 Create Environment File
```bash
# Create .env file in backend directory
cd ethiccompanion-mvp/backend
```

Create `.env` file with real credentials:
```env
# Google Cloud
GOOGLE_CLOUD_PROJECT=ethiccompanion-hackathon
GOOGLE_APPLICATION_CREDENTIALS=./service-account-key.json

# AI Model APIs
GEMINI_API_KEY=your_actual_gemini_api_key_here
ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
HUGGINGFACE_TOKEN=your_actual_hf_token_here

# Content Moderation
PERSPECTIVE_API_KEY=your_actual_perspective_api_key_here

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 🧪 Step 3: Create Real API Testing Script
