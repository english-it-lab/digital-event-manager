0. создать такой .env на уровне с .env.sample (по дефолту сделано):

TG_BOT_TOKEN=8218829806:AAHhB_UJ9_vL2BaXSoW0QAd_JKlfkckG0NU
TG_BOT_EMAIL=123
TG_BOT_EMAIL_PASSWORD=123
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=123

DB_HOST=89.191.229.210
DB_PORT=5432
DB_NAME=digital_event_manager
DB_USER=digital_event_manager_user
DB_PASS=e<xStirRQI&9|e

1. make setup (из папки source)
2. make init
2.1. чтобы заполнить бд: uv run source/bot/components/reports_evaluation/fill_db.py (из корня)
3. скопировать бд source\bot\database\instance\digital_event_manager.db в source\bot\
4. make run (из source)

код доступа - 1111