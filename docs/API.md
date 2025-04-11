# Mirror Reality API 文档

## 1. 概述

Mirror Reality API 提供了与数字镜像交互的完整接口，包括创建、训练、查询和管理镜像等功能。

## 2. 基础信息

- **基础 URL**: `http://localhost:8000/api/v1`
- **认证方式**: Bearer Token
- **响应格式**: JSON

## 3. 认证

所有 API 请求必须在 Header 中包含认证信息：

```
Authorization: Bearer <token>
```

## 4. 错误码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 5. API 端点

### 5.1 镜像管理

#### 创建镜像
- **URL**: `/mirrors`
- **方法**: POST
- **请求体**:
```json
{
    "name": "string",
    "description": "string",
    "model_type": "string",
    "training_data": {
        "text": "string",
        "voice": "string",
        "image": "string"
    }
}
```
- **响应**:
```json
{
    "id": "string",
    "name": "string",
    "status": "string",
    "created_at": "string"
}
```

#### 获取镜像信息
- **URL**: `/mirrors/{id}`
- **方法**: GET
- **响应**:
```json
{
    "id": "string",
    "name": "string",
    "description": "string",
    "status": "string",
    "created_at": "string",
    "updated_at": "string"
}
```

#### 训练镜像
- **URL**: `/mirrors/{id}/train`
- **方法**: POST
- **请求体**:
```json
{
    "training_data": {
        "text": "string",
        "voice": "string",
        "image": "string"
    }
}
```
- **响应**:
```json
{
    "status": "string",
    "progress": "float",
    "estimated_time": "string"
}
```

#### 生成响应
- **URL**: `/mirrors/{id}/generate`
- **方法**: POST
- **请求体**:
```json
{
    "input": "string",
    "type": "string"
}
```
- **响应**:
```json
{
    "output": "string",
    "confidence": "float"
}
```

#### 停用镜像
- **URL**: `/mirrors/{id}/deactivate`
- **方法**: POST
- **响应**:
```json
{
    "status": "string",
    "message": "string"
}
```

### 5.2 用户管理

#### 获取用户信息
- **URL**: `/users/me`
- **方法**: GET
- **响应**:
```json
{
    "id": "string",
    "username": "string",
    "email": "string",
    "created_at": "string"
}
```

#### 更新用户信息
- **URL**: `/users/me`
- **方法**: PUT
- **请求体**:
```json
{
    "username": "string",
    "email": "string"
}
```
- **响应**:
```json
{
    "id": "string",
    "username": "string",
    "email": "string",
    "updated_at": "string"
}
```

## 6. WebSocket 接口

### 6.1 镜像状态更新
- **URL**: `ws://localhost:8000/api/v1/mirrors/{id}/status`
- **事件**:
  - `status_update`: 镜像状态更新
  - `training_progress`: 训练进度更新
  - `error`: 错误信息

## 7. 示例代码

### Python
```python
import requests

headers = {
    "Authorization": "Bearer <token>",
    "Content-Type": "application/json"
}

# 创建镜像
response = requests.post(
    "http://localhost:8000/api/v1/mirrors",
    headers=headers,
    json={
        "name": "My Mirror",
        "description": "A personal digital mirror",
        "model_type": "text",
        "training_data": {
            "text": "Hello, I am your digital mirror."
        }
    }
)
```

### JavaScript
```javascript
const createMirror = async () => {
    const response = await fetch('http://localhost:8000/api/v1/mirrors', {
        method: 'POST',
        headers: {
            'Authorization': 'Bearer <token>',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: 'My Mirror',
            description: 'A personal digital mirror',
            model_type: 'text',
            training_data: {
                text: 'Hello, I am your digital mirror.'
            }
        })
    });
    return await response.json();
};
```

## 8. 注意事项

1. **时间戳格式**: ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
2. **ID 格式**: UUID v4
3. **字符串编码**: UTF-8
4. **数字格式**: 浮点数使用 IEEE 754
5. **布尔值**: true/false
6. **数组格式**: JSON 数组
7. **对象格式**: JSON 对象 