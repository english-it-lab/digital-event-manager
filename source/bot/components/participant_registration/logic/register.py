from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str
from components.participant_registration.logic.states import RegisterStates

from database.db import (
    get_sections_by_event_id,
    get_faculties,
    get_courses,
    add_participant_to_db,
    get_teachers_with_people_data,
    get_textbook_levels
)

locale = load_locales(join(dirname(__file__), "..", "locale"))


def getstr(lang, prefix, path):
    return get_locale_str(locale, f"{lang}.{prefix}.{path}")


lang = "ru"
prefix_base = "participant_registration.user.register"
prefix_lst = "participant_registration.user.register.listener"
prefix_prt = "participant_registration.user.register.participant"
shared = "participant_registration.shared"


async def pr_cb_user_register(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text=getstr(lang, prefix_base, "listener.button"),
        callback_data="pr_cb_reg_lst_frm_section",
    )
    keyboard.button(
        text=getstr(lang, prefix_base, "participant.button"),
        callback_data="pr_cb_reg_prt_frm_section",
    )
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    keyboard.adjust(2, 1, 1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_base, "caption"), reply_markup=keyboard.as_markup()
    )


# Listener ---------------------------------------------------------------------


async def pr_cb_reg_lst_frm_section(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    sections = get_sections_by_event_id(data.get("event")["id"])

    keyboard = InlineKeyboardBuilder()

    for section in sections:
        keyboard.button(text=section["name"], callback_data="pr_cb_reg_lst_frm_faculty")

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "form.section"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_lst_frm_theme(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_lst_frm_faculty(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    faculties = get_faculties()

    for faculty in faculties:
        keyboard.button(text=faculty["name"], callback_data="pr_cb_reg_lst_frm_course")

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "form.faculty"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_lst_frm_course(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    courses = get_courses()

    for course in courses:
        keyboard.button(text=str(course["year"]), callback_data="pr_cb_reg_lst_frm_add_to_db")

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "form.course"), reply_markup=keyboard.as_markup()
    )

async def pr_cb_reg_lst_frm_add_to_db(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    success = add_participant_to_db(person_id=1, faculty_id=1, course_id=1,
                                    section_id=1, is_poster_participant=False,
                                    teacher_id=1,
                                    is_translators_participate=False,
                                    has_translator_education=False,
                                    textbook_level_id=1,
                                    is_group_leader=False,
                                    presentation_topic="Listen",
                                    is_notification_allowed=False,
                                    password="12345")

async def pr_cb_reg_lst_frm_on_success(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_lst_frm_on_failure(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup()
    )


# Participant ------------------------------------------------------------------


async def pr_cb_reg_prt_frm_section(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    lang = data.get("lang", "ru")

    sections = get_sections_by_event_id(data.get("event")["id"])

    keyboard = InlineKeyboardBuilder()

    for section in sections:
        keyboard.button(text=section["name"],
                        callback_data="pr_cb_reg_prt_frm_faculty section_id " + str(section["id"]))

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.section"), reply_markup=keyboard.as_markup()
    )

async def pr_cb_reg_prt_frm_faculty(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    faculties = get_faculties()

    for faculty in faculties:
        keyboard.button(text=faculty["name"],
                        callback_data="pr_cb_reg_prt_frm_course faculty_id " + str(faculty["id"]))

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.faculty"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_prt_frm_course(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    courses = get_courses()

    for course in courses:
        keyboard.button(text=str(course["year"]),
                        callback_data="pr_cb_reg_prt_frm_advisor course_id " + str(course["id"]))

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.course"), reply_markup=keyboard.as_markup()
    )

async def pr_cb_reg_prt_frm_add_to_db(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    success = add_participant_to_db(person_id=1, faculty_id=1, course_id=1,
                                    section_id=1, is_poster_participant=False,
                                    teacher_id=1,
                                    is_translators_participate=False,
                                    has_translator_education=False,
                                    textbook_level_id=1,
                                    is_group_leader=False,
                                    presentation_topic="Listen",
                                    is_notification_allowed=False,
                                    password="12345")

async def pr_cb_reg_prt_frm_advisor(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    teachers = get_teachers_with_people_data()

    for teacher in teachers:
        keyboard.button(text=teacher["last_name"] + ' ' + teacher["first_name"] + ' ' 
                        + teacher["middle_name"],
                        callback_data="pr_cb_reg_prt_frm_english_level teacher_id "
                        + str(teacher["id"]))

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.advisor"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_prt_frm_english_level(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    textbook_levels = get_textbook_levels()

    for textbook_level in textbook_levels:
        keyboard.button(text=textbook_level["level_abbreviation"],
                        callback_data="pr_cb_reg_prt_frm_translator textbook_level_id "
                        + str(textbook_level["id"]))

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.english_level"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_prt_frm_translator(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=getstr(lang, shared, "_yes"), 
                    callback_data="pr_cb_reg_prt_frm_translator_education translator 1")
    keyboard.button(text=getstr(lang, shared, "_no"), 
                    callback_data="pr_cb_reg_prt_frm_translator_education translator 0")

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.translator"), reply_markup=keyboard.as_markup()
    )

async def pr_cb_reg_prt_frm_translator_education(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=getstr(lang, shared, "_yes"), 
                    callback_data="pr_cb_reg_prt_frm_theme has_translator_education 1")
    keyboard.button(text=getstr(lang, shared, "_no"), 
                    callback_data="pr_cb_reg_prt_frm_theme has_translator_education 0")

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.has_translator_education"), reply_markup=keyboard.as_markup()
    )

async def pr_cb_reg_prt_frm_theme(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
    keyboard.adjust(1)

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "form.theme"), reply_markup=keyboard.as_markup()
    )
    await state.set_state(RegisterStates.theme)

async def pr_cb_handle_theme_input(message: types.Message, state: FSMContext):
    print("----------------------------------- theme", message.text)
    await state.update_data(theme=message.text.strip())

    data = await state.get_data()
    lang = data.get("lang", "ru")

    success = add_participant_to_db(person_id=1,
                                    faculty_id=data.get("faculty_id"), 
                                    course_id=data.get("course_id"),
                                    section_id=data.get("section_id"),
                                    is_poster_participant=True,
                                    teacher_id=data.get("teacher_id"),
                                    is_translators_participate=data.get("translator"),
                                    has_translator_education=data.get("has_translator_education"),
                                    textbook_level_id=data.get("textbook_level_id"),
                                    is_group_leader=False,
                                    presentation_topic=data.get("theme"),
                                    is_notification_allowed=False,
                                    password="12345")
    print("---------------------------------------- success", success)
    await state.clear()


async def pr_cb_reg_prt_frm_on_success(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "section"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_prt_frm_on_failure(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_prt, "section"), reply_markup=keyboard.as_markup()
    )


# Group member -----------------------------------------------------------------
async def pr_cb_reg_gm_frm_section(
    callback_query: types.CallbackQuery, bot: Bot
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_gm_frm_theme(callback_query: types.CallbackQuery, bot: Bot) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_gm_frm_amount(
    callback_query: types.CallbackQuery, bot: Bot
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")


async def pr_cb_reg_gm_frm_on_success(
    callback_query: types.CallbackQuery, bot: Bot
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup()
    )


async def pr_cb_reg_gm_frm_on_failure(
    callback_query: types.CallbackQuery, bot: Bot
) -> None:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

    await callback_query.message.edit_text(
        getstr(lang, prefix_lst, "section"), reply_markup=keyboard.as_markup()
    )
