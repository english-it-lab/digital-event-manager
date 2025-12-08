import time  # <--- ДОБАВИЛ ЭТОТ ИМПОРТ
from components.shared.db import Database

# --- Функции авторизации ---

async def is_user_authorized(db: Database, tg_id: int):
    """Проверяет, привязан ли этот TG ID к какому-либо члену жюри."""
    query = """
        SELECT j.id, p.first_name, p.last_name 
        FROM juries j
        JOIN people p ON j.person_id = p.id
        WHERE p.tg_name = ?
    """
    cursor = db.conn.execute(query, (str(tg_id),))
    return cursor.fetchone()

async def get_juries_by_code(db: Database, access_code: str):
    """Ищет членов жюри по коду доступа."""
    try:
        code_int = int(access_code)
    except ValueError:
        return []

    query = """
        SELECT j.id, p.first_name, p.last_name, p.middle_name
        FROM juries j
        JOIN people p ON j.person_id = p.id
        WHERE j.access_key = ?
    """
    cursor = db.conn.execute(query, (code_int,))
    return cursor.fetchall()

async def link_user_to_jury(db: Database, jury_id: int, tg_id: int):
    """Привязывает TG ID к записи человека."""
    cursor = db.conn.execute("SELECT person_id FROM juries WHERE id = ?", (jury_id,))
    row = cursor.fetchone()
    if not row:
        return False
    
    person_id = row[0]
    
    db.conn.execute(
        "UPDATE people SET tg_name = ? WHERE id = ?", 
        (str(tg_id), person_id)
    )
    db.conn.commit()
    return True

# --- Новые функции для меню ---

async def get_jury_info(db: Database, tg_id: int):
    """Возвращает полную инфу о члене жюри по TG ID (включая is_chairman)."""
    query = """
        SELECT j.id, p.first_name, p.last_name, j.is_chairman
        FROM juries j
        JOIN people p ON j.person_id = p.id
        WHERE p.tg_name = ?
    """
    cursor = db.conn.execute(query, (str(tg_id),))
    return cursor.fetchone()

async def get_participants_for_jury(db: Database, jury_id: int):
    """
    Возвращает список участников, привязанных к той же секции, что и член жюри.
    """
    query = """
        SELECT p.id, pp.first_name, pp.last_name, p.presentation_topic
        FROM participants p
        JOIN people pp ON p.person_id = pp.id
        JOIN section_juries sj ON p.section_id = sj.section_id
        WHERE sj.jury_id = ?
    """
    cursor = db.conn.execute(query, (jury_id,))
    return cursor.fetchall()

async def get_leaderboard(db: Database, jury_id: int):
    """
    Считает сумму баллов для каждого участника секции.
    """
    query = """
        SELECT 
            pp.last_name, 
            pp.first_name,
            SUM(
                COALESCE(js.organization_criteria, 0) + 
                COALESCE(js.content_criteria, 0) + 
                COALESCE(js.visuals_criteria, 0) + 
                COALESCE(js.mechanics_criteria, 0) + 
                COALESCE(js.delivery_criteria, 0)
            ) as total_score
        FROM participants p
        JOIN people pp ON p.person_id = pp.id
        JOIN section_juries sj ON p.section_id = sj.section_id
        LEFT JOIN jury_scores js ON p.id = js.participant_id
        WHERE sj.jury_id = ?
        GROUP BY p.id
        ORDER BY total_score DESC, pp.last_name ASC
    """
    cursor = db.conn.execute(query, (jury_id,))
    return cursor.fetchall()

async def save_score(db: Database, jury_id: int, participant_id: int, scores: dict, comment: str):
    """Сохраняет оценку в БД."""
    try:
        check_query = "SELECT id FROM jury_scores WHERE jury_id = ? AND participant_id = ?"
        cursor = db.conn.execute(check_query, (jury_id, participant_id))
        existing = cursor.fetchone()
        
        if existing:
            update_query = """
                UPDATE jury_scores 
                SET organization_criteria=?, content_criteria=?, visuals_criteria=?, 
                    mechanics_criteria=?, delivery_criteria=?, comment=?
                WHERE id=?
            """
            db.conn.execute(update_query, (
                scores['c1'], scores['c2'], scores['c3'], scores['c4'], scores['c5'], 
                comment, existing[0]
            ))
        else:
            insert_query = """
                INSERT INTO jury_scores 
                (jury_id, participant_id, organization_criteria, content_criteria, visuals_criteria, mechanics_criteria, delivery_criteria, comment)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            db.conn.execute(insert_query, (
                jury_id, participant_id, 
                scores['c1'], scores['c2'], scores['c3'], scores['c4'], scores['c5'], 
                comment
            ))
            
        db.conn.commit()
        return True
    except Exception as e:
        print(f"Save error: {e}")
        return False

# --- ВЫХОД (LOGOUT) ---

async def logout_user(db: Database, tg_id: int):
    """
    Отвязывает TG ID.
    Добавляем timestamp, чтобы имя 'released_ID_TIMESTAMP' было всегда уникальным.
    """
    # Теперь имя будет: released_12345_17300055
    new_fake_name = f"released_{tg_id}_{int(time.time())}"
    
    query = "UPDATE people SET tg_name = ? WHERE tg_name = ?"
    db.conn.execute(query, (new_fake_name, str(tg_id)))
    db.conn.commit()