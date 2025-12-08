import sqlite3
import os

# Имя базы данных
db_file = os.path.join("source","bot", "database", "instance", "digital_event_manager.db") 
sql_file = os.path.join("source","bot", "components", "reports_evaluation", "query.sql") 

if not os.path.exists(db_file):
    print(f"❌ Ошибка: Файл БД '{db_file}' не найден! Сначала сделай make init.")
    exit(1)

if not os.path.exists(sql_file):
    print(f"❌ Ошибка: Файл '{sql_file}' не найден!")
    exit(1)

# Читаем SQL
with open(sql_file, "r", encoding="utf-8") as f:
    sql_script = f.read()

try:
    print(f"🔌 Подключение к {db_file}...")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    print("🚀 Выполняем SQL скрипт...")
    cursor.executescript(sql_script)
    conn.commit()
    
    print("✅ Данные успешно добавлены!")
    print("🔑 Код доступа: 1111")
    print("ℹ️  Секция: Backend Development")
    print("ℹ️  Жюри: Председатель (Иван) и Петров")
    
except sqlite3.Error as e:
    print(f"❌ Ошибка SQLite: {e}")
finally:
    if conn:
        conn.close()