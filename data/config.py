from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.int("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

UY_KANAL = env.int("UY_KANAL")  # Uy kanal id raqami
KVARTIRA_KANAL = env.int("KVARTIRA_KANAL")  # Kvartira kanal id raqami

UY_URL = env.str("UY_URL")  # Uy kanal url manzili
KVARTIRA_URL = env.str("KVARTIRA_URL")  # Kvartira kanal url manzili