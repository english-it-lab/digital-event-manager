from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from components.participant_registration.logic.states import RegisterStates
from components.participant_registration.logic.main import pr_cb_main
from components.participant_registration.logic.browse import (
    pr_cb_user_browse,
)
from components.participant_registration.logic.register import (
    pr_cb_user_register,
    pr_cb_reg_lst_frm_section,
    pr_cb_reg_lst_frm_theme,
    pr_cb_reg_lst_frm_faculty,
    pr_cb_reg_lst_frm_course,
    pr_cb_reg_lst_frm_add_to_db,
    pr_cb_reg_prt_frm_section,
    pr_cb_reg_prt_frm_theme,
    pr_cb_reg_prt_frm_faculty,
    pr_cb_reg_prt_frm_course,
    pr_cb_reg_prt_frm_add_to_db,
    pr_cb_reg_prt_frm_advisor,
    pr_cb_reg_prt_frm_english_level,
    pr_cb_reg_prt_frm_translator,
    pr_cb_reg_prt_frm_translator_education,
    pr_cb_handle_theme_input
)

from components.participant_registration.logic.my_data import (
    pr_cb_user_my_data,
    pr_cb_add_user_fio,
    pr_cb_add_user_phone,
    pr_cb_handle_fio_input,
    pr_cb_handle_email_input,
    pr_cb_handle_verification_code,
    pr_cb_handle_phone_input,
    pr_cb_change_user_fio,
)

from components.participant_registration.logic.browse import (
    pr_cb_browse_next_event,
    pr_cb_browse_prev_event
)

router = Router()


@router.callback_query(lambda c: c.data == "pr_cb_main")
async def callback_user_main_menu(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_main(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "pr_cb_user_browse")
async def callback_user_events_browse(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_user_browse(callback_query, bot, state)


# ---------------------------- My_data routers -----------------------------------------


@router.callback_query(lambda c: c.data == "pr_cb_user_my_data")
async def callback_user_my_data(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_user_my_data(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "pr_cb_add_user_fio")
async def callback_add_user_fio(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_add_user_fio(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "pr_cb_add_user_phone")
async def callback_add_user_phone(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_add_user_phone(callback_query, bot, state)


@router.callback_query(lambda c: c.data == "pr_cb_change_user_fio")
async def callback_change_user_fio(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data(change=True)
    await pr_cb_change_user_fio(callback_query, bot, state)


@router.message(RegisterStates.fio)
async def msg_fio(message: types.Message, state: FSMContext):
    await pr_cb_handle_fio_input(message, state)


@router.message(RegisterStates.phone)
async def msg_phone(message: types.Message, state: FSMContext):
    await pr_cb_handle_phone_input(message, state)


@router.message(RegisterStates.email)
async def msg_email(message: types.Message, state: FSMContext):
    await pr_cb_handle_email_input(message, state)


@router.message(RegisterStates.waiting_for_verification_code)
async def msg_waiting_for_verification_code(message: types.Message, state: FSMContext):
    await pr_cb_handle_verification_code(message, state)


# ---------------------------- Registration routers -----------------------------------------


@router.callback_query(lambda c: c.data == "pr_cb_user_register")
async def callback_user_register(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_user_register(callback_query, bot, state)


# Listener ---------------------------------------------------------------------
@router.callback_query(lambda c: c.data == "pr_cb_reg_lst_frm_section")
async def callback_reg_listener_section(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_lst_frm_section(callback_query, bot, state)

@router.callback_query(lambda c: c.data == "pr_cb_reg_lst_frm_theme")
async def callback_reg_listener_theme(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_lst_frm_theme(callback_query, bot, state)

@router.callback_query(lambda c: c.data == "pr_cb_reg_lst_frm_faculty")
async def callback_reg_listener_faculty(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_lst_frm_faculty(callback_query, bot, state)

@router.callback_query(lambda c: c.data == "pr_cb_reg_lst_frm_course")
async def callback_reg_listener_course(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_lst_frm_course(callback_query, bot, state)

@router.callback_query(lambda c: c.data == "pr_cb_reg_lst_frm_add_to_db")
async def callback_reg_listener_add_to_db(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_lst_frm_add_to_db(callback_query, bot, state)

# Participant ---------------------------------------------------------------------
@router.callback_query(lambda c: c.data == "pr_cb_reg_prt_frm_section")
async def callback_reg_participant_section(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_prt_frm_section(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_faculty")
async def callback_reg_participant_faculty(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data({callback_query.data.split()[1]: callback_query.data.split()[2]})
    print("--------------------------------------- ", callback_query.data.split()[1], callback_query.data.split()[2])
    await pr_cb_reg_prt_frm_faculty(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_course")
async def callback_reg_participant_course(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data({callback_query.data.split()[1]: callback_query.data.split()[2]})
    print("--------------------------------------- ", callback_query.data.split()[1], callback_query.data.split()[2])
    await pr_cb_reg_prt_frm_course(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_add_to_db")
async def callback_reg_participant_add_to_db(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_reg_prt_frm_add_to_db(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_advisor")
async def callback_reg_participant_advisor(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data({callback_query.data.split()[1]: callback_query.data.split()[2]})
    print("--------------------------------------- ", callback_query.data.split()[1], callback_query.data.split()[2])

    await pr_cb_reg_prt_frm_advisor(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_english_level")
async def callback_reg_participant_english_level(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data({callback_query.data.split()[1]: callback_query.data.split()[2]})
    print("--------------------------------------- ", callback_query.data.split()[1], callback_query.data.split()[2])

    await pr_cb_reg_prt_frm_english_level(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_translator")
async def callback_reg_participant_is_translator(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data({callback_query.data.split()[1]: callback_query.data.split()[2]})
    print("--------------------------------------- ", callback_query.data.split()[1], callback_query.data.split()[2])

    await pr_cb_reg_prt_frm_translator(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_translator_education")
async def callback_reg_participant_has_translator_education(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data({callback_query.data.split()[1]: callback_query.data.split()[2]})
    print("--------------------------------------- ", callback_query.data.split()[1], callback_query.data.split()[2])

    await pr_cb_reg_prt_frm_translator_education(callback_query, bot, state)

@router.callback_query(lambda c: c.data.split()[0] == "pr_cb_reg_prt_frm_theme")
async def callback_reg_participant_theme(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await state.update_data({callback_query.data.split()[1]: callback_query.data.split()[2]})
    print("--------------------------------------- ", callback_query.data.split()[1], callback_query.data.split()[2])

    await pr_cb_reg_prt_frm_theme(callback_query, bot, state)

@router.message(RegisterStates.theme)
async def msg_theme(message: types.Message, state: FSMContext):
    await pr_cb_handle_theme_input(message, state)

# ---------------------------- Browse routers -----------------------------------------


@router.callback_query(lambda c: c.data == "pr_cb_browse_next_event")
async def callback_next_event(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_browse_next_event(callback_query, bot, state)

@router.callback_query(lambda c: c.data == "pr_cb_browse_prev_event")
async def callback_prev_event(
    callback_query: types.CallbackQuery, bot: Bot, state: FSMContext
) -> None:
    await pr_cb_browse_prev_event(callback_query, bot, state)
