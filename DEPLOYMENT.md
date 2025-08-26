# 🚀 Deployment Guide

This document provides comprehensive deployment instructions for the Agentic Research Assistant.

## 🌐 Streamlit Cloud Deployment

### Prerequisites
- GitHub repository with your code
- Streamlit Cloud account (free)
- Required API keys

### Steps
1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file: `app.py`

3. **Configure Environment Variables**
   - Add secrets in Streamlit Cloud dashboard:
   ```toml
   # .streamlit/secrets.toml
   GOOGLE_API_KEY = "your_key_here"
   BRAVE_API_KEY = "your_key_here"
   OPENAI_API_KEY = "your_key_here"  # Optional
   PINECONE_API_KEY = "your_key_here"  # Optional
   PINECONE_INDEX_NAME = "your_index_name"  # Optional
   GEMINI_MODEL = "gemini-2.5-flash"
   ```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Commands
```bash
# Build image
docker build -t agentic-research-assistant .

# Run container
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your_key \
  -e BRAVE_API_KEY=your_key \
  agentic-research-assistant
```

## ☁️ Cloud Platform Deployment

### AWS ECS
1. **Build and push to ECR**
2. **Create ECS task definition**
3. **Configure environment variables**
4. **Set up load balancer**

### Google Cloud Run
```bash
# Deploy to Cloud Run
gcloud run deploy agentic-research-assistant \
  --image gcr.io/PROJECT-ID/agentic-research-assistant \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku
```bash
# Create Heroku app
heroku create agentic-research-assistant

# Set environment variables
heroku config:set GOOGLE_API_KEY=your_key
heroku config:set BRAVE_API_KEY=your_key

# Deploy
git push heroku main
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Production settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Performance settings
MAX_SEARCH_RESULTS=10
CONFIDENCE_THRESHOLD=0.85
REQUEST_TIMEOUT=30
```

### Monitoring Setup
- **Health Checks**: `/health` endpoint
- **Metrics**: Application performance monitoring
- **Logging**: Structured logging with levels
- **Alerts**: Error rate and response time alerts

### Security Considerations
- **API Key Rotation**: Regular key rotation schedule
- **Rate Limiting**: Implement request rate limiting
- **HTTPS**: Force HTTPS in production
- **Input Validation**: Sanitize all user inputs

## 📊 Scaling Configuration

### Horizontal Scaling
- **Load Balancer**: Distribute traffic across instances
- **Auto Scaling**: Scale based on CPU/memory usage
- **Session Management**: Stateless application design

### Performance Optimization
- **Caching**: Redis for session and result caching
- **CDN**: Static asset delivery optimization
- **Database**: Connection pooling and optimization

## 🔍 Monitoring & Observability

### Application Metrics
- Response time percentiles (p50, p95, p99)
- Error rates by endpoint
- Tool execution success rates
- User engagement metrics

### Infrastructure Metrics
- CPU and memory utilization
- Network I/O and latency
- Disk usage and I/O
- Database performance

### Log Aggregation
```python
# Structured logging example
import logging
import json

logger = logging.getLogger(__name__)

def log_tool_execution(tool_name: str, query: str, success: bool, duration: float):
    logger.info(json.dumps({
        "event": "tool_execution",
        "tool": tool_name,
        "query_hash": hash(query),
        "success": success,
        "duration_ms": duration * 1000,
        "timestamp": datetime.utcnow().isoformat()
    }))
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Issues**
   - Verify all required keys are set
   - Check API key permissions and quotas
   - Validate key format and expiration

2. **Memory Issues**
   - Monitor memory usage patterns
   - Implement proper garbage collection
   - Consider increasing instance memory

3. **Performance Issues**
   - Check external API response times
   - Monitor database query performance
   - Optimize expensive operations

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
export LOG_LEVEL=DEBUG

# Run with profiling
python -m cProfile -o profile.stats app.py
```

### Health Checks
```python
# Add to app.py for health check endpoint
@st.experimental_fragment
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "dependencies": {
            "openai": check_openai_health(),
            "pinecone": check_pinecone_health(),
            "brave": check_brave_health()
        }
    }
```

## 📈 Performance Benchmarks

### Target Metrics
- **Response Time**: <3 seconds for 95% of queries
- **Uptime**: >99.9% availability
- **Error Rate**: <0.1% for valid requests
- **Throughput**: 100+ concurrent users

### Load Testing
```bash
# Using Apache Bench
ab -n 1000 -c 10 http://your-app-url/

# Using Artillery
artillery quick --count 10 --num 100 http://your-app-url/
```

---

This deployment guide ensures your Agentic Research Assistant runs reliably in production with proper monitoring and scaling capabilities.
