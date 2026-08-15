import os
import json
import time
import logging
import requests
import threading
from flask import Flask

# ============ تنظیمات ============
BOT_TOKEN = os.environ.get("BOT_TOKEN", "TOKEN")
ADMIN_ID_RAW = os.environ.get("ADMIN_ID", "0")

try:
    if "," in ADMIN_ID_RAW:
        DEFAULT_ADMIN_IDS = [int(x.strip()) for x in ADMIN_ID_RAW.split(",") if x.strip()]
    else:
        DEFAULT_ADMIN_IDS = [int(ADMIN_ID_RAW)]
except ValueError:
    DEFAULT_ADMIN_IDS = [0]

SUPER_ADMIN_ID = DEFAULT_ADMIN_IDS[0] if DEFAULT_ADMIN_IDS else 0
DATA_FILE = "data.json"
PORT = int(os.environ.get("PORT", 10000))

BALE_API = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# استیکرهای دسته
DEFAULT_CAT_ICONS = {
    "ادویه جات ترکیبی گهنیج": "🔬",
    "چاشنی های گهنیج": "🧂",
    "ادویه جات اصلی": "🌿",
    "دانه ها و تخم ها": "🌰",
    "طعم دهنده ها": "🍋",
    "سبزی خشک و متفرقه": "🥬",
    "عرقیجات خالص": "🌸",
    "زردچوبه چارمنار": "💛",
}

DEFAULT_CAT_ORDER = [
    "ادویه جات ترکیبی گهنیج",
    "چاشنی های گهنیج",
    "ادویه جات اصلی",
    "دانه ها و تخم ها",
    "طعم دهنده ها",
    "سبزی خشک و متفرقه",
    "عرقیجات خالص",
    "زردچوبه چارمنار",
]

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ============ Flask (برای بیدار موندن) ============
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات فروشگاه گهنیج در بله فعال است 🌿"

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

# ============ دیتابیس ============
def get_default_data():
    return {
        "categories": {
            "ادویه جات ترکیبی گهنیج": {
                "ادویه مامان بلوچی (قوطی مربعی 130گ)": {"price": 200000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه مامان بلوچی (پاکت نیم کیلویی)": {"price": 600000, "unit": "پاکت نیم کیلویی"},
                "ادویه بریانی بلوچی (قوطی مربعی 130گ)": {"price": 170000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه بریانی بلوچی (پاکت نیم کیلویی)": {"price": 435000, "unit": "پاکت نیم کیلویی"},
                "ادویه عربی مخصوص (قوطی مربعی 130گ)": {"price": 370000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه عربی مخصوص (پاکت نیم کیلویی)": {"price": 1245000, "unit": "پاکت نیم کیلویی"},
                "ادویه کاری مخصوص (قوطی مربعی 130گ)": {"price": 180000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه کاری مخصوص (پاکت نیم کیلویی)": {"price": 480000, "unit": "پاکت نیم کیلویی"},
                "ادویه ماهی و میگو (قوطی مربعی 130گ)": {"price": 200000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه ماهی و میگو (پاکت نیم کیلویی)": {"price": 570000, "unit": "پاکت نیم کیلویی"},
                "ادویه کباب (قوطی مربعی 130گ)": {"price": 170000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه کباب (پاکت نیم کیلویی)": {"price": 470000, "unit": "پاکت نیم کیلویی"},
                "ادویه کرایی بلوچی (قوطی مربعی 130گ)": {"price": 200000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه کرایی بلوچی (پاکت نیم کیلویی)": {"price": 610000, "unit": "پاکت نیم کیلویی"},
                "ادویه کاچی (قوطی مربعی 130گ)": {"price": 170000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه کاچی (پاکت نیم کیلویی)": {"price": 500000, "unit": "پاکت نیم کیلویی"},
                "ادویه کاجون (قوطی مربعی 130گ)": {"price": 170000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه کاجون (پاکت نیم کیلویی)": {"price": 480000, "unit": "پاکت نیم کیلویی"},
                "ادویه مرغ (قوطی مربعی 130گ)": {"price": 180000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه مرغ (نیم کیلویی پاکت)": {"price": 500000, "unit": "پاکت نیم کیلویی"},
                "ادویه سمبوسه (قوطی مربعی 130گ)": {"price": 220000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه سمبوسه (پاکت نیم کیلویی)": {"price": 660000, "unit": "پاکت نیم کیلویی"},
                "ادویه گراماسالا (قوطی مربعی 130گ)": {"price": 320000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه گراماسالا (پاکت نیم کیلویی)": {"price": 1035000, "unit": "پاکت نیم کیلویی"},
                "ادویه فلافل (قوطی مربعی 130گ)": {"price": 180000, "unit": "قوطی مربعی 130 گرم"},
                "ادویه پکوره (قوطی مربعی 130گ)": {"price": 120000, "unit": "قوطی مربعی 130 گرم"},
            },
            "چاشنی های گهنیج": {
                "پودر لیمو عمانی (نمکپاشی)": {"price": 110000, "unit": "نمکپاشی"},
                "چاشنی ماست (نمکپاشی)": {"price": 120000, "unit": "نمکپاشی"},
                "چاشنی ماست (نیم کیلویی)": {"price": 475000, "unit": "نیم کیلویی"},
                "ادویه سوسیس بندری (قوطی مربعی)": {"price": 200000, "unit": "قوطی مربعی"},
                "ادویه سوسیس بندری (نیم کیلویی)": {"price": 590000, "unit": "نیم کیلویی"},
                "چاشنی زعتر (نمکپاشی)": {"price": 150000, "unit": "نمکپاشی"},
                "چاشنی زعتر (نیم کیلویی)": {"price": 490000, "unit": "نیم کیلویی"},
                "چاشنی املت (نمکپاشی)": {"price": 120000, "unit": "نمکپاشی"},
                "چاشنی املت (نیم کیلویی)": {"price": 300000, "unit": "نیم کیلویی"},
                "چاشنی سیب زمینی (نمکپاشی)": {"price": 150000, "unit": "نمکپاشی"},
                "چاشنی سیب زمینی (نیم کیلویی)": {"price": 460000, "unit": "نیم کیلویی"},
                "ایتالیایی (نمکپاشی)": {"price": 150000, "unit": "نمکپاشی"},
                "ایتالیایی (نیم کیلویی)": {"price": 555000, "unit": "نیم کیلویی"},
                "ادویه ماکارونی (نمکپاشی)": {"price": 150000, "unit": "نمکپاشی"},
                "ادویه ماکارونی (نیم کیلویی)": {"price": 490000, "unit": "نیم کیلویی"},
                "فلفل سیاه (نمکپاشی)": {"price": 220000, "unit": "نمکپاشی"},
                "فلفل سیاه (نیم کیلویی)": {"price": 950000, "unit": "نیم کیلویی"},
                "فلفل سیاه (نکوبیده قوطی 150گ)": {"price": 300000, "unit": "قوطی 150 گرم"},
                "دارچین (نمکپاشی)": {"price": 100000, "unit": "نمکپاشی"},
                "دارچین (نیم کیلویی)": {"price": 395000, "unit": "نیم کیلویی"},
                "دارچین (سالم 150 گ)": {"price": 150000, "unit": "قوطی 150 گرم سالم"},
                "پودر فلفل قرمز تند چیلی (نمکپاشی)": {"price": 150000, "unit": "نمکپاشی"},
                "پودر فلفل قرمز تند چیلی (نیم کیلویی)": {"price": 640000, "unit": "نیم کیلویی"},
            },
            "ادویه جات اصلی": {
                "پودر پاپریکا (قوطی مربعی)": {"price": 150000, "unit": "قوطی مربعی"},
                "پودر پاپریکا (پاکت نیم کیلویی)": {"price": 360000, "unit": "پاکت نیم کیلویی"},
                "پودر سیر خالص (قوطی 180 گ)": {"price": 220000, "unit": "قوطی 180 گرم"},
                "پودر سیر خالص (پاکت نیم کیلویی)": {"price": 500000, "unit": "پاکت نیم کیلویی"},
                "زیره سبز (قوطی مربعی)": {"price": 130000, "unit": "قوطی مربعی"},
                "زیره سبز (پاکت نیم کیلویی)": {"price": 360000, "unit": "پاکت نیم کیلویی"},
                "زیره سیاه (قوطی مربعی)": {"price": 410000, "unit": "قوطی مربعی"},
                "زیره سیاه (پاکت نیم کیلویی)": {"price": 1330000, "unit": "پاکت نیم کیلویی"},
                "زنجبیل (قوطی مربعی)": {"price": 140000, "unit": "قوطی مربعی"},
                "زنجبیل (پاکت نیم کیلویی)": {"price": 480000, "unit": "پاکت نیم کیلویی"},
                "پودر گشنیز (قوطی مربعی)": {"price": 100000, "unit": "قوطی مربعی"},
                "پودر گشنیز (پاکت نیم کیلویی)": {"price": 280000, "unit": "پاکت نیم کیلویی"},
                "تخم گشنیز (قوطی مربعی)": {"price": 80000, "unit": "قوطی مربعی"},
                "تخم گشنیز (پاکت نیم کیلویی)": {"price": 280000, "unit": "پاکت نیم کیلویی"},
            },
            "دانه ها و تخم ها": {
                "دانه چیا (200 گرمی)": {"price": 190000, "unit": "قوطی 200 گرم"},
                "خاکشیر (200 گرمی)": {"price": 120000, "unit": "قوطی 200 گرم"},
                "تخم شربتی ریز": {"price": 180000, "unit": "قوطی"},
                "تخم شربتی درشت": {"price": 140000, "unit": "قوطی"},
                "سیاهدانه": {"price": 200000, "unit": "قوطی"},
                "بارهنگ": {"price": 160000, "unit": "قوطی"},
                "پاپ کورن بزرگ (800 گ)": {"price": 330000, "unit": "قوطی 800 گرم"},
                "اسپند": {"price": 80000, "unit": "قوطی"},
                "تخم زنیان": {"price": 120000, "unit": "قوطی"},
            },
            "طعم دهنده ها": {
                "آروماتز": {"price": 170000, "unit": "قوطی"},
                "سیر و کره": {"price": 150000, "unit": "قوطی"},
                "دود": {"price": 120000, "unit": "قوطی"},
                "قارچ و خامه": {"price": 180000, "unit": "قوطی"},
                "کره": {"price": 100000, "unit": "قوطی"},
                "لیمو فلفلی زرد": {"price": 150000, "unit": "قوطی"},
                "لیمو فلفلی چاشنی": {"price": 190000, "unit": "قوطی"},
                "پنیر چدار": {"price": 120000, "unit": "قوطی"},
                "پیاز جعفری": {"price": 150000, "unit": "قوطی"},
                "کچاپ": {"price": 150000, "unit": "قوطی"},
                "سماق": {"price": 200000, "unit": "قوطی"},
                "ادویه انبه": {"price": 150000, "unit": "قوطی"},
                "پودر آویشن": {"price": 200000, "unit": "قوطی"},
                "ادویه برگر": {"price": 150000, "unit": "قوطی"},
                "پودر لیمو": {"price": 110000, "unit": "قوطی"},
                "پودر لبو": {"price": 120000, "unit": "قوطی"},
                "عصاره مرغ": {"price": 120000, "unit": "قوطی"},
            },
            "سبزی خشک و متفرقه": {
                "فلفل لاهوری (کناری)": {"price": 200000, "unit": "بسته"},
                "نعناع خشک بزرگ": {"price": 220000, "unit": "بسته بزرگ"},
                "نعناع خشک متوسط": {"price": 160000, "unit": "بسته متوسط"},
                "شوید خشک بزرگ": {"price": 220000, "unit": "بسته بزرگ"},
                "شنبلیله خشک": {"price": 230000, "unit": "بسته"},
                "ترخون خشک": {"price": 260000, "unit": "بسته"},
                "رزماری خشک قوطی": {"price": 70000, "unit": "قوطی"},
                "برگ بو (40 گرم)": {"price": 100000, "unit": "بسته 40 گرم"},
                "هل اکبر بنفش (20 گرمی)": {"price": 270000, "unit": "بسته 20 گرم"},
                "نمک صورتی یک کیلو": {"price": 150000, "unit": "یک کیلو"},
                "پرک لیمو کوچک": {"price": 200000, "unit": "بسته کوچک"},
                "پرک لیمو بزرگ": {"price": 500000, "unit": "بسته بزرگ"},
                "رب انار ترش": {"price": 450000, "unit": "بسته"},
                "رب انار ترش متوسط": {"price": 420000, "unit": "بسته متوسط"},
                "آبغوره خالص": {"price": 250000, "unit": "بسته"},
                "غنچه گل محمدی": {"price": 300000, "unit": "بسته"},
                "گلرنگ (زردی) بسته 80 گ": {"price": 250000, "unit": "بسته 80 گرم"},
                "رب گوجه خالص خونگی 1100 گرم": {"price": 420000, "unit": "بسته 1100 گرم"},
            },
            "عرقیجات خالص": {
                "گلاب ویژه": {"price": 290000, "unit": "بطری"},
                "عرق نسترن": {"price": 190000, "unit": "بطری"},
                "عرق بهار نارنج": {"price": 220000, "unit": "بطری"},
                "عرق چهل گیاه": {"price": 200000, "unit": "بطری"},
                "عرق زنیان": {"price": 150000, "unit": "بطری"},
                "عرق بید مشک": {"price": 190000, "unit": "بطری"},
                "عرق آویشن": {"price": 150000, "unit": "بطری"},
                "عرق شاتره": {"price": 150000, "unit": "بطری"},
                "عرق رازیانه": {"price": 150000, "unit": "بطری"},
                "عرق شوید": {"price": 150000, "unit": "بطری"},
                "عرق خار مریم": {"price": 150000, "unit": "بطری"},
                "عرق خار شتر": {"price": 150000, "unit": "بطری"},
                "عرق زیره": {"price": 150000, "unit": "بطری"},
                "عرق کاسنی": {"price": 150000, "unit": "بطری"},
                "عرق طارونه": {"price": 150000, "unit": "بطری"},
                "معجون آرامش بخش": {"price": 270000, "unit": "بطری"},
                "معجون معده": {"price": 270000, "unit": "بطری"},
                "عرق نعناع": {"price": 220000, "unit": "بطری"},
            },
            "زردچوبه چارمنار": {
                "زردچوبه چارمنار (نیم کیلو)": {"price": 470000, "unit": "نیم کیلو"},
                "زردچوبه چارمنار (150 گرمی)": {"price": 180000, "unit": "150 گرمی"},
            },
        },
        "orders": [],
        "shipping_options": {
            "پست پیشتاز": 45000,
            "پست سفارشی": 30000,
            "تیپاکس": 65000,
            "پیک (تهران)": 50000
        },
        "card_number": "6037-XXXX-XXXX-XXXX",
        "card_holder": "نام صاحب فروشگاه",
        "contact_info": {
            "phone": "09XXXXXXXXX",
            "address": "تهران",
            "hours": "۹ صبح تا ۹ شب"
        },
        "admins": list(DEFAULT_ADMIN_IDS),
        "cat_icons": dict(DEFAULT_CAT_ICONS),
        "cat_order": list(DEFAULT_CAT_ORDER)
    }

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        data = get_default_data()
        save_data(data)
        return data

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def format_price(price):
    return f"{price:,} تومان"

def get_cat_icon(data, cat_name):
    icons = data.get("cat_icons", DEFAULT_CAT_ICONS)
    return icons.get(cat_name, "📂")

def get_ordered_categories(data):
    cat_order = data.get("cat_order", DEFAULT_CAT_ORDER)
    categories = data.get("categories", {})
    ordered = []
    for cat_name in cat_order:
        if cat_name in categories:
            ordered.append(cat_name)
    for cat_name in categories:
        if cat_name not in ordered:
            ordered.append(cat_name)
    return ordered

def is_admin(user_id):
    data = load_data()
    return user_id in data.get("admins", DEFAULT_ADMIN_IDS)

# ============ حالت کاربران (State Management) ============
user_states = {}  # {chat_id: {"state": "...", "data": {...}}}
user_carts = {}   # {chat_id: {product_name: qty}}

def get_state(chat_id):
    return user_states.get(chat_id, {}).get("state", "main")

def set_state(chat_id, state, data=None):
    user_states[chat_id] = {"state": state, "data": data or {}}

def get_state_data(chat_id):
    return user_states.get(chat_id, {}).get("data", {})

def clear_state(chat_id):
    user_states.pop(chat_id, None)

def get_cart(chat_id):
    if chat_id not in user_carts:
        user_carts[chat_id] = {}
    return user_carts[chat_id]

# ============ توابع Bale API ============
def bale_request(method, params=None, files=None):
    url = f"{BALE_API}/{method}"
    try:
        if files:
            r = requests.post(url, data=params, files=files, timeout=30)
        else:
            r = requests.post(url, json=params, timeout=30)
        return r.json()
    except Exception as e:
        logger.error(f"Bale API error: {e}")
        return None

def send_message(chat_id, text, keyboard=None, parse_mode=None):
    params = {"chat_id": chat_id, "text": text}
    if keyboard:
        params["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    if parse_mode:
        params["parse_mode"] = parse_mode
    return bale_request("sendMessage", params)

def edit_message(chat_id, message_id, text, keyboard=None):
    params = {"chat_id": chat_id, "message_id": message_id, "text": text}
    if keyboard:
        params["reply_markup"] = json.dumps({"inline_keyboard": keyboard})
    return bale_request("editMessageText", params)

def answer_callback(callback_id, text=""):
    return bale_request("answerCallbackQuery", {"callback_query_id": callback_id, "text": text})

def send_photo(chat_id, photo_file_id, caption=""):
    params = {"chat_id": chat_id, "photo": photo_file_id, "caption": caption}
    return bale_request("sendPhoto", params)

# ============ منوی اصلی ============
def show_main_menu(chat_id, user_name="کاربر"):
    text = (
        f"🌿 سلام {user_name} عزیز!\n\n"
        f"به فروشگاه ادویه جات گهنیج خوش آمدید 🌿\n\n"
        f"از منوی زیر انتخاب کنید:"
    )
    keyboard = [
        [{"text": "🛒 مشاهده محصولات", "callback_data": "browse"}],
        [{"text": "🛍 سبد خرید", "callback_data": "cart"}],
        [{"text": "📞 تماس با ما", "callback_data": "contact"}],
    ]
    if is_admin(chat_id):
        keyboard.append([{"text": "⚙️ پنل مدیریت", "callback_data": "admin"}])
    
    clear_state(chat_id)
    return send_message(chat_id, text, keyboard)

def show_categories(chat_id, message_id=None):
    data = load_data()
    text = "🌿 فروشگاه ادویه گهنیج\n\n📂 دسته بندی محصولات:\n\nلطفا یک دسته را انتخاب کنید:"
    keyboard = []
    
    ordered = get_ordered_categories(data)
    row = []
    for i, cat_name in enumerate(ordered):
        icon = get_cat_icon(data, cat_name)
        row.append({"text": f"{icon} {cat_name}", "callback_data": f"cat|{i}"})
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    keyboard.append([{"text": "🛍 سبد خرید", "callback_data": "cart"}])
    keyboard.append([{"text": "🔙 بازگشت", "callback_data": "back_main"}])
    
    if message_id:
        return edit_message(chat_id, message_id, text, keyboard)
    return send_message(chat_id, text, keyboard)

def show_category_products(chat_id, cat_index, message_id=None):
    data = load_data()
    ordered = get_ordered_categories(data)
    
    if cat_index >= len(ordered):
        return send_message(chat_id, "❌ دسته پیدا نشد!")
    
    cat_name = ordered[cat_index]
    icon = get_cat_icon(data, cat_name)
    products = data["categories"].get(cat_name, {})
    
    text = f"{icon} {cat_name}\n\nلطفا محصول مورد نظر خود را انتخاب کنید:"
    keyboard = []
    
    prod_list = list(products.keys())
    set_state(chat_id, "browsing", {"cat_index": cat_index, "products": prod_list})
    
    for i, prod_name in enumerate(prod_list):
        info = products[prod_name]
        keyboard.append([{
            "text": f"{icon} {prod_name} - {format_price(info['price'])}",
            "callback_data": f"prod|{cat_index}|{i}"
        }])
    
    keyboard.append([{"text": "🛍 سبد خرید", "callback_data": "cart"}])
    keyboard.append([{"text": "🔙 بازگشت به دسته ها", "callback_data": "browse"}])
    
    if message_id:
        return edit_message(chat_id, message_id, text, keyboard)
    return send_message(chat_id, text, keyboard)

def show_product(chat_id, cat_index, prod_index, message_id=None):
    data = load_data()
    ordered = get_ordered_categories(data)
    
    if cat_index >= len(ordered):
        return
    
    cat_name = ordered[cat_index]
    icon = get_cat_icon(data, cat_name)
    products = data["categories"].get(cat_name, {})
    prod_list = list(products.keys())
    
    if prod_index >= len(prod_list):
        return
    
    prod_name = prod_list[prod_index]
    product = products[prod_name]
    
    set_state(chat_id, "product", {"cat_index": cat_index, "prod_index": prod_index, "prod_name": prod_name})
    
    text = (
        f"{icon} {prod_name}\n\n"
        f"📂 دسته: {cat_name}\n"
        f"💰 قیمت: {format_price(product['price'])}\n"
        f"📦 نوع بسته: {product['unit']}\n\n"
        f"تعداد مورد نظر را انتخاب کنید:"
    )
    
    keyboard = [
        [
            {"text": "1️⃣", "callback_data": f"qty|1"},
            {"text": "2️⃣", "callback_data": f"qty|2"},
            {"text": "3️⃣", "callback_data": f"qty|3"},
        ],
        [
            {"text": "4️⃣", "callback_data": f"qty|4"},
            {"text": "5️⃣", "callback_data": f"qty|5"},
            {"text": "🔟", "callback_data": f"qty|10"},
        ],
        [{"text": "🔙 بازگشت", "callback_data": f"cat|{cat_index}"}],
    ]
    
    if message_id:
        return edit_message(chat_id, message_id, text, keyboard)
    return send_message(chat_id, text, keyboard)

def add_to_cart(chat_id, qty, message_id=None):
    state_data = get_state_data(chat_id)
    prod_name = state_data.get("prod_name")
    
    if not prod_name:
        return
    
    cart = get_cart(chat_id)
    cart[prod_name] = cart.get(prod_name, 0) + qty
    
    data = load_data()
    for cat_name, products in data["categories"].items():
        if prod_name in products:
            icon = get_cat_icon(data, cat_name)
            price = products[prod_name]["price"]
            total = price * qty
            text = (
                f"✅ به سبد خرید اضافه شد!\n\n"
                f"{icon} {prod_name}\n"
                f"📦 تعداد: {qty}\n"
                f"💰 قیمت: {format_price(total)}"
            )
            keyboard = [
                [{"text": "🛒 ادامه خرید", "callback_data": "browse"}],
                [{"text": "🛍 مشاهده سبد", "callback_data": "cart"}],
                [{"text": "🔙 منوی اصلی", "callback_data": "back_main"}],
            ]
            if message_id:
                return edit_message(chat_id, message_id, text, keyboard)
            return send_message(chat_id, text, keyboard)

def show_cart(chat_id, message_id=None):
    cart = get_cart(chat_id)
    
    if not cart:
        keyboard = [
            [{"text": "🛒 مشاهده محصولات", "callback_data": "browse"}],
            [{"text": "🔙 منوی اصلی", "callback_data": "back_main"}],
        ]
        text = "🛍 سبد خرید شما خالی است!"
        if message_id:
            return edit_message(chat_id, message_id, text, keyboard)
        return send_message(chat_id, text, keyboard)
    
    data = load_data()
    text = "🛍 سبد خرید شما:\n\n"
    total = 0
    
    for prod_name, qty in cart.items():
        for cat_name, products in data["categories"].items():
            if prod_name in products:
                icon = get_cat_icon(data, cat_name)
                price = products[prod_name]["price"]
                item_total = price * qty
                total += item_total
                text += f"{icon} {prod_name}\n   {qty} × {format_price(price)} = {format_price(item_total)}\n\n"
                break
    
    text += f"\n💰 جمع کل: {format_price(total)}"
    
    keyboard = [
        [{"text": "✅ تکمیل سفارش", "callback_data": "checkout"}],
        [{"text": "🗑 خالی کردن سبد", "callback_data": "clear_cart"}],
        [{"text": "🛒 ادامه خرید", "callback_data": "browse"}],
        [{"text": "🔙 منوی اصلی", "callback_data": "back_main"}],
    ]
    
    if len(text) > 3500:
        text = text[:3400] + "\n...(سبد بزرگ است)"
    
    if message_id:
        return edit_message(chat_id, message_id, text, keyboard)
    return send_message(chat_id, text, keyboard)

def start_checkout(chat_id, message_id=None):
    cart = get_cart(chat_id)
    if not cart:
        return show_cart(chat_id, message_id)
    
    set_state(chat_id, "checkout_name")
    text = "📝 تکمیل سفارش - مرحله ۱ از ۴\n\nلطفا نام و نام خانوادگی خود را وارد کنید:"
    if message_id:
        return edit_message(chat_id, message_id, text)
    return send_message(chat_id, text)

def show_contact(chat_id, message_id=None):
    data = load_data()
    contact = data.get("contact_info", {})
    text = (
        "📞 تماس با ما:\n\n"
        f"📱 تلفن: {contact.get('phone', '')}\n"
        f"🏪 آدرس: {contact.get('address', '')}\n"
        f"⏰ ساعت کاری: {contact.get('hours', '')}\n\n"
        "🌿 فروشگاه ادویه جات گهنیج"
    )
    keyboard = [[{"text": "🔙 بازگشت", "callback_data": "back_main"}]]
    if message_id:
        return edit_message(chat_id, message_id, text, keyboard)
    return send_message(chat_id, text, keyboard)

# ============ پنل مدیریت ============
def show_admin_panel(chat_id, message_id=None):
    if not is_admin(chat_id):
        return
    text = "⚙️ پنل مدیریت فروشگاه گهنیج\n\nیکی از گزینه ها را انتخاب کنید:"
    keyboard = [
        [{"text": "💰 ویرایش قیمت محصولات", "callback_data": "adm_prices"}],
        [{"text": "📦 مدیریت هزینه ارسال", "callback_data": "adm_ship"}],
        [{"text": "💳 مدیریت اطلاعات پرداخت", "callback_data": "adm_pay"}],
        [{"text": "📞 مدیریت اطلاعات تماس", "callback_data": "adm_contact"}],
        [{"text": "📋 لیست سفارشات", "callback_data": "adm_orders"}],
        [{"text": "🔙 بازگشت", "callback_data": "back_main"}],
    ]
    if message_id:
        return edit_message(chat_id, message_id, text, keyboard)
    return send_message(chat_id, text, keyboard)

def show_admin_orders(chat_id, message_id=None):
    data = load_data()
    orders = data.get("orders", [])
    
    if not orders:
        text = "📋 هیچ سفارشی ثبت نشده."
    else:
        text = "📋 آخرین سفارشات:\n\n"
        for order in orders[-10:]:
            items = ""
            for item, qty in order["items"].items():
                items += f"  • {item}: {qty}\n"
            text += (
                f"━━━━━━━━━━━━\n"
                f"# {order['order_id']}\n"
                f"👤 {order['customer_name']}\n"
                f"📱 {order['customer_phone']}\n"
                f"📍 {order['customer_address']}\n"
                f"🚚 {order['shipping_method']}\n"
                f"{items}"
                f"💵 {format_price(order['grand_total'])}\n\n"
            )
    
    keyboard = [[{"text": "🔙 پنل مدیریت", "callback_data": "admin"}]]
    if len(text) > 3500:
        text = text[:3400] + "\n...(زیاد است)"
    if message_id:
        return edit_message(chat_id, message_id, text, keyboard)
    return send_message(chat_id, text, keyboard)

# ============ پردازش کالبک ============
def handle_callback(callback):
    chat_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]
    data_str = callback["data"]
    callback_id = callback["id"]
    
    answer_callback(callback_id)
    
    if data_str == "back_main":
        clear_state(chat_id)
        show_main_menu(chat_id, callback.get("from", {}).get("first_name", "کاربر"))
    elif data_str == "browse":
        show_categories(chat_id, message_id)
    elif data_str == "cart":
        show_cart(chat_id, message_id)
    elif data_str == "clear_cart":
        user_carts[chat_id] = {}
        show_cart(chat_id, message_id)
    elif data_str == "checkout":
        start_checkout(chat_id, message_id)
    elif data_str == "contact":
        show_contact(chat_id, message_id)
    elif data_str == "admin":
        show_admin_panel(chat_id, message_id)
    elif data_str == "adm_orders":
        show_admin_orders(chat_id, message_id)
    elif data_str.startswith("cat|"):
        cat_index = int(data_str.split("|")[1])
        show_category_products(chat_id, cat_index, message_id)
    elif data_str.startswith("prod|"):
        parts = data_str.split("|")
        show_product(chat_id, int(parts[1]), int(parts[2]), message_id)
    elif data_str.startswith("qty|"):
        qty = int(data_str.split("|")[1])
        add_to_cart(chat_id, qty, message_id)
    elif data_str.startswith("ship|"):
        idx = int(data_str.split("|")[1])
        process_shipping(chat_id, idx, message_id)

# ============ پردازش پیام متنی ============
def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")
    user = message.get("from", {})
    user_name = user.get("first_name", "کاربر")
    
    if text == "/start":
        show_main_menu(chat_id, user_name)
        return
    
    state = get_state(chat_id)
    
    if state == "checkout_name":
        state_data = get_state_data(chat_id)
        state_data["name"] = text
        set_state(chat_id, "checkout_phone", state_data)
        send_message(chat_id, "📝 مرحله ۲ از ۴\n\nلطفا شماره تلفن خود را وارد کنید:")
    
    elif state == "checkout_phone":
        state_data = get_state_data(chat_id)
        state_data["phone"] = text
        set_state(chat_id, "checkout_address", state_data)
        send_message(chat_id, "📝 مرحله ۳ از ۴\n\nلطفا آدرس کامل خود را وارد کنید:")
    
    elif state == "checkout_address":
        state_data = get_state_data(chat_id)
        state_data["address"] = text
        
        data = load_data()
        shipping = data["shipping_options"]
        ship_list = list(shipping.keys())
        state_data["ship_list"] = ship_list
        set_state(chat_id, "checkout_shipping", state_data)
        
        msg = "📝 مرحله ۴ از ۴\n\n🚚 روش ارسال را انتخاب کنید:\n\n"
        keyboard = []
        for i, method in enumerate(ship_list):
            msg += f"▫️ {method}: {format_price(shipping[method])}\n"
            keyboard.append([{"text": f"🚚 {method} - {format_price(shipping[method])}", "callback_data": f"ship|{i}"}])
        send_message(chat_id, msg, keyboard)

def process_shipping(chat_id, ship_index, message_id):
    state_data = get_state_data(chat_id)
    ship_list = state_data.get("ship_list", [])
    
    if ship_index >= len(ship_list):
        return
    
    method = ship_list[ship_index]
    data = load_data()
    ship_cost = data["shipping_options"][method]
    
    cart = get_cart(chat_id)
    products_total = 0
    items_text = ""
    
    for prod_name, qty in cart.items():
        for cat_name, products in data["categories"].items():
            if prod_name in products:
                price = products[prod_name]["price"]
                item_total = price * qty
                products_total += item_total
                items_text += f"  ▫️ {prod_name}: {qty} = {format_price(item_total)}\n"
                break
    
    grand_total = products_total + ship_cost
    state_data["ship_method"] = method
    state_data["ship_cost"] = ship_cost
    state_data["grand_total"] = grand_total
    set_state(chat_id, "waiting_receipt", state_data)
    
    text = (
        f"🧾 خلاصه سفارش:\n\n"
        f"👤 نام: {state_data['name']}\n"
        f"📱 تلفن: {state_data['phone']}\n"
        f"📍 آدرس: {state_data['address']}\n"
        f"🚚 ارسال: {method}\n\n"
        f"📦 محصولات:\n{items_text}\n"
        f"💰 جمع محصولات: {format_price(products_total)}\n"
        f"🚚 هزینه ارسال: {format_price(ship_cost)}\n"
        f"━━━━━━━━━━━━\n"
        f"💵 مبلغ کل: {format_price(grand_total)}\n\n"
        f"━━━━━━━━━━━━\n"
        f"💳 شماره کارت:\n{data['card_number']}\n"
        f"به نام: {data['card_holder']}\n\n"
        f"لطفا مبلغ را واریز کنید و عکس رسید را ارسال کنید:"
    )
    
    if len(text) > 3500:
        text = text[:3400] + "\n..."
    
    edit_message(chat_id, message_id, text)

def handle_photo(message):
    chat_id = message["chat"]["id"]
    state = get_state(chat_id)
    
    if state != "waiting_receipt":
        return
    
    photo = message["photo"][-1]
    file_id = photo["file_id"]
    
    state_data = get_state_data(chat_id)
    cart = get_cart(chat_id)
    data = load_data()
    
    order = {
        "order_id": len(data["orders"]) + 1,
        "user_id": chat_id,
        "customer_name": state_data["name"],
        "customer_phone": state_data["phone"],
        "customer_address": state_data["address"],
        "shipping_method": state_data["ship_method"],
        "shipping_cost": state_data["ship_cost"],
        "items": dict(cart),
        "grand_total": state_data["grand_total"],
        "status": "در انتظار تایید"
    }
    
    data["orders"].append(order)
    save_data(data)
    
    send_message(chat_id, 
        f"✅ سفارش شما ثبت شد!\n\n"
        f"🔢 شماره سفارش: #{order['order_id']}\n"
        f"💵 مبلغ: {format_price(order['grand_total'])}\n\n"
        f"🙏 از خرید شما متشکریم!")
    
    # ارسال به مدیران
    items_text = ""
    for prod, qty in cart.items():
        items_text += f"  • {prod}: {qty}\n"
    
    admin_text = (
        f"🔔 سفارش جدید #{order['order_id']}\n\n"
        f"👤 {order['customer_name']}\n"
        f"📱 {order['customer_phone']}\n"
        f"📍 {order['customer_address']}\n"
        f"🚚 {order['shipping_method']}\n\n"
        f"📦:\n{items_text}\n"
        f"💵 {format_price(order['grand_total'])}"
    )
    
    for admin_id in data.get("admins", []):
        try:
            send_message(admin_id, admin_text)
            send_photo(admin_id, file_id, f"🧾 رسید #{order['order_id']}")
        except Exception as e:
            logger.error(f"Send to admin failed: {e}")
    
    user_carts[chat_id] = {}
    clear_state(chat_id)

# ============ Long Polling ============
def polling():
    logger.info("Bot polling started...")
    offset = 0
    while True:
        try:
            r = requests.get(f"{BALE_API}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=40)
            result = r.json()
            
            if result.get("ok"):
                for update in result.get("result", []):
                    offset = update["update_id"] + 1
                    
                    if "message" in update:
                        msg = update["message"]
                        if "photo" in msg:
                            handle_photo(msg)
                        elif "text" in msg:
                            handle_message(msg)
                    elif "callback_query" in update:
                        handle_callback(update["callback_query"])
        except Exception as e:
            logger.error(f"Polling error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Flask در thread جدا
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()
    logger.info(f"Flask started on port {PORT}")
    
    # شروع polling
    load_data()
    polling()
