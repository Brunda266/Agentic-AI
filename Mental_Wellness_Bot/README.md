# Mental Wellness Bot

**Streamlit Dashboard + Groq AI**

## Quick Start

### 1. Install
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
export GROQ_API_KEY="your-key-here"
```

### 3. Run
```bash
streamlit run app.py
```

## Files

- `app.py` - Streamlit dashboard
- `analyzer.py` - Emotion/urgency/crisis detection
- `ai_wrapper.py` - Groq API integration
- `guardrails.py` - Safety validation
- `config.py` - Keywords & prompts

## Features

✅ Chat interface  
✅ Emotion detection  
✅ Crisis escalation  
✅ Groq API powered  
✅ Conversation history  
✅ Safety guardrails  

## How It Works

```
User Message
    ↓
Analyze (emotion/urgency/crisis)
    ↓
Groq API Response
    ↓
Safety Check
    ↓
Display + Escalate if needed
```

## Crisis Resources

- 988 - National Suicide Prevention Lifeline
- Crisis Text Line: Text HELLO to 741741
- 911 - Emergency Services
