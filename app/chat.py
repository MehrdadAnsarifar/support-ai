from g4f.client import Client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatManager:
    def set_system_prompt(self, prompt):
        self.system_prompt = prompt
        self.reset_history()
        
    def __init__(self):
        self.client = Client()
        self.model = "gpt-4o-mini"

        # Define and inject system prompt at init time
        self.system_prompt = (
            "شما یک دستیار هوشمند برای پشتیبانی فنی هستید. حوزه کاری شما محدود به موارد زیر است:\n\n"
            "1. مشکلات فنی محصولات و خدمات\n"
            "2. راهنمایی در مورد نحوه استفاده از محصولات\n"
            "3. عیب‌یابی و رفع مشکلات\n"
            "4. پاسخ به سؤالات فنی\n"
            "5. راهنمایی در مورد ویژگی‌های محصولات\n\n"
            "قوانین پاسخ‌دهی:\n"
            "- فقط به سؤالات مرتبط با حوزه پشتیبانی فنی پاسخ دهید\n"
            "- اگر سؤالی خارج از حوزه کاری شما پرسیده شد، محترمانه به کاربر اطلاع دهید که فقط در زمینه پشتیبانی فنی می‌توانید کمک کنید\n"
            "- از پاسخ دادن به سؤالات شخصی، مالی، حقوقی یا هر موضوع غیر مرتبط خودداری کنید\n"
            "- اگر سؤالی مبهم است، برای درک بهتر مشکل از کاربر توضیح بیشتری بخواهید\n"
            "- همیشه با لحن دوستانه و حرفه‌ای پاسخ دهید\n"
            "- پاسخ‌ها را مرحله‌به‌مرحله و با جزئیات کافی ارائه دهید\n"
            "- در صورت نیاز به اطلاعات بیشتر، با لحن دوستانه سؤال بپرسید\n"
            "- اگر در مورد موضوعی مطمئن نیستید، صادقانه به کاربر اطلاع دهید\n\n"
            "یادآوری: فقط یک دستیار پشتیبانی فنی هستید و نباید به سؤالات خارج از این حوزه پاسخ دهید."
        )
        
        # Inject system prompt into conversation history
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        logger.info("System prompt injected into history.")

    def reset_history(self):
        """Reset conversation history and re-inject system prompt."""
        self.conversation_history = [{"role": "system", "content": self.system_prompt}]
        logger.info("Conversation history reset.")

    def send_message(self, user_message):
        """Send a message and get AI response."""
        try:
            self.conversation_history.append({"role": "user", "content": user_message})
            logger.info(f"User message: {user_message[:50]}...")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                web_search=False
            )

            ai_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            logger.info(f"AI response: {ai_response[:50]}...")

            return ai_response

        except Exception as e:
            logger.exception("Error during message send.")
            return f"متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید. (جزئیات خطا: {str(e)})"
