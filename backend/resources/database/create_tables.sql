CREATE TABLE universities (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL
);

CREATE TABLE faculties (
    id serial PRIMARY KEY,
    university_id integer REFERENCES universities(id) ON DELETE SET NULL,
    name varchar(255) NOT NULL
);

CREATE TABLE departments (
    id serial PRIMARY KEY,
    name varchar(200) NOT NULL
);

CREATE TABLE people (
    id serial PRIMARY KEY,
    first_name varchar(100),
    last_name varchar(100),
    middle_name varchar(100),
    email varchar(255),
    title varchar(20),        
    degree varchar(20), 
    position varchar(50),
    workplace varchar(50),
    tg_name varchar(32)
);

CREATE TABLE organizers (
    id serial PRIMARY KEY,
    person_id integer REFERENCES people(id) ON DELETE SET NULL,
    contact_number varchar(15),
    access_key bigint
);

CREATE TABLE venues (
    id serial PRIMARY KEY,
    city varchar(100),
    street varchar(100),
    building varchar(10)
);

CREATE TABLE events (
    id serial PRIMARY KEY,
    venue_id integer REFERENCES venues(id) ON DELETE SET NULL,
    organizer_id integer REFERENCES organizers(id) ON DELETE SET NULL,
    name varchar(255),
    type varchar(100),
    event_date date
);

CREATE TABLE courses (
    id serial PRIMARY KEY,
    year integer
);

CREATE TABLE textbook_levels (
    id serial PRIMARY KEY,
    level_abbreviation varchar(3)
);

CREATE TABLE sections (
    id serial PRIMARY KEY,
    name varchar(100) NOT NULL,
    lecture_hall varchar(7),
    time timestamptz
);

CREATE TABLE event_sections (
    id serial PRIMARY KEY,
    event_id integer REFERENCES events(id) ON DELETE CASCADE,
    section_id integer REFERENCES sections(id) ON DELETE CASCADE
);

CREATE TABLE topics (
    id serial PRIMARY KEY,
    section_id integer REFERENCES sections(id) ON DELETE SET NULL,
    name varchar(50)
);

CREATE TABLE groups (
    id serial PRIMARY KEY,
    section_id integer REFERENCES sections(id) ON DELETE SET NULL,
    name varchar(100),
    member_count integer,
    registration_time timestamptz
);

CREATE TABLE group_topics (
    id serial PRIMARY KEY,
    group_id integer REFERENCES groups(id) ON DELETE CASCADE,
    topic_id integer REFERENCES topics(id) ON DELETE SET NULL
);

CREATE TABLE teachers (
    id serial PRIMARY KEY,
    university_id integer REFERENCES universities(id) ON DELETE SET NULL,
    department_id integer REFERENCES departments(id) ON DELETE SET NULL,
    person_id integer REFERENCES people(id) ON DELETE SET NULL
);

CREATE TABLE participants (
    id serial PRIMARY KEY, 
    person_id integer REFERENCES people(id) ON DELETE SET NULL,
    faculty_id integer REFERENCES faculties(id) ON DELETE SET NULL,
    course_id integer REFERENCES courses(id) ON DELETE SET NULL,
    teacher_id integer REFERENCES teachers(id) ON DELETE SET NULL, 
    section_id integer REFERENCES sections(id) ON DELETE SET NULL,
    is_poster_participant boolean DEFAULT FALSE,
    is_translator_participant boolean DEFAULT FALSE,
    has_translator_education boolean DEFAULT FALSE,
    textbook_level_id integer REFERENCES textbook_levels(id) ON DELETE SET NULL,
    is_group_leader boolean DEFAULT FALSE,
    presentation_topic varchar(255),
    is_notification_allowed boolean DEFAULT TRUE,
    password_hash varchar(255)
);

CREATE TABLE group_participants (
    id serial PRIMARY KEY,
    group_id integer REFERENCES groups(id) ON DELETE CASCADE,
    participant_id integer REFERENCES participants(id) ON DELETE CASCADE,
    UNIQUE (group_id, participant_id)
);

CREATE TABLE juries (
    id serial PRIMARY KEY,
    university_id integer REFERENCES universities(id) ON DELETE SET NULL,
    person_id integer REFERENCES people(id) ON DELETE SET NULL,
    is_chairman boolean DEFAULT FALSE,
    access_key bigint
);

CREATE TABLE section_juries (
    id serial PRIMARY KEY,
    section_id integer REFERENCES sections(id) ON DELETE CASCADE,
    jury_id integer REFERENCES juries(id) ON DELETE CASCADE,
    UNIQUE (section_id, jury_id)
);

CREATE TABLE jury_scores (
    id serial PRIMARY KEY,
    jury_id integer REFERENCES juries(id) ON DELETE SET NULL,
    participant_id integer REFERENCES participants(id) ON DELETE SET NULL,
    organization_score double precision,
    content double precision,
    visuals double precision,
    mechanics double precision,
    delivery double precision,
    comment varchar(100)
);

CREATE TABLE jury_scores_changes (
    id serial PRIMARY KEY,
    jury_scores_id integer REFERENCES jury_scores(id) ON DELETE CASCADE,
    jury_id integer REFERENCES juries(id) ON DELETE SET NULL,
    update_time timestamptz DEFAULT now()
);

CREATE TABLE organizer_section_changes (
    id serial PRIMARY KEY,
    section_id integer REFERENCES sections(id) ON DELETE CASCADE,
    organizer_id integer REFERENCES organizers(id) ON DELETE SET NULL,
    update_time timestamptz DEFAULT now()
);

CREATE TABLE organizer_participant_changes (
    id serial PRIMARY KEY,
    participant_id integer REFERENCES participants(id) ON DELETE CASCADE,
    organizer_id integer REFERENCES organizers(id) ON DELETE SET NULL,
    update_time timestamptz DEFAULT now()
);

CREATE TABLE technical_requirements (
    id serial PRIMARY KEY,
    topic_id integer REFERENCES topics(id) ON DELETE SET NULL,
    format varchar(10),
    sizes varchar(2)
);

CREATE TABLE posters_content (
    id serial PRIMARY KEY,
    technical_requirements_id integer REFERENCES technical_requirements(id) ON DELETE SET NULL,
    words_amount integer,
    images_amount integer
);



