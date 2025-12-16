import sqlite3
from database.init_db import DB_PATH


def add_user_to_db(
    first_name,
    last_name,
    middle_name,
    phone,
    email,
    tg_name,
    title=None,
    degree=None,
    position=None,
    workplace=None,
):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO people (first_name, last_name, middle_name, phone, email,
                                title, degree, position, workplace, tg_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                first_name,
                last_name,
                middle_name,
                phone,
                email,
                title,
                degree,
                position,
                workplace,
                tg_name,
            ),
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
        return False

    finally:
        conn.close()


def update_user_db(
    first_name,
    last_name,
    middle_name,
    phone,
    email,
    tg_name,
    title=None,
    degree=None,
    position=None,
    workplace=None,
):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE people
            SET first_name  = ?,
                last_name   = ?,
                middle_name = ?,
                phone       = ?,
                email       = ?,
                title       = ?,
                degree      = ?,
                position    = ?,
                workplace   = ?
            WHERE tg_name = ?
            """,
            (
                first_name,
                last_name,
                middle_name,
                phone,
                email,
                title,
                degree,
                position,
                workplace,
                tg_name,
            ),
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
        return False

    finally:
        conn.close()


def get_user_by_tg_name(tg_name: str) -> dict | None:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM people WHERE tg_name = ?", (tg_name,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        else:
            return None

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()


def get_user_by_email(email: str) -> dict | None:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM people WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            return dict(row)
        else:
            return None

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()


def register_user_from_state(data: dict, tg_name: str) -> bool:
    fio_parts = data.get("fio", "").split()

    if len(fio_parts) == 1:
        last_name = fio_parts[0]
        first_name = ""
        middle_name = ""
    elif len(fio_parts) == 2:
        last_name, first_name = fio_parts
        middle_name = ""
    else:
        last_name, first_name, *rest = fio_parts
        middle_name = " ".join(rest) if rest else None

    return add_user_to_db(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        phone=data.get("phone"),
        email=data.get("email"),
        tg_name=tg_name,
        title=None,
        degree=None,
        position=None,
        workplace=None,
    )


def update_user_from_state(data: dict, tg_name: str) -> bool:
    fio_parts = data.get("fio", "").split()

    if len(fio_parts) == 1:
        last_name = fio_parts[0]
        first_name = ""
        middle_name = ""
    elif len(fio_parts) == 2:
        last_name, first_name = fio_parts
        middle_name = ""
    else:
        last_name, first_name, *rest = fio_parts
        middle_name = " ".join(rest) if rest else None

    return update_user_db(
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        phone=data.get("phone"),
        email=data.get("email"),
        tg_name=tg_name,
        title=None,
        degree=None,
        position=None,
        workplace=None,
    )

def add_participant_to_db(
    person_id,
    faculty_id,
    course_id,
    section_id,
    is_poster_participant,
    teacher_id=None,
    is_translators_participate=None,
    has_translator_education=None,
    textbook_level_id=None,
    is_group_leader=None,
    presentation_topic=None,
    is_notification_allowed=None,
    password=None
):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO participants (person_id, faculty_id, course_id, section_id,
                is_poster_participant, teacher_id, is_translators_participate,
                has_translator_education, textbook_level_id, is_group_leader,
                presentation_topic, is_notification_allowed, password)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                person_id,
                faculty_id,
                course_id, 
                section_id,
                is_poster_participant, 
                teacher_id, 
                is_translators_participate,
                has_translator_education,
                textbook_level_id,
                is_group_leader,
                presentation_topic, 
                is_notification_allowed, 
                password
            ),
        )

        conn.commit()
        return True

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e}")
        return False

    finally:
        conn.close()

def get_events() -> list[dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM events")
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()

def get_sections_by_event_id(event_id: int) -> list[dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM event_sections AS es LEFT JOIN sections AS s " \
        "ON es.section_id = s.id " \
        "WHERE es.event_id = ?", (event_id,))
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()

def get_faculties() -> list[dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM faculties")
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()

def get_courses() -> list[dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM courses")
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()

def get_teachers_with_people_data() -> list[dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM teachers AS T LEFT JOIN people AS P " \
        "ON T.person_id = P.id ")
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

def get_textbook_levels() -> list[dict]:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM textbook_levels")
        return cursor.fetchall()

    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return None

    finally:
        conn.close()