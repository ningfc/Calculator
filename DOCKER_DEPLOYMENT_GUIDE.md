# Docker 部署完整流程

本指南详细说明如何使用Docker部署沙盘摄像头安装计算器应用。

## 🐳 准备工作

### 1. 安装Docker和Docker Compose

#### macOS
```bash
# 下载并安装Docker Desktop
# 从 https://docs.docker.com/desktop/mac/install/ 下载
# 或使用Homebrew
brew install --cask docker
```

#### Linux (Ubuntu/Debian)
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 添加用户到docker组
sudo usermod -aG docker $USER
# 重新登录以生效
```

#### Windows
```bash
# 下载并安装Docker Desktop
# 从 https://docs.docker.com/desktop/windows/install/ 下载
```

### 2. 验证安装
```bash
docker --version
docker-compose --version
```

## 🚀 快速部署

### 方式一：使用 Docker Compose（推荐）

```bash
# 1. 克隆项目（如果还没有）
git clone <repository-url>
cd Calculator

# 2. 一键启动
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs camera-calculator
```

### 方式二：手动Docker命令

```bash
# 1. 构建镜像
docker build -t camera-calculator .

# 2. 运行容器
docker run -d \
  --name camera-calculator \
  -p 8501:8501 \
  -v $(pwd)/output:/app/output \
  camera-calculator

# 3. 查看状态
docker ps
```

## 📋 部署配置详解

### Docker Compose 配置

项目包含两个服务配置：

#### 生产环境服务 (`camera-calculator`)
- **端口**: 8501
- **特点**: 稳定版本，不会自动重载
- **适用**: 生产环境部署

#### 开发环境服务 (`camera-calculator-dev`)
- **端口**: 8502
- **特点**: 支持热重载，代码变更自动更新
- **适用**: 开发调试

### 环境变量说明

| 变量名 | 作用 | 默认值 |
|--------|------|--------|
| `PYTHONPATH` | Python模块路径 | `/app` |
| `MPLBACKEND` | matplotlib后端 | `Agg` |
| `LANG` | 系统语言 | `C.UTF-8` |
| `LC_ALL` | 本地化设置 | `C.UTF-8` |

### 数据卷挂载

- `./output:/app/output` - 输出文件持久化存储

## 🔧 部署操作命令

### 基础操作

```bash
# 启动服务（后台运行）
docker-compose up -d

# 启动服务（前台运行，查看日志）
docker-compose up

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f camera-calculator
```

### 镜像管理

```bash
# 重新构建镜像
docker-compose build

# 强制重新构建（不使用缓存）
docker-compose build --no-cache

# 拉取最新镜像
docker-compose pull

# 查看镜像
docker images | grep camera-calculator
```

### 容器管理

```bash
# 进入容器
docker-compose exec camera-calculator bash

# 查看容器资源使用
docker stats camera-calculator

# 查看容器详细信息
docker inspect camera-calculator
```

## 🌐 访问应用

部署成功后，可通过以下地址访问：

- **生产版本**: http://localhost:8501
- **开发版本**: http://localhost:8502（如果启动了dev服务）

### 外网访问配置

如需外网访问，需要配置防火墙和端口转发：

```bash
# Linux防火墙配置
sudo ufw allow 8501

# 使用nginx反向代理（可选）
# 在/etc/nginx/sites-available/camera-calculator中配置：
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔍 故障排除

### 常见问题及解决方案

#### 1. 容器启动失败
```bash
# 查看错误日志
docker-compose logs camera-calculator

# 检查端口占用
lsof -i :8501
netstat -tulpn | grep 8501
```

#### 2. 中文字体显示问题
```bash
# 进入容器检查字体
docker-compose exec camera-calculator bash
fc-list | grep -i "noto\|wqy"

# 如果字体缺失，重新构建镜像
docker-compose build --no-cache
```

#### 3. 文件权限问题
```bash
# 修复输出目录权限
sudo chown -R $USER:$USER ./output
chmod 755 ./output
```

#### 4. 内存不足
```bash
# 查看容器资源使用
docker stats

# 增加内存限制（在docker-compose.yml中）
services:
  camera-calculator:
    # ... 其他配置
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

### 日志分析

```bash
# 查看最近100行日志
docker-compose logs --tail=100 camera-calculator

# 查看特定时间范围的日志
docker-compose logs --since="2023-01-01T00:00:00" camera-calculator

# 持续监控日志
docker-compose logs -f camera-calculator
```

## 🔄 更新部署

### 代码更新
```bash
# 1. 拉取最新代码
git pull origin main

# 2. 停止当前服务
docker-compose down

# 3. 重新构建并启动
docker-compose up -d --build
```

### 配置更新
```bash
# 仅重启服务（不重新构建）
docker-compose restart

# 重新加载配置
docker-compose up -d
```

## 📊 生产环境部署建议

### 1. 安全配置
```bash
# 使用非root用户运行
# 在Dockerfile中添加：
RUN useradd -m -u 1000 appuser
USER appuser
```

### 2. 资源限制
```yaml
# docker-compose.yml
services:
  camera-calculator:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 512M
```

### 3. 健康检查
```yaml
# docker-compose.yml
services:
  camera-calculator:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 4. 日志管理
```yaml
# docker-compose.yml
services:
  camera-calculator:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 🎯 部署验证

### 功能测试脚本
```bash
# 创建测试脚本
cat > test_deployment.sh << 'EOF'
#!/bin/bash

echo "Testing deployment..."

# 检查服务状态
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ Service is healthy"
else
    echo "❌ Service health check failed"
    exit 1
fi

# 检查输出目录
if [ -d "./output" ]; then
    echo "✅ Output directory exists"
else
    echo "❌ Output directory not found"
    exit 1
fi

echo "🎉 Deployment test passed!"
EOF

chmod +x test_deployment.sh
./test_deployment.sh
```

### 性能测试
```bash
# 使用ab进行简单压力测试
apt-get install apache2-utils
ab -n 100 -c 10 http://localhost:8501/
```

## 📝 部署清单

部署前检查清单：

- [ ] Docker和Docker Compose已安装
- [ ] 项目代码已获取
- [ ] 端口8501未被占用
- [ ] 有足够的磁盘空间（至少2GB）
- [ ] 网络连接正常，可拉取镜像
- [ ] 输出目录权限正确
- [ ] 防火墙规则已配置（如需外网访问）

部署后验证清单：

- [ ] 容器正常运行
- [ ] Web界面可访问
- [ ] 中文字体显示正常
- [ ] 图表生成功能正常
- [ ] 文件输出功能正常
- [ ] 日志无错误信息

## 📞 技术支持

如遇到部署问题，请提供以下信息：

1. 操作系统版本
2. Docker版本
3. 错误日志
4. 网络环境信息

通过Issue或邮件联系获取支持。