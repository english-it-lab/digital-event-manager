from aiogram.fsm.state import StatesGroup, State


class RegisterStates(StatesGroup):
    # User data changing
    fio = State()
    phone = State()
    email = State()
    waiting_for_verification_code = State()

    # Register to event
    theme = State()
