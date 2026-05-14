# Logging, Monitoring & Rate Limiting Documentation

## Tổng Quan

Dự án đã được cấu hình với:

1. **Logging** - Ghi lại tất cả các hoạt động của ứng dụng
2. **Monitoring (Prometheus)** - Thu thập metrics và giám sát hiệu suất
3. **Rate Limiting** - Giới hạn số lượng request từ các client

## 1. Logging Setup

### Vị trí cấu hình

- File: `config/logging_config.py`

### Tính năng

- **Console Logging**: In log ra terminal với định dạng dễ đọc
- **File Logging**: Lưu log vào file JSON (rotated mỗi 10MB)
- **Error Logging**: Riêng file cho error logs
- **Request/Response Logging**: Tự động log tất cả HTTP requests

### Log Files

- `logs/app.log` - Tất cả application logs (JSON format)
- `logs/app_error.log` - Chỉ error logs (JSON format)

### Cách sử dụng

```python
import logging

logger = logging.getLogger(__name__)

# Log levels
logger.debug("Debug message")
logger.info("Information message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Log Format

```json
{
  "timestamp": "2024-01-15 10:30:45",
  "level": "INFO",
  "name": "app.controllers",
  "message": "User logged in successfully"
}
```

## 2. Prometheus Monitoring

### Vị trí cấu hình

- File: `monitoring/metrics.py`

### Metrics được theo dõi

#### HTTP Requests

- `http_requests_total` - Tổng số request (bao gồm method, endpoint, status)
- `http_request_duration_seconds` - Thời gian xử lý request
- `active_connections` - Số kết nối đang hoạt động

#### Authentication

- `login_attempts_total` - Tổng login attempts (success/failed)
- `token_refresh_total` - Tổng token refresh (success/failed)

#### Business Operations

- `user_operations_total` - Tổng user operations (create/read/update/delete)

#### Rate Limiting

- `rate_limit_hits_total` - Tổng số lần bị rate limit

### Truy cập Metrics

- URL: `http://localhost:5000/metrics`
- Format: Prometheus text format
- Có thể scrape bằng Prometheus server

### Ví dụ Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "user-api"
    static_configs:
      - targets: ["localhost:5000"]
```

## 3. Rate Limiting

### Vị trí cấu hình

- File: `monitoring/rate_limiter.py`

### Rate Limits áp dụng

| Endpoint      | Method | Limit         | Mục đích                 |
| ------------- | ------ | ------------- | ------------------------ |
| `/login`      | POST   | 5 per minute  | Ngăn brute force attacks |
| `/logout`     | POST   | 30 per minute | Normal usage             |
| `/refresh`    | POST   | 10 per minute | Token refresh            |
| `/users`      | GET    | 30 per minute | Read operations          |
| `/users`      | POST   | 5 per minute  | Create user              |
| `/users/<id>` | PUT    | 10 per minute | Update user              |
| `/users/<id>` | DELETE | 5 per minute  | Delete user              |

### Cách thức hoạt động

- Rate limit dựa trên **IP address** của client
- Mỗi client có giới hạn riêng
- Khi vượt quá giới hạn → Nhận response 429 (Too Many Requests)

### Error Response (429)

```json
{
  "error": "Rate limit exceeded",
  "message": "Too many requests. Please try again later."
}
```

### Tùy chỉnh Rate Limits

Chỉnh sửa `RATE_LIMITS` dict trong `monitoring/rate_limiter.py`:

```python
RATE_LIMITS = {
    'login': '5 per minute',      # 5 requests per minute
    'logout': '30 per minute',    # 30 requests per minute
    'refresh': '10 per minute',   # 10 requests per minute
    # ...
}
```

## 4. Health Check Endpoint

- URL: `http://localhost:5000/health`
- Trả về trạng thái của service

Ví dụ response:

```json
{
  "status": "healthy",
  "service": "User Management API",
  "version": "1.0.0"
}
```

## 5. Integrated Endpoints

### Endpoint mới/cập nhật

- `GET /metrics` - Prometheus metrics
- `GET /health` - Health check

### Tất cả endpoints có:

- Automatic request/response logging
- Automatic metrics collection
- Rate limiting (nếu áp dụng)
- Exception handling với logging

## 6. Dependencies

```
Flask==2.3.0
PyJWT==2.8.0
prometheus-client==0.17.1
flask-limiter==3.5.0
python-json-logger==2.0.7
```

Install bằng:

```bash
pip install -r requirements.txt
```

## 7. Chạy Application

```bash
python project.py
```

Server sẽ khởi động trên `http://localhost:5000`

Các URLs khả dụng:

- API: `http://localhost:5000` (các endpoints gốc)
- Metrics: `http://localhost:5000/metrics`
- Health: `http://localhost:5000/health`

## 8. Monitoring Best Practices

### Prometheus Queries

```promql
# Total requests
rate(http_requests_total[5m])

# Average response time
rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])

# Failed requests
rate(http_requests_total{status=~"4.."}[5m])

# Rate limit hits
rate(rate_limit_hits_total[5m])
```

### Log Queries

Có thể phân tích logs JSON:

```bash
# Lấy tất cả login attempts
grep '"message": ".*login' logs/app.log

# Lấy error logs
cat logs/app_error.log
```

## 9. Troubleshooting

### Metrics không xuất hiện

- Đảm bảo Flask app đã chạy
- Kiểm tra `/metrics` endpoint có trả về dữ liệu

### Rate limit không hoạt động

- Kiểm tra `flask-limiter` đã được install
- Xem logs để tìm lỗi

### Logs không được ghi

- Kiểm tra thư mục `logs/` có tồn tại
- Kiểm tra quyền ghi file

## 10. Tùy chỉnh nâng cao

### Thay đổi log level

Chỉnh sửa trong `config/logging_config.py`:

```python
root_logger.setLevel(logging.DEBUG)  # Hoặc INFO, WARNING, ERROR
```

### Thay đổi Storage cho rate limiter

Mặc định dùng memory, có thể dùng Redis:

```python
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
```

### Custom Metrics

Thêm metrics mới trong `monitoring/metrics.py`:

```python
from prometheus_client import Counter

MY_METRIC = Counter(
    'my_metric_total',
    'Mô tả',
    ['label1', 'label2']
)

# Sử dụng
MY_METRIC.labels(label1='value1', label2='value2').inc()
```
