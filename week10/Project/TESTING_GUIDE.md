# Testing Guide - Logging, Monitoring & Rate Limiting

## Setup for Testing

### 1. Install Dependencies

```bash
cd c:\Users\Admin\Downloads\2526II_INT3505_1\week10\Project
pip install -r requirements.txt
```

### 2. Start Application

```bash
python project.py
```

Expected output:

```
Server running at http://localhost:5000
Metrics available at http://localhost:5000/metrics
Health check at http://localhost:5000/health
```

## Testing Logging

### Test 1: View Console Logs

Run your requests and observe logs in console:

```
2024-01-15 10:30:45,123 - root - INFO - Incoming request
2024-01-15 10:30:45,124 - root - INFO - Response sent
```

### Test 2: Login and Check Logs

```bash
# Send login request
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"khoe@gmail.com","password":"password1"}'

# Check logs
cat logs/app.log | grep "User logged in"
```

### Test 3: Failed Login and Error Logs

```bash
# Send invalid login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"khoe@gmail.com","password":"wrong"}'

# Check error logs
cat logs/app_error.log | grep "Login failed"
```

## Testing Prometheus Metrics

### Test 1: Access Metrics Endpoint

```bash
curl http://localhost:5000/metrics
```

Expected output:

```
# HELP http_requests_total Tổng số request HTTP
# TYPE http_requests_total counter
http_requests_total{endpoint="login",method="POST",status="200"} 1.0
http_requests_total{endpoint="login",method="POST",status="401"} 2.0
...
```

### Test 2: Verify Request Metrics

Make multiple requests and check metrics:

```bash
# Make 5 successful logins
for i in {1..5}; do
  curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"email":"khoe@gmail.com","password":"password1"}' \
    -s > /dev/null
done

# Check login_attempts_total metric
curl http://localhost:5000/metrics | grep login_attempts
```

### Test 3: Check Active Connections

```bash
# During request processing
curl http://localhost:5000/metrics | grep active_connections
```

## Testing Rate Limiting

### Test 1: Test Login Rate Limit (5 per minute)

```bash
# Make 5 successful requests (should succeed)
for i in {1..5}; do
  echo "Request $i:"
  curl -X POST http://localhost:5000/login \
    -H "Content-Type: application/json" \
    -d '{"email":"khoe@gmail.com","password":"password1"}' \
    -w "\nStatus: %{http_code}\n\n"
done

# 6th request should fail with 429
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"khoe@gmail.com","password":"password1"}'
```

Expected 429 response:

```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later."
}
```

### Test 2: Test Different Endpoints Rate Limits

```bash
# Test GET /users (30 per minute)
for i in {1..30}; do
  curl -X GET http://localhost:5000/users \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -s > /dev/null
  echo "Request $i"
done

# 31st request should fail
curl -X GET http://localhost:5000/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test 3: Rate Limit Metrics

```bash
# Make requests that exceed rate limit
# Then check metrics
curl http://localhost:5000/metrics | grep rate_limit_hits
```

## Testing Health Check

### Test 1: Access Health Endpoint

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy",
  "service": "User Management API",
  "version": "1.0.0"
}
```

## Testing with Postman

### Create Collection

**1. Login Request**

```
POST http://localhost:5000/login
Content-Type: application/json

{
  "email": "khoe@gmail.com",
  "password": "password1"
}
```

**2. Get Users Request**

```
GET http://localhost:5000/users
Authorization: Bearer {{access_token}}
```

**3. Health Check**

```
GET http://localhost:5000/health
```

**4. Metrics**

```
GET http://localhost:5000/metrics
```

### Test Rate Limiting in Postman

1. Create "Login" request
2. Set up Collection Runner
3. Run 10 times
4. Observe failures after 5th attempt

## Testing with Python Script

```python
import requests
import time
import json

BASE_URL = "http://localhost:5000"

def test_logging():
    print("=== Testing Logging ===")
    response = requests.post(
        f"{BASE_URL}/login",
        json={"email": "khoe@gmail.com", "password": "password1"}
    )
    print(f"Status: {response.status_code}")
    print("Check logs/app.log for details")

def test_metrics():
    print("\n=== Testing Metrics ===")
    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Metrics endpoint status: {response.status_code}")
    # Show first 500 chars
    print(response.text[:500])

def test_rate_limiting():
    print("\n=== Testing Rate Limiting ===")
    for i in range(7):
        response = requests.post(
            f"{BASE_URL}/login",
            json={"email": "khoe@gmail.com", "password": "password1"}
        )
        print(f"Request {i+1}: Status {response.status_code}")
        if response.status_code == 429:
            print("Rate limit hit! ✓")
            break

def test_health():
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    test_logging()
    test_metrics()
    test_rate_limiting()
    test_health()
```

Run with:

```bash
python test_features.py
```

## Monitoring Metrics in Real-Time

### Option 1: Using grep (Simple)

```bash
# Watch for login attempts
watch 'curl -s http://localhost:5000/metrics | grep login_attempts'
```

### Option 2: Using jq (Parse JSON)

```bash
# Format metrics nicely
curl http://localhost:5000/metrics | grep -E "^[a-z_]+ " | head -20
```

### Option 3: Using Prometheus (Production)

1. Install Prometheus
2. Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: "user-api"
    static_configs:
      - targets: ["localhost:5000"]
```

3. Run Prometheus:

```bash
prometheus --config.file=prometheus.yml
```

4. Access Prometheus UI: `http://localhost:9090`

## Checking Logs

### View All Logs

```bash
# Last 50 lines
tail -50 logs/app.log

# Follow in real-time
tail -f logs/app.log

# Search for specific term
grep "login" logs/app.log

# Count entries by level
grep '"level": "INFO"' logs/app.log | wc -l
```

### Parse JSON Logs

```bash
# Pretty print
cat logs/app.log | python -m json.tool

# Extract timestamps
grep "timestamp" logs/app.log | cut -d'"' -f4 | sort | uniq -c
```

## Troubleshooting Tests

### Issue: Port 5000 Already in Use

```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process
taskkill /PID <PID> /F
```

### Issue: Metrics Not Updating

- Ensure requests are being made
- Check that application is running
- Verify metrics endpoint returns data

### Issue: Rate Limit Not Working

- Check rate_limiter module is imported
- Verify flask-limiter is installed
- Check application logs for errors

### Issue: Logs Not Writing

- Check `logs/` directory exists
- Verify write permissions
- Check disk space

## Performance Testing

### Load Test Rate Limiting

```bash
# Use Apache Bench
ab -n 100 -c 10 http://localhost:5000/login

# Or use hey
go install github.com/rakyll/hey@latest
hey -n 100 -c 10 http://localhost:5000/login
```

### Monitor Metrics Under Load

```bash
# In one terminal, start load
ab -n 1000 -c 50 http://localhost:5000/users

# In another terminal, monitor metrics
watch 'curl -s http://localhost:5000/metrics | grep http_requests_total'
```

## Success Criteria

✅ **Logging Works** if:

- Console shows request/response logs
- `logs/app.log` contains JSON entries
- Errors appear in `logs/app_error.log`

✅ **Metrics Work** if:

- `/metrics` endpoint returns data
- Metrics increase after requests
- All metric types appear

✅ **Rate Limiting Works** if:

- 5 login requests succeed
- 6th request returns 429
- Rate limit metrics increment

✅ **Health Check Works** if:

- `/health` returns JSON status
- Status shows "healthy"

---

**Testing Date**: January 2024
**Version**: 1.0
**Status**: Ready for testing
