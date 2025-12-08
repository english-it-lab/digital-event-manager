from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from os.path import join, dirname
from components.shared.locale import load_locales, get_locale_str

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path, **kwargs: get_locale_str(locale, f"{lang}.{path}").format(**kwargs)

# экраны авторизации

async def show_auth_code_request(message: types.Message, lang="ru"):
    """Просит ввести код"""
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, "reports_evaluation.main.back"), callback_data="cb_mm_main")
    
    # Если это callback (нажатие кнопки меню), редактируем сообщение
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(
            getstr(lang, "reports_evaluation.auth.enter_code"), 
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML"
        )
    else:
        # Если это сообщение (например, после неверного ввода), отправляем новое
        await message.answer(
            getstr(lang, "reports_evaluation.auth.enter_code"), 
            reply_markup=keyboard.as_markup(),
            parse_mode="HTML"
        )

async def show_jury_selection(message: types.Message, juries_list, lang="ru"):
    """Показывает список кнопок с именами членов жюри"""
    keyboard = InlineKeyboardBuilder()
    
    for jury in juries_list:
        # jury = (id, first_name, last_name, middle_name)
        j_id, f_name, l_name, m_name = jury
        # Формируем ФИО
        full_name = f"{l_name} {f_name} {m_name or ''}".strip()
        
        # callback_data: `cb_re_login_<jury_id>`
        keyboard.button(text=full_name, callback_data=f"cb_re_login_{j_id}")

    keyboard.button(text=getstr(lang, "reports_evaluation.main.back"), callback_data="cb_re_main") # Вернуться к вводу кода
    keyboard.adjust(1) # Кнопки в один столбик

    await message.answer(
        getstr(lang, "reports_evaluation.auth.select_jury"),
        reply_markup=keyboard.as_markup()
    )

#Главное меню модуля (после входа)

async def show_evaluation_menu(message: types.Message, user_name: str, lang="ru"):
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text=getstr(lang, "reports_evaluation.main.button_evaluate"), callback_data="cb_re_evaluate")
    keyboard.button(text=getstr(lang, "reports_evaluation.main.button_results"), callback_data="cb_re_results")
    keyboard.button(text=getstr(lang, "reports_evaluation.main.button_finish"), callback_data="cb_re_finish")
    
    # --- НОВАЯ КНОПКА ---
    keyboard.button(text="🚪 Выйти из аккаунта", callback_data="cb_re_logout")
    # --------------------

    keyboard.button(text=getstr(lang, "reports_evaluation.main.back"), callback_data="cb_mm_main")
    
    keyboard.adjust(1)
    
    text = getstr(lang, "reports_evaluation.main.caption", name=user_name)
    
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text, reply_markup=keyboard.as_markup(), parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

async def show_participant_selection(message: types.Message, participants, lang="ru"):
    """Показывает список участников для оценки."""
    keyboard = InlineKeyboardBuilder()
    
    if not participants:
        text = getstr(lang, "reports_evaluation.evaluate.empty_list")
    else:
        text = getstr(lang, "reports_evaluation.evaluate.select_participant")
        for p in participants:
            # p = (id, first_name, last_name, topic)
            p_id, f_name, l_name, topic = p
            # Кнопка: "Фамилия И. - Тема..."
            label = f"{l_name} {f_name} - {topic[:20]}..."
            keyboard.button(text=label, callback_data=f"cb_re_eval_p_{p_id}")

    keyboard.button(text=getstr(lang, "reports_evaluation.main.back"), callback_data="cb_re_main")
    keyboard.adjust(1)
    
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text, reply_markup=keyboard.as_markup(), parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

async def show_leaderboard_text(message: types.Message, results, lang="ru"):
    """Формирует и отправляет таблицу результатов."""
    header = getstr(lang, "reports_evaluation.results.header")
    
    if not results or results[0][2] is None: 
        body = getstr(lang, "reports_evaluation.results.empty")
    else:
        lines = []
        
        # Логика ранжирования
        rank = 1
        prev_score = None
        
        # results = [(last, first, score), ...]
        for i, row in enumerate(results):
            l_name, f_name, score = row
            score_int = int(score) if score else 0
            
            # Показываем только тех, у кого есть баллы (> 0)
            if score_int > 0:
                # Если текущий балл меньше предыдущего, увеличиваем место
                # (Если равен - место остается тем же)
                if prev_score is not None and score_int < prev_score:
                    rank += 1
                
                prev_score = score_int
                
                full_name = f"{l_name} {f_name}"
                line = getstr(lang, "reports_evaluation.results.row", 
                              rank=rank, name=full_name, score=score_int)
                lines.append(line)
        
        if not lines:
             body = getstr(lang, "reports_evaluation.results.empty")
        else:
             body = "\n".join(lines)
             # Добавим примечание о сортировке, как в ТЗ
             body += "\n\n<i>* Участники с равными баллами занимают одно место и отсортированы по алфавиту.</i>"

    text = header + body
    
    # Кнопка "Назад"
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=getstr(lang, "reports_evaluation.main.back"), callback_data="cb_re_main")
    
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text, reply_markup=keyboard.as_markup(), parse_mode="HTML")

async def show_chairman_menu(message: types.Message, lang="ru"):
    """Меню подтверждения завершения (только для председателя)."""
    text = getstr(lang, "reports_evaluation.chairman.confirm_finish")
    keyboard = InlineKeyboardBuilder()
    
    keyboard.button(text=getstr(lang, "reports_evaluation.chairman.button_confirm"), callback_data="cb_re_finish_confirm")
    keyboard.button(text=getstr(lang, "reports_evaluation.chairman.button_cancel"), callback_data="cb_re_main")
    
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text, reply_markup=keyboard.as_markup(), parse_mode="HTML")
def get_score_keyboard():
    """Возвращает кнопки от 0 до 4."""
    builder = InlineKeyboardBuilder()
    for i in range(5): # 0, 1, 2, 3, 4
        builder.button(text=str(i), callback_data=f"score_{i}")
    builder.adjust(5) # Все в один ряд
    return builder.as_markup()

async def show_criteria_step(message: types.Message, step_key: str, lang="ru"):
    """Показывает сообщение с описанием критерия и кнопками."""
    text = getstr(lang, f"reports_evaluation.criteria.{step_key}")
    kb = get_score_keyboard()
    
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text, reply_markup=kb, parse_mode="HTML")
    else:
        await message.answer(text, reply_markup=kb, parse_mode="HTML")

async def show_comment_step(message: types.Message, lang="ru"):
    """Просит ввести комментарий."""
    text = getstr(lang, "reports_evaluation.criteria.comment")
    
    builder = InlineKeyboardBuilder()
    builder.button(text=getstr(lang, "reports_evaluation.criteria.skip"), callback_data="skip_comment")
    
    if isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")

async def show_confirmation_step(message: types.Message, data: dict, lang="ru"):
    """Показывает итог и кнопку Сохранить."""
    # data содержит: p_name, scores={c1:.., c2:..}, comment
    scores = data.get('scores', {})
    total = sum(scores.values())
    
    text = getstr(lang, "reports_evaluation.criteria.summary",
                  name=data.get('p_name', 'Unknown'),
                  s1=scores.get('c1'),
                  s2=scores.get('c2'),
                  s3=scores.get('c3'),
                  s4=scores.get('c4'),
                  s5=scores.get('c5'),
                  comment=data.get('comment', '-'),
                  total=total)
    
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Сохранить", callback_data="save_score_confirm")
    builder.button(text="❌ Отмена", callback_data="cb_re_evaluate")
    builder.adjust(1)
    
    # Если это сообщение (после ввода коммента), шлем новое, иначе редактируем
    if isinstance(message, types.Message):
        await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    else:
        await message.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")