from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str

from database.db import get_events

locale = load_locales(join(dirname(__file__), "..", "locale"))


def getstr(lang, prefix, path):
    return get_locale_str(locale, f"{lang}.{prefix}.{path}")

async def pr_cb_user_browse(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    event_index = data.get("event_index", 0)
    lang = data.get("lang", "ru")

    prefix = "participant_registration.user.browse"
    shared = "participant_registration.shared"

    events = get_events()
    
    keyboard = InlineKeyboardBuilder()

    if len(events) > 0:
        event_index = event_index % len(events)
        keyboard.button(text=getstr(lang, shared, "left"), callback_data="pr_cb_browse_prev_event")
        keyboard.button(text=getstr(lang, shared, "right"), callback_data="pr_cb_browse_next_event")

        await state.update_data(event=events[event_index])

        keyboard.button(
            text=getstr(lang, prefix, "register"), callback_data="pr_cb_user_register"
        )
        keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")

        keyboard.adjust(2, 1, 1)

        await callback_query.message.edit_text(
            events[event_index]['name'], reply_markup=keyboard.as_markup()
        )
    else:
        keyboard.button(text=getstr(lang, shared, "exit"), callback_data="pr_cb_main")
        await callback_query.message.edit_text(
            "Мероприятий нет", reply_markup=keyboard.as_markup()
        )

async def pr_cb_browse_next_event(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    event_index = data.get("event_index", 0)
    event_index += 1
    await state.update_data(event_index=event_index)
    await pr_cb_user_browse(callback_query, bot, state)

async def pr_cb_browse_prev_event(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    data = await state.get_data()
    event_index = data.get("event_index", 0)
    event_index -= 1
    await state.update_data(event_index=event_index)
    await pr_cb_user_browse(callback_query, bot, state)