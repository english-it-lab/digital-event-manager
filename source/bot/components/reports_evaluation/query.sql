-- Включаем поддержку внешних ключей
PRAGMA foreign_keys = ON;

-- 1. Справочники
INSERT OR IGNORE INTO universities (name) VALUES ('МГУ');
INSERT OR IGNORE INTO departments (name) VALUES ('Кафедра АСВК');
INSERT OR IGNORE INTO courses (year) VALUES (1);
INSERT OR IGNORE INTO textbook_levels (level_abbreviation) VALUES ('B2');

-- Факультет
INSERT INTO faculties (university_id, name) 
SELECT id, 'ВМК' FROM universities 
WHERE name = 'МГУ' 
  AND NOT EXISTS (SELECT 1 FROM faculties WHERE name = 'ВМК');

-- 2. Секция
INSERT INTO sections (name, lecture_hall, time) 
SELECT 'Backend Development', '404', '2025-05-20 10:00:00+00'
WHERE NOT EXISTS (SELECT 1 FROM sections WHERE name = 'Backend Development');

-- 3. Люди: ПРЕДСЕДАТЕЛЬ (Иван)
INSERT OR IGNORE INTO people (first_name, last_name, middle_name, phone, email, tg_name)
VALUES ('Иван', 'Председатель', 'Иванович', '89990000001', 'chair@test.com', '@chairman_ivan');

-- Жюри: Председатель (Код 1111)
INSERT INTO juries (university_id, person_id, is_chairman, access_key)
SELECT 
    (SELECT id FROM universities WHERE name = 'МГУ'),
    (SELECT id FROM people WHERE email = 'chair@test.com'),
    1, 
    1111
WHERE NOT EXISTS (SELECT 1 FROM juries WHERE access_key = 1111 AND is_chairman = 1);

-- 4. Люди: ОБЫЧНЫЙ ЧЛЕН ЖЮРИ (Петр)
INSERT OR IGNORE INTO people (first_name, last_name, middle_name, phone, email, tg_name)
VALUES ('Петр', 'Петров', 'Петрович', '89990000002', 'petr@test.com', '@jury_petr');

-- Жюри: Петров (Код 1111)
INSERT INTO juries (university_id, person_id, is_chairman, access_key)
SELECT 
    (SELECT id FROM universities WHERE name = 'МГУ'),
    (SELECT id FROM people WHERE email = 'petr@test.com'),
    0, 
    1111
WHERE NOT EXISTS (SELECT 1 FROM juries WHERE access_key = 1111 AND is_chairman = 0);

-- 5. Привязка Жюри к Секции
INSERT INTO section_juries (section_id, jury_id)
SELECT s.id, j.id
FROM sections s, juries j
JOIN people p ON j.person_id = p.id
WHERE s.name = 'Backend Development' 
  AND p.email IN ('chair@test.com', 'petr@test.com')
  AND NOT EXISTS (SELECT 1 FROM section_juries WHERE section_id = s.id AND jury_id = j.id);

-- 6. Преподаватель
INSERT OR IGNORE INTO people (first_name, last_name, phone, email, tg_name)
VALUES ('Сергей', 'Преподаватель', '89990000003', 'teach@test.com', '@teacher_sergey');

INSERT INTO teachers (university_id, department_id, person_id)
SELECT 
    (SELECT id FROM universities WHERE name = 'МГУ'),
    (SELECT id FROM departments WHERE name = 'Кафедра АСВК'),
    (SELECT id FROM people WHERE email = 'teach@test.com')
WHERE NOT EXISTS (SELECT 1 FROM teachers WHERE person_id = (SELECT id FROM people WHERE email = 'teach@test.com'));

-- 7. УЧАСТНИКИ (Студенты)
-- Студент 1
INSERT OR IGNORE INTO people (first_name, last_name, phone, email, tg_name)
VALUES ('Алексей', 'Смирнов', '89990000010', 'smirnov@stud.com', '@smirnov_alex');

-- ! ВАЖНО: Ниже добавлено t.id вместо просто id, чтобы не было ошибки ambiguous column !
INSERT INTO participants (
    faculty_id, course_id, teacher_id, section_id, person_id,
    is_poster_participant, is_translators_participate, has_translator_education,
    textbook_level_id, is_group_leader, presentation_topic, 
    is_notification_allowed, password
) 
SELECT
    (SELECT id FROM faculties WHERE name = 'ВМК'),
    (SELECT id FROM courses WHERE year = 1),
    (SELECT t.id FROM teachers t JOIN people p ON t.person_id = p.id WHERE p.email = 'teach@test.com'),
    (SELECT id FROM sections WHERE name = 'Backend Development'),
    (SELECT id FROM people WHERE email = 'smirnov@stud.com'),
    0, 0, 0, 
    (SELECT id FROM textbook_levels WHERE level_abbreviation = 'B2'),
    0, 'Архитектура Telegram ботов', 1, 'hash123'
WHERE NOT EXISTS (SELECT 1 FROM participants WHERE person_id = (SELECT id FROM people WHERE email = 'smirnov@stud.com'));

-- Студент 2
INSERT OR IGNORE INTO people (first_name, last_name, phone, email, tg_name)
VALUES ('Мария', 'Сидорова', '89990000011', 'sidorova@stud.com', '@sidorova_mash');

-- ! ВАЖНО: Тут тоже t.id !
INSERT INTO participants (
    faculty_id, course_id, teacher_id, section_id, person_id,
    is_poster_participant, is_translators_participate, has_translator_education,
    textbook_level_id, is_group_leader, presentation_topic, 
    is_notification_allowed, password
) 
SELECT
    (SELECT id FROM faculties WHERE name = 'ВМК'),
    (SELECT id FROM courses WHERE year = 1),
    (SELECT t.id FROM teachers t JOIN people p ON t.person_id = p.id WHERE p.email = 'teach@test.com'),
    (SELECT id FROM sections WHERE name = 'Backend Development'),
    (SELECT id FROM people WHERE email = 'sidorova@stud.com'),
    0, 0, 0,
    (SELECT id FROM textbook_levels WHERE level_abbreviation = 'B2'),
    0, 'Data Science в Python', 1, 'hash456'
WHERE NOT EXISTS (SELECT 1 FROM participants WHERE person_id = (SELECT id FROM people WHERE email = 'sidorova@stud.com'));