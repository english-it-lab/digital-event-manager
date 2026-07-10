# Тест-кейсы для API POST /api/v1/notifications/draw/results

## Позитивные тесты

| ID | Название | Предусловие | Шаги | Ожидаемый результат |
|----|----------|-------------|------|---------------------|
| TC-01 | Успешная отправка уведомлений | - Event с id=1 существует<br>- У event есть группы<br>- У групп есть темы<br>- У участников есть email | 1. POST /notifications/draw/results<br>2. Body: `{"eventId": 1}` | 200 OK<br>`{"success": true, "message": "Уведомления успешно отправлены"}` |
| TC-02 | Отправка без уведомлений (нет участников) | - Event существует<br>- Группы есть<br>- У участников нет email или отключены уведомления | 1. POST /notifications/draw/results<br>2. Body: `{"eventId": 2}` | 200 OK<br>Уведомления не отправлены, но API успешен |

## Негативные тесты (ошибки клиента)

| ID | Название | Предусловие | Шаги | Ожидаемый результат |
|----|----------|-------------|------|---------------------|
| TC-03 | Event не найден | Event с id=999 не существует | POST с `{"eventId": 999}` | 404 Not Found<br>Сообщение: "Event with id 999 not found" |
| TC-04 | eventId = 0 | - | POST с `{"eventId": 0}` | 422 Validation Error |
| TC-05 | Отрицательный eventId | - | POST с `{"eventId": -5}` | 422 Validation Error |
| TC-06 | Отсутствует eventId | - | POST с `{}` | 422 Validation Error |
| TC-07 | eventId как строка | - | POST с `{"eventId": "abc"}` | 422 Validation Error |
| TC-08 | eventId как float | - | POST с `{"eventId": 1.5}` | 422 Validation Error |
| TC-09 | eventId как null | - | POST с `{"eventId": null}` | 422 Validation Error |
| TC-10 | Пустой body | - | POST с пустым телом | 422 Validation Error |

## Негативные тесты (ошибки сервера)

| ID | Название | Предусловие | Шаги | Ожидаемый результат |
|----|----------|-------------|------|---------------------|
| TC-11 | Ошибка подключения к БД | БД недоступна | POST с `{"eventId": 1}` | 500 Internal Server Error |
| TC-12 | Ошибка SMTP | SMTP сервер недоступен | POST с `{"eventId": 1}` | 500 Internal Server Error |