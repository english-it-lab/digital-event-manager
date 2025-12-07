from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State  # <--- Вот этой строки не хватало
from components.shared.db import Database

# Импорты наших модулей
from components.reports_evaluation.frontend import (
    show_auth_code_request, 
    show_jury_selection, 
    show_evaluation_menu,
    show_participant_selection,
    show_leaderboard_text,
    show_chairman_menu,
    show_criteria_step,
    show_comment_step,
    show_confirmation_step,
    getstr
)
from components.reports_evaluation.backend import (
    is_user_authorized, 
    get_juries_by_code, 
    link_user_to_jury,
    get_jury_info,
    get_participants_for_jury,
    get_leaderboard,
    save_score,
    logout_user
)
from components.reports_evaluation.states import ReportsEvaluationState

router = Router()

# вход в раздел "Оценка докладов"
@router.callback_query(lambda c: c.data == "cb_re_main")
async def cb_re_main_menu(callback_query: types.CallbackQuery, bot: Bot, state: FSMContext, db: Database) -> None:
    tg_id = callback_query.from_user.id
    
    # проверяем, авторизован ли пользователь
    user_info = await is_user_authorized(db, tg_id)
    
    if user_info:
        # если авторизован, показываем главное меню оценки
        # user_info = (jury_id, first_name, last_name)
        full_name = f"{user_info[2]} {user_info[1]}"
        await show_evaluation_menu(callback_query, full_name)
    else:
        # если нет, просим ввести код
        await state.set_state(ReportsEvaluationState.waiting_for_access_code)
        await show_auth_code_request(callback_query)

# обработка ввода кода доступа
@router.message(ReportsEvaluationState.waiting_for_access_code)
async def handle_access_code(message: types.Message, state: FSMContext, db: Database):
    code = message.text.strip()
    
    # ищем членов жюри с таким кодом
    juries = await get_juries_by_code(db, code)
    
    if not juries:
        # код неверный
        await message.answer(getstr("ru", "reports_evaluation.auth.invalid_code"))
        return

    # код верный, показываем список людей
    await state.set_state(ReportsEvaluationState.choosing_jury_member)
    await show_jury_selection(message, juries)

# обработка выбора человека (нажатие на кнопку с именем)
@router.callback_query(ReportsEvaluationState.choosing_jury_member, F.data.startswith("cb_re_login_"))
async def handle_jury_selection(callback_query: types.CallbackQuery, state: FSMContext, db: Database):
    # извлекаем ID из callback_data (cb_re_login_123)
    jury_id = int(callback_query.data.split("_")[-1])
    tg_id = callback_query.from_user.id
    
    # привязываем пользователя в БД
    success = await link_user_to_jury(db, jury_id, tg_id)
    
    if success:
        # авторизация завершена
        await state.clear()
        
        # получаем данные для приветствия
        # просто перезапросим авторизацию, чтобы получить имя
        user_info = await is_user_authorized(db, tg_id)
        full_name = f"{user_info[2]} {user_info[1]}"
        
        await show_evaluation_menu(callback_query, full_name)
    else:
        await callback_query.answer("Ошибка привязки пользователя.", show_alert=True)

# обработчик кнопки "Назад" внутри авторизации
@router.callback_query(lambda c: c.data == "cb_re_main", ReportsEvaluationState.choosing_jury_member)
async def back_to_code_input(callback_query: types.CallbackQuery, state: FSMContext):
    # возвращаемся к вводу кода
    await state.set_state(ReportsEvaluationState.waiting_for_access_code)
    await show_auth_code_request(callback_query)

# 5. Нажата кнопка "Оценить участника"
@router.callback_query(lambda c: c.data == "cb_re_logout")
async def cb_re_logout_handler(callback_query: types.CallbackQuery, state: FSMContext, db: Database):
    # 1. Отвязываем пользователя в БД
    await logout_user(db, callback_query.from_user.id)
    
    # 2. Очищаем состояние
    await state.clear()
    
    # 3. Сообщаем об успехе
    await callback_query.answer("Вы вышли из системы", show_alert=False)
    
    # 4. Перекидываем на экран ввода кода
    await state.set_state(ReportsEvaluationState.waiting_for_access_code)
    await show_auth_code_request(callback_query)

@router.callback_query(lambda c: c.data == "cb_re_evaluate")
async def cb_re_evaluate_list(callback_query: types.CallbackQuery, state: FSMContext, db: Database):
    tg_id = callback_query.from_user.id
    
    # 1. Получаем ID жюри
    user_info = await get_jury_info(db, tg_id)
    if not user_info:
        await callback_query.answer("Ошибка авторизации", show_alert=True)
        return
    
    jury_id = user_info[0]
    
    # 2. Получаем список студентов
    participants = await get_participants_for_jury(db, jury_id)
    
    # 3. Показываем
    await show_participant_selection(callback_query, participants)

# 6. Нажата кнопка "Текущие результаты"
@router.callback_query(lambda c: c.data == "cb_re_results")
async def cb_re_show_results(callback_query: types.CallbackQuery, db: Database):
    tg_id = callback_query.from_user.id
    
    # 1. Получаем ID жюри
    user_info = await get_jury_info(db, tg_id)
    if not user_info: return

    jury_id = user_info[0]
    
    # 2. Считаем баллы
    results = await get_leaderboard(db, jury_id)
    
    # 3. Выводим таблицу
    await show_leaderboard_text(callback_query, results)

# 7. Нажата кнопка "Завершить (Председатель)"
@router.callback_query(lambda c: c.data == "cb_re_finish")
async def cb_re_finish_check(callback_query: types.CallbackQuery, db: Database):
    tg_id = callback_query.from_user.id
    
    # 1. Проверяем, председатель ли это
    user_info = await get_jury_info(db, tg_id)
    # user_info = (id, first, last, is_chairman)
    
    if not user_info or not user_info[3]: # is_chairman is False/0
        await callback_query.answer(getstr("ru", "reports_evaluation.chairman.access_denied"), show_alert=True)
        return

    # 2. Если председатель - показываем меню подтверждения
    await show_chairman_menu(callback_query)

# 8. Начало оценки конкретного участника (Нажатие на фамилию)
@router.callback_query(F.data.startswith("cb_re_eval_p_"))
async def cb_re_start_evaluation(callback_query: types.CallbackQuery, state: FSMContext, db: Database):
    p_id = int(callback_query.data.split("_")[-1])
    
    # Получаем имя участника (для красоты), достаем из кнопки или делаем запрос
    # Для скорости просто начнем оценку
    # Сохраняем ID участника в память
    
    # Нужно получить имя участника для отображения в конце
    # Быстрый запрос (можно вынести в backend, но для краткости тут)
    cursor = db.conn.execute("SELECT last_name, first_name FROM people JOIN participants ON people.id = participants.person_id WHERE participants.id = ?", (p_id,))
    res = cursor.fetchone()
    p_name = f"{res[0]} {res[1]}" if res else "Участник"

    await state.update_data(participant_id=p_id, p_name=p_name, scores={})
    
    # Переходим к Критерию 1
    await state.set_state(ReportsEvaluationState.eval_c1_organization)
    await show_criteria_step(callback_query, "c1")

# Цепочка оценки (Критерии 1-5)

async def process_criteria(callback_query: types.CallbackQuery, state: FSMContext, current_key: str, next_state: State, next_key: str):
    """Универсальная функция для перехода между критериями."""
    score = int(callback_query.data.split("_")[1])
    
    data = await state.get_data()
    scores = data.get('scores', {})
    scores[current_key] = score
    await state.update_data(scores=scores)
    
    await state.set_state(next_state)
    if next_key == "comment":
        await show_comment_step(callback_query)
    else:
        await show_criteria_step(callback_query, next_key)

@router.callback_query(ReportsEvaluationState.eval_c1_organization, F.data.startswith("score_"))
async def step_c1(callback: types.CallbackQuery, state: FSMContext):
    await process_criteria(callback, state, "c1", ReportsEvaluationState.eval_c2_content, "c2")

@router.callback_query(ReportsEvaluationState.eval_c2_content, F.data.startswith("score_"))
async def step_c2(callback: types.CallbackQuery, state: FSMContext):
    await process_criteria(callback, state, "c2", ReportsEvaluationState.eval_c3_visuals, "c3")

@router.callback_query(ReportsEvaluationState.eval_c3_visuals, F.data.startswith("score_"))
async def step_c3(callback: types.CallbackQuery, state: FSMContext):
    await process_criteria(callback, state, "c3", ReportsEvaluationState.eval_c4_mechanics, "c4")

@router.callback_query(ReportsEvaluationState.eval_c4_mechanics, F.data.startswith("score_"))
async def step_c4(callback: types.CallbackQuery, state: FSMContext):
    await process_criteria(callback, state, "c4", ReportsEvaluationState.eval_c5_delivery, "c5")

@router.callback_query(ReportsEvaluationState.eval_c5_delivery, F.data.startswith("score_"))
async def step_c5(callback: types.CallbackQuery, state: FSMContext):
    await process_criteria(callback, state, "c5", ReportsEvaluationState.eval_comment, "comment")

# Комментарий

@router.callback_query(ReportsEvaluationState.eval_comment, F.data == "skip_comment")
async def step_comment_skip(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(comment="")
    await state.set_state(ReportsEvaluationState.eval_confirm)
    data = await state.get_data()
    await show_confirmation_step(callback, data)

@router.message(ReportsEvaluationState.eval_comment)
async def step_comment_text(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await state.set_state(ReportsEvaluationState.eval_confirm)
    data = await state.get_data()
    await show_confirmation_step(message, data)

# Финал: Сохранение

@router.callback_query(ReportsEvaluationState.eval_confirm, F.data == "save_score_confirm")
async def step_save_final(callback: types.CallbackQuery, state: FSMContext, db: Database):
    data = await state.get_data()
    tg_id = callback.from_user.id
    
    # Получаем ID жюри
    jury_info = await get_jury_info(db, tg_id)
    jury_id = jury_info[0]
    
    success = await save_score(
        db, 
        jury_id, 
        data['participant_id'], 
        data['scores'], 
        data.get('comment', '')
    )
    
    if success:
        # Показываем всплывающее уведомление (сверху экрана)
        await callback.answer("✅ Оценка успешно сохранена!", show_alert=False)
        
        # Сбрасываем состояние
        await state.clear()
        
        # Сразу рисуем Главное Меню
        full_name = f"{jury_info[2]} {jury_info[1]}"
        await show_evaluation_menu(callback, full_name)
    else:
        # Если ошибка — показываем Alert
        await callback.answer("❌ Ошибка сохранения базы данных!", show_alert=True)

# Реализация кнопки "Завершить" (Подтверждение)

@router.callback_query(lambda c: c.data == "cb_re_finish_confirm")
async def cb_re_finish_confirmed(callback_query: types.CallbackQuery, db: Database):
    # Просто показываем сообщение об успехе
    final_text = getstr('ru', 'reports_evaluation.finish.success')
    
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    kb = InlineKeyboardBuilder()
    
    # Кнопка выхода в главное меню всего бота
    kb.button(text="🏠 В главное меню", callback_data="cb_mm_main")
    
    await callback_query.message.edit_text(final_text, reply_markup=kb.as_markup(), parse_mode="HTML")