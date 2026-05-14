# Quick Start Guide

## ⚡ Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Application

```bash
python project.py
```

### Step 3: Test Everything Works

**In another terminal:**

```bash
# 1. Check health
curl http://localhost:5000/health

# 2. View metrics
curl http://localhost:5000/metrics

# 3. Login (should succeed)
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"khoe@gmail.com","password":"password1"}'

# 4. Trigger rate limit (try login 6 times quickly)
for i in {1..6}; do
  curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"email":"khoe@gmail.com","password":"password1"}' \
    -w "\n"
done
```

### Step 4: Check Logs

```bash
# View logs
tail logs/app.log

# View error logs
tail logs/app_error.log
```

## 📋 What Was Added

### 1. **Logging** 📝

- Automatic request/response logging
- JSON formatted logs
- Auto-rotating log files
- Separate error logs

### 2. **Monitoring** 📊

- Prometheus metrics
- `/metrics` endpoint for scraping
- 8+ metrics tracked
- Ready for Grafana dashboards

### 3. **Rate Limiting** 🛡️

- 5 login attempts per minute
- Protection for all endpoints
- IP-based limiting
- Returns 429 when limit exceeded

## 🎯 Key URLs

```
API Base:       http://localhost:5000
Health Check:   http://localhost:5000/health
Metrics:        http://localhost:5000/metrics
Login:          POST http://localhost:5000/login
```

## 📁 New Files

```
config/
├── logging_config.py          # Logging setup
monitoring/
├── metrics.py                 # Prometheus metrics
├── rate_limiter.py           # Rate limiting
LOGGING_MONITORING_GUIDE.md    # Full documentation
TESTING_GUIDE.md              # Testing instructions
IMPLEMENTATION_SUMMARY.md     # What was done
QUICK_START.md               # This file
```

## 🔍 Testing Quick Reference

### Test Logging

```bash
# Make a request and check logs
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"khoe@gmail.com","password":"password1"}'

# View what was logged
tail -5 logs/app.log
```

### Test Metrics

```bash
# Make several requests first
for i in {1..5}; do
  curl http://localhost:5000/health > /dev/null 2>&1
done

# Check metrics
curl http://localhost:5000/metrics | grep http_requests_total
```

### Test Rate Limiting

```bash
# Make 6 quick login attempts
for i in {1..6}; do
  echo "Attempt $i:"
  curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"email":"khoe@gmail.com","password":"password1"}' \
    -s | grep -o '"error\|"message\|"access_token"'
done

# 6th attempt should show "error": "Rate limit exceeded"
```

## 🛠️ Common Tasks

### Change Rate Limit

Edit `monitoring/rate_limiter.py`:

```python
RATE_LIMITS = {
    'login': '10 per minute',  # Changed from 5
}
```

Then restart application.

### Add Custom Logging

In any controller file:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("My message")
logger.error("Error message")
```

### View Metrics

```bash
# All metrics
curl http://localhost:5000/metrics

# Only request metrics
curl http://localhost:5000/metrics | grep http_requests

# Only login metrics
curl http://localhost:5000/metrics | grep login
```

## 📈 Production Setup

### Set up Prometheus Monitoring

1. Install Prometheus
2. Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "user-api"
    static_configs:
      - targets: ["localhost:5000"]
```

3. Run: `prometheus --config.file=prometheus.yml`
4. Access: `http://localhost:9090`

### Log Analysis

```bash
# Count requests by type
grep '"method"' logs/app.log | sort | uniq -c

# Find errors
grep '"level": "ERROR"' logs/app.log

# Monitor in real-time
tail -f logs/app.log
```

## ❓ FAQ

**Q: How do I disable rate limiting?**
A: Remove rate limiting decorators or set very high limits in `monitoring/rate_limiter.py`

**Q: Where are my logs?**
A: Check `logs/app.log` and `logs/app_error.log`

**Q: How do I see metrics?**
A: Visit `http://localhost:5000/metrics`

**Q: What's the health endpoint for?**
A: Kubernetes/Docker health checks - visit `http://localhost:5000/health`

**Q: Can I change log format?**
A: Yes, edit `config/logging_config.py`

**Q: How do I integrate Grafana?**
A: Set up Prometheus first, then add Prometheus as datasource in Grafana

## 📚 Documentation Files

- **LOGGING_MONITORING_GUIDE.md** - Complete reference guide
- **TESTING_GUIDE.md** - Detailed testing instructions
- **IMPLEMENTATION_SUMMARY.md** - What was implemented
- **requirements.txt** - All dependencies

## ✅ Verification Checklist

- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Application runs: `python project.py`
- [ ] Health check works: `curl http://localhost:5000/health`
- [ ] Metrics available: `curl http://localhost:5000/metrics`
- [ ] Logs created: Check `logs/` directory
- [ ] Rate limiting works: Login 6 times, 6th fails with 429

## 🚀 Next Steps

1. Read `LOGGING_MONITORING_GUIDE.md` for detailed documentation
2. Follow `TESTING_GUIDE.md` to test all features
3. Set up Prometheus for production monitoring
4. Customize rate limits for your needs
5. Add custom metrics for your business logic

---

**Ready to use!** 🎉
