import subprocess
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# التوكن وأي دي المستخدم
TOKEN = "7916824366:AAF27FerQ0raPQ3VoPRtxQ_FUhWrdEOeELc"
AUTHORIZED_USER_ID = 5833417353  # فقط هذا المستخدم يمكنه استخدام البوت

# إعدادات تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة للتأكد من هوية المستخدم
def check_authorization(update: Update):
    user_id = update.message.from_user.id
    if user_id != AUTHORIZED_USER_ID:
        update.message.reply_text("أنت غير مفوض لاستخدام هذا البوت.")
        return False
    return True

# دالة لعرض الأزرار التفاعلية التي تنفذ الأوامر
def start(update: Update, context: CallbackContext):
    if not check_authorization(update):
        return

    keyboard = [
        [InlineKeyboardButton("تشغيل Metasploit", callback_data='run_metasploit')],
        [InlineKeyboardButton("عرض معلومات النظام", callback_data='system_info')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر الأداة التي تريد تشغيلها:', reply_markup=reply_markup)

# دالة لتشغيل الأوامر بناءً على الضغط على الأزرار
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # تأكيد أن المستخدم ضغط على الزر

    tool_name = query.data

    if tool_name == 'run_metasploit':
        # تنفيذ سكربت Metasploit
        query.edit_message_text(text="بدء تثبيت وتشغيل Metasploit... يرجى الانتظار.")
        
        # التحقق من وجود السكربت
        script_path = "scripts/metasploit.sh"
        if not os.path.exists(script_path):
            query.edit_message_text(text="السكربت غير موجود!")
            return
        
        # منح صلاحيات تنفيذ للسكربت
        subprocess.run(['chmod', '+x', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # تنفيذ السكربت
        try:
            result = subprocess.run(['bash', script_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                query.edit_message_text(f"تم تثبيت Metasploit بنجاح!\n\n{result.stdout}")
            else:
                query.edit_message_text(f"فشل التثبيت:\n{result.stderr}")
        except Exception as e:
            query.edit_message_text(f"حدث خطأ أثناء تنفيذ السكربت: {str(e)}")

    elif tool_name == 'system_info':
        # أداة لعرض معلومات النظام
        try:
            result = subprocess.run(['uname', '-a'], capture_output=True, text=True)
            query.edit_message_text(f"معلومات النظام:\n{result.stdout}")
        except Exception as e:
            query.edit_message_text(f"حدث خطأ أثناء الحصول على معلومات النظام: {str(e)}")
    else:
        query.edit_message_text(text="أداة غير معروفة. حاول مرة أخرى.")

# دالة للتعامل مع الأخطاء
def error(update: Update, context: CallbackContext):
    logger.warning(f"بعض الأخطاء حدثت: {context.error}")

# الدالة الرئيسية لإعداد البوت
def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    # إضافة الأمر الذي سيشغل الأزرار التفاعلية
    dp.add_handler(CommandHandler("start", start))

    # إضافة معالج الزر التفاعلي
    dp.add_handler(CallbackQueryHandler(button))

    # إضافة معالج الأخطاء
    dp.add_error_handler(error)

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
