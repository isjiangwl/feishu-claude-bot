# 飞书 Claude 机器人

一个连接飞书和 Claude AI 的机器人，让你在飞书中直接与 Claude 对话。

## 功能

- ✅ 在飞书中与 Claude 对话
- ✅ 支持上下文记忆（会话历史）
- ✅ 支持多用户并发
- ✅ Docker 一键部署

## 部署步骤

### 1. 准备工作

确保你已经有：
- 飞书自建应用（App ID 和 App Secret）
- Anthropic API Key
- 服务器（公网可访问）

### 2. 配置飞书应用

1. 登录 [飞书开放平台](https://open.feishu.cn/)
2. 进入你的应用 → 添加应用能力 → 机器人
3. 权限管理 → 添加以下权限：
   - `im:message` - 获取与发送单聊、群组消息
   - `im:message:send_as_bot` - 以应用的身份发消息
4. 事件与回调 → 事件配置：
   - 请求地址：`https://你的服务器地址/webhook/event`
   - 订阅事件：`im.message.receive_v1`（接收消息）
5. 复制 Encrypt Key 和 Verification Token

### 3. 部署服务

#### 方式 A：Docker 部署（推荐）

```bash
# 克隆项目
git clone <项目地址>
cd feishu-claude-bot

# 修改 .env 文件，填入你的配置
# 已经预填了你的配置，确认无误即可

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

#### 方式 B：直接运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

### 4. 配置飞书回调地址

1. 确保服务已启动且公网可访问
2. 在飞书开放平台的事件配置中：
   - 填写请求地址：`https://你的服务器/webhook/event`
   - 点击保存，飞书会发送验证请求
3. 如果验证失败，检查服务日志

### 5. 测试机器人

1. 在飞书中搜索你的机器人名称
2. 发送消息测试

## 配置说明

### .env 文件

```env
# 飞书应用凭据（必填）
FEISHU_APP_ID=cli_xxxxx
FEISHU_APP_SECRET=xxxxx
FEISHU_ENCRYPT_KEY=xxxxx
FEISHU_VERIFICATION_TOKEN=xxxxx

# Anthropic API Key（必填）
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Claude 模型配置（可选）
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=2048

# 服务端口（可选）
PORT=8080
```

## 常见问题

### 1. 回调地址验证失败

- 确保服务已启动且公网可访问
- 检查防火墙是否开放 8080 端口
- 查看服务日志排查错误

### 2. Claude API 调用失败

- 检查 API Key 是否正确
- 确认账户有余额或在免费额度内
- 检查网络是否能访问 Anthropic API

### 3. 机器人不回复消息

- 检查是否配置了正确的事件订阅
- 确认应用已发布上线
- 查看服务日志是否有错误

## 技术栈

- Python 3.11
- Flask
- Anthropic SDK
- 飞书开放平台 API

## 许可证

MIT License
