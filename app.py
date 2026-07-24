import os
import json
import hashlib
import logging
from flask import Flask, request, jsonify
from anthropic import Anthropic
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 配置
FEISHU_APP_ID = os.getenv('FEISHU_APP_ID')
FEISHU_APP_SECRET = os.getenv('FEISHU_APP_SECRET')
FEISHU_ENCRYPT_KEY = os.getenv('FEISHU_ENCRYPT_KEY')
FEISHU_VERIFICATION_TOKEN = os.getenv('FEISHU_VERIFICATION_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
CLAUDE_MAX_TOKENS = int(os.getenv('CLAUDE_MAX_TOKENS', '2048'))

# Anthropic 客户端
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# 存储会话历史（生产环境应使用 Redis 等持久化存储）
conversation_history = {}


def get_tenant_access_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("tenant_access_token")


def send_feishu_message(chat_id, content, msg_type="text"):
    """发送消息到飞书"""
    token = get_tenant_access_token()
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "receive_id": chat_id,
        "msg_type": msg_type,
        "content": json.dumps(content)
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def call_claude(user_message, chat_id):
    """调用 Claude API"""
    # 获取或初始化对话历史
    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    # 添加用户消息
    conversation_history[chat_id].append({
        "role": "user",
        "content": user_message
    })

    # 限制历史长度，避免 token 超限
    if len(conversation_history[chat_id]) > 20:
        conversation_history[chat_id] = conversation_history[chat_id][-20:]

    try:
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=conversation_history[chat_id]
        )
        assistant_message = response.content[0].text

        # 添加助手回复到历史
        conversation_history[chat_id].append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message
    except Exception as e:
        logger.error(f"Claude API error: {e}")
        return f"抱歉，调用 Claude 时出错：{str(e)}"


@app.route("/webhook/event", methods=["POST"])
def feishu_event():
    """飞书事件订阅回调"""
    data = request.json

    # 处理 URL 验证
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})

    # 验证 token
    token = data.get("header", {}).get("token") or data.get("token")
    if token != FEISHU_VERIFICATION_TOKEN:
        logger.warning("Invalid verification token")
        return jsonify({"code": 403, "msg": "Invalid token"}), 403

    # 处理消息事件
    event = data.get("event", {})
    event_type = data.get("header", {}).get("event_type")

    if event_type == "im.message.receive_v1":
        message = event.get("message", {})
        chat_id = message.get("chat_id")
        msg_type = message.get("message_type")
        content = json.loads(message.get("content", "{}"))

        # 只处理文本消息
        if msg_type == "text":
            user_text = content.get("text", "").strip()

            # 忽略空消息和机器人自己的消息
            sender = event.get("sender", {})
            sender_type = sender.get("sender_id", {}).get("open_id")

            if user_text and sender_type:
                logger.info(f"Received message: {user_text}")
                reply = call_claude(user_text, chat_id)

                # 发送回复
                reply_content = {"text": reply}
                send_feishu_message(chat_id, reply_content)

    return jsonify({"code": 0, "msg": "success"})


@app.route("/", methods=["GET"])
def index():
    """健康检查"""
    return "Feishu Claude Bot is running!"


@app.route("/health", methods=["GET"])
def health():
    """健康检查端点"""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logger.info(f"Starting Feishu Claude Bot on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
