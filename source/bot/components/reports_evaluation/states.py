from aiogram.fsm.state import State, StatesGroup

class ReportsEvaluationState(StatesGroup):
    waiting_for_access_code = State()  # Ждем ввод кода
    choosing_jury_member = State()     # Ждем выбор фамилии из списка
    # состояния для процесса оценки
    eval_c1_organization = State()
    eval_c2_content = State()
    eval_c3_visuals = State()
    eval_c4_mechanics = State()
    eval_c5_delivery = State()
    eval_comment = State()
    eval_confirm = State()