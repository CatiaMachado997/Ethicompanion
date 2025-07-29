# EthicCompanion: Local Model Testing Guide

## 🚀 Quick Start with Your Enhanced Backend

Your EthicCompanion project now has comprehensive custom model training capabilities! Here's how to test everything locally and on Google Cloud.

## 📁 Project Structure Update

```
ethiccompanion-mvp/
├── notebooks/                           # 🆕 New training notebooks
│   ├── gemma_finetuning_vertex_ai.ipynb    # Gemma fine-tuning on Vertex AI
│   └── ethical_classifiers_training.ipynb   # Custom classifier training
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── chat_models_enhanced.py      # Enhanced Pydantic models
│   │   ├── api/
│   │   │   └── chat_enhanced.py             # Enhanced API endpoints
│   │   └── services/
│   │       ├── llm_service_enhanced.py      # Multi-LLM orchestrator
│   │       ├── rag_service_enhanced.py      # Enhanced RAG pipeline
│   │       └── ethical_guardrails_enhanced.py # Content moderation
│   └── test_enhanced_api.py             # 🆕 Comprehensive testing
└── trained_models/                      # 🆕 Your custom models will be here
    ├── ethiccompanion_ethical_scope_classifier/
    ├── ethiccompanion_crisis_detection_classifier/
    └── ethiccompanion_bias_detection_classifier/
```

## 🧪 Testing Strategy

### 1. Local Testing (Start Here)

#### Test Enhanced Backend API
```bash
cd ethiccompanion-mvp/backend

# Install dependencies
pip install -r requirements.txt

# Run the enhanced API
python -m app.main

# In another terminal, test the API
python test_enhanced_api.py
```

#### Train Custom Classifiers
```bash
# Open Jupyter notebook
jupyter notebook notebooks/ethical_classifiers_training.ipynb

# Run all cells to train:
# - Ethical scope classifier
# - Crisis detection model  
# - Bias detection system
```

### 2. Google Cloud Testing

#### Setup Vertex AI Environment
```bash
# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Authenticate
gcloud auth login
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable compute.googleapis.com
```

#### Run Gemma Fine-tuning on Vertex AI
```bash
# Open the Vertex AI notebook
jupyter notebook notebooks/gemma_finetuning_vertex_ai.ipynb

# The notebook will:
# 1. Set up Vertex AI environment
# 2. Prepare ethical guidance dataset
# 3. Fine-tune Gemma models with LoRA
# 4. Deploy to Vertex AI endpoints
# 5. Test and compare model performance
```

## 🔧 Configuration Required

### Environment Variables
Create a `.env` file in your backend directory:

```bash
# OpenAI API (for GPT models)
OPENAI_API_KEY=your_openai_api_key

# Anthropic API (for Claude)
ANTHROPIC_API_KEY=your_anthropic_api_key

# Google Cloud (for Gemini and Vertex AI)
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_REGION=us-central1

# Hugging Face (for Gemma models)
HUGGINGFACE_API_TOKEN=your_hf_token
```

### API Keys You'll Need

1. **OpenAI API Key**: https://platform.openai.com/api-keys
2. **Anthropic API Key**: https://console.anthropic.com/
3. **Google Cloud Service Account**: 
   - Go to Google Cloud Console
   - Create a service account with Vertex AI permissions
   - Download the JSON key file
4. **Hugging Face Token**: https://huggingface.co/settings/tokens

## 🧪 Comprehensive Testing Workflow

### Phase 1: Local API Testing (5 minutes)
```bash
# Test basic enhanced API
curl -X POST "http://localhost:8000/ask_ethical" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I feel overwhelmed by climate change news",
    "user_context": {
      "stress_level": "high",
      "preferred_approach": "mindful"
    }
  }'
```

### Phase 2: Custom Classifier Training (15 minutes)
```python
# Run in ethical_classifiers_training.ipynb
# This will train 3 specialized models:
# 1. Ethical scope classifier
# 2. Crisis detection model
# 3. Bias detection system

# After training, integrate with your backend:
from app.services.ethical_guardrails_enhanced import EnhancedEthicalClassifiers
classifiers = EnhancedEthicalClassifiers()
```

### Phase 3: Vertex AI Testing (30 minutes)
```python
# Run in gemma_finetuning_vertex_ai.ipynb
# This will:
# 1. Test base Gemma models on Vertex AI
# 2. Fine-tune models for ethical guidance
# 3. Compare performance metrics
# 4. Deploy best models to endpoints
```

## 🎯 Expected Results

### Enhanced API Features
- ✅ Multi-LLM provider support (OpenAI, Anthropic, Google)
- ✅ Comprehensive input validation with Pydantic
- ✅ Advanced error handling and retry logic
- ✅ Content moderation and ethical guardrails
- ✅ Conversation history and context management
- ✅ Background task processing
- ✅ Health monitoring and metrics

### Custom Model Capabilities
- ✅ **Ethical Scope Classification**: Determines if queries fit ethical guidance scope
- ✅ **Crisis Detection**: Identifies users needing immediate intervention
- ✅ **Bias Detection**: Flags biased or one-sided content
- ✅ **Content Moderation**: Comprehensive analysis pipeline

### Vertex AI Integration
- ✅ **Gemma Model Testing**: Compare different model sizes and configurations
- ✅ **Custom Fine-tuning**: Train specialized models for ethical guidance
- ✅ **Performance Benchmarking**: Evaluate models against ethical guidance tasks
- ✅ **Production Deployment**: Deploy models to scalable endpoints

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors in Enhanced Backend**
   ```bash
   # Make sure you're in the right directory
   cd ethiccompanion-mvp/backend
   python -c "from app.models.chat_models_enhanced import EthicalRequest; print('✅ Imports working')"
   ```

2. **API Key Issues**
   ```bash
   # Check environment variables
   echo $OPENAI_API_KEY
   echo $GOOGLE_APPLICATION_CREDENTIALS
   ```

3. **Vertex AI Permission Errors**
   ```bash
   # Re-authenticate
   gcloud auth application-default login
   gcloud config set project YOUR_PROJECT_ID
   ```

4. **Custom Model Loading Issues**
   ```python
   # Check if models are trained and saved
   import os
   print(os.listdir('./ethiccompanion_ethical_scope_classifier'))
   ```

## 🎉 Success Metrics

You'll know everything is working when:

- ✅ Enhanced API responds with structured JSON and proper error handling
- ✅ Custom classifiers achieve >90% accuracy on ethical classification tasks
- ✅ Vertex AI successfully loads and tests Gemma models
- ✅ Fine-tuned models show improved performance on ethical guidance tasks
- ✅ All models integrate seamlessly with your Flutter frontend

## 🚀 Next Steps

1. **Expand Training Data**: Add more diverse examples to improve classifier accuracy
2. **A/B Testing**: Compare different model configurations in production
3. **Monitoring Setup**: Implement logging and performance tracking
4. **User Feedback**: Collect feedback to continuously improve model responses
5. **Production Deployment**: Deploy to Google Cloud Run or Kubernetes

Your EthicCompanion now has enterprise-grade AI capabilities with custom ethical intelligence! 🌟
