class RuLocale:
    class Common:
        GREETING_MSG = f'Привет!😄\n' \
                       f' Я QA Review Bot.\n' \
                       f'Моя главная задача - отправлять пользователям нотификации по задачам рецензирвоания\n' \
                       f'Чтобы узнать больше введите: /help'

        HELP_MSG = f'QA Review Bot используется для распределения задач рецензирования между участниками чата' \
                   f'Для начала работы отправьте 🔗ссылку на мердж-реквест:\n' \
                   f'/review *ссылка*'

        CHAT_ORIGIN_MSG = 'Источник:'

    class Menu:
        # Group
        MENU_HEADER = 'Меню'
        SHOW_USER_TASKS_BTN = '🟢 Отправить мои активные задачи в ЛС'
        SHOW_ALL_TASKS_BTN = '🔐 Показать все активные задачи'
        SHOW_ADM_MENU_BTN = '🔐 Отправить меню админа в ЛС'

        # Pm
        SHOW_ALL_MY_TASKS = '🟢 Показать мои активные задчи по всем чатам'

    class Task:
        # General
        ID = 'Идентификатор'
        STATUS = 'Статус'
        URL = 'Ссылка'

        # When published
        PUBLISHED_AT = 'Время публикации'
        PUBLISHED_BY = 'Заявитель'

        # When taken on review
        REVIEWED_BY = 'Рецензент'
        TAKEN_TO_REVIEW_AT = 'Время принятия на рецензироание'

        # When on review
        SUBMITTED_TO_FINAL_REVIEW = 'Время подтверждения рецензии'
        REJECTED_AT = 'Время отклонения ревью'

        # When completed
        COMPLETED_AT = 'Время завершения'
        COMPLETED_BY = 'Финальный рецензент'

        # BTNS
        # \- When taken on review
        TAKE_BTN = '🔬 Взять на ревью'

        # \- When on review
        SUBMIT_BTN = '✅ Отправить на финальное ревью 👀'
        REJECT_BTN = '❌ Отклонить'
        RESUBMIT_BTN = ' ⚙️ Подать на ревью еще раз'

        # \- When completed
        FINAL_CONFIRM_BTN = '🔐 Подтвердить ✅'
        FINAL_REJECT_BTN = '🔐 Отклонить  ❌'

        # Notify
        TASK_MR_IS_REJECTED = 'Отклонено на финальном ревью 🙈 💩 🧻'
        TASK_IS_READY_FOR_FINAL_REVIEW = '🦾 Задача готова для финального рецензирования 🧐'
        TASK_FIX_REQUIRED = '🔥🔥🔥 🛠 Задача требует исправления 🔥🔥🔥'
        TASK_IS_READY_REVIEW_AFTER_FIX = '🛠 Задача требует реценезирвоания после исправления'

        # Other
        NO_TASKS_MSG = 'Нет задач на ревью 😎 🎉'
        TASK_LIMIT_IS = '💤 Максимальное число задач в одном ответе'

    class Error:
        INCORRECT_REVIEW_SUBMIT_COMMAND = '⛔️ Некорректная команда\n' \
                                          'Пожалуйста, отправьте команду /review и ссылку через пробел\n' \
                                          'Помощь: /help'
        UNABLE_TO_INITIALIZE_CHAT = 'Бот: Не могу отправить вам сообщение в ЛС 😭. Пожалуйста, сперва добавьте меня 🙏.'

        UNABLE_TO_PASS_TASK_TO_REVIEW_BY_ANY_USER = '⛔️ Запрещено. Только рецензент или администратор ' \
                                                    'могут подать заявку на финальное ревью'
        UNABLE_TO_REJECT_TASK_FROM_FINAL_REVIEW_BY_ANY_USER = '⛔️ Запрещено. Только рецензент или администратор ' \
                                                              'могут отклонить заявку на ревью'
        UNABLE_TO_RESUBMIT_TASK_TO_REVIEW_BY_ANY_USER = '⛔️ Запрещено. Только заявитель или администратор ' \
                                                        'могут подать заявку на ревью повторно'
        UNABLE_TO_SELF_REVIEW = '⛔️ Запрещено. Нельзя рценезировать самого себя 🗿'
        ADMIN_RIGHTS_REQUIRED = '⛔️ Запрещено. Нужны права администратора'

        CONTACT_ADMINISTRATOR = '📲 Пожалуйста, обратитесь к администратору'
        MESSAGE_FORWARD_NOT_FOUND = '✉️ Сообщение для переотправки не найдено. Похоже, что кто-то его удалил 🤭'
        MESSAGE_TO_EDIT_NOT_FOUND = '✉️ Сообщение для редактирование не найдено. Похоже, что кто-то его удалил 🤭'
        TO_MANY_UNFINISHED_TASKS = 'Слишком много незавершенных задач'
        ERROR_MSG_WILL_BE_REMOVED_IN = '🕐 Сообщение об ошибке будет удалено в течении'
