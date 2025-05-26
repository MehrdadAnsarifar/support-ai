from flask import Blueprint, jsonify, request, render_template
from app.chat import ChatManager
from app.config import get_system_prompt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

chat_sessions = {}

def get_chat_manager(username):
    if username not in chat_sessions:
        chat_sessions[username] = ChatManager()
        # فقط هنگام ساخت چت منیجر، پرامپت را ست کن
        chat_sessions[username].set_system_prompt(get_system_prompt())
    return chat_sessions[username]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message')
        username = data.get('username')
        
        if not all([message, username]):
            return jsonify({
                'error': 'Missing required fields',
                'status': 'error'
            }), 400
        
        chat_manager = get_chat_manager(username)
        # دیگر نیازی به set_system_prompt اینجا نیست
        
        response = chat_manager.send_message(message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        
        return jsonify({
            'response': 'پشتیبان‌ها در دسترس نیستند، لطفا ساعاتی بعد پیام دهید 🙏',
            'status': 'error'
        })

@main.route('/api/report-bug', methods=['POST'])
def report_bug():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        username = data.get('username')

        sender_email = "your-email@gmail.com"  
        sender_password = "your-app-password"  
        receiver_email = "mehrdadansarifar@outlook.com"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"گزارش باگ - {title}"

        body = f"""
        گزارش باگ جدید:
        
        عنوان: {title}
        توضیحات: {description}
        کاربر: {username}
        """

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(message)

        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error in report-bug endpoint: {str(e)}", exc_info=True)
        
        return jsonify({
            'response': 'متأسفانه در حال حاضر امکان ارسال گزارش وجود ندارد. لطفا ساعاتی بعد تلاش کنید 🙏',
            'status': 'error'
        })