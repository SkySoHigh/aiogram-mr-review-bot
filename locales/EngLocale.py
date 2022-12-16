class Locale:
    class Common:
        GREETING_MSG = f'Hello, i am QA Review Bot reminder.\n' \
                       f'For more info pls send me: /help'

        HELP_MSG = f'This is QA Review Bot to distribute review tasks among testers.' \
                   f'Please, send me link to MR via:\n' \
                   f'/review *link*'

        CHAT_ORIGIN_MSG = 'Origin:'

    class Menu:
        MENU_HEADER = 'Menu:'
        SHOW_TASKS_BTN = 'Show my tasks'
        SHOW_TASKS_BTN_CONFIRMED_MSG = 'Your review tasks are sent to pm'
        SHOW_ADM_MENU_BTN = 'Show admin menu'
        SHOW_ADM_MENU_BTN_CONFIRMED_MSG = 'Admin menu is sent to pm'

    class NewTaskOnReview:
        NEW_TASK_MSG = 'New task submitted!\n' \
                     'Anyone want to take it?'
        TAKE_NEW_TASK_BTN = 'Take it!'

    class TaskSubmitted:
        SUBMITTED_MSG_ACCEPTED_TIME = 'Accepted:'
        SUBMITTED_MSG_REQUESTED_BY = 'Applicant:'
        SUBMITTED_MSG_ACCEPTED_BY = 'Reviewer:'

    class TaskConfirmed:
        CONFIRMED_MSG_COMPLETION_TIME = 'Completed:'
        CONFIRMED_TASK_BTN = 'Done!'

    class Error:
        UNABLE_TO_INITIALIZE_CHAT = 'Bot can\'t initiate conversation with a user. Please, add me firs.'
        INCORRECT_REVIEW_SUBMIT_COMMAND = 'Incorrect command.\n' \
                                          'Pls, send me review command with link to MR separated by whitespace.\n' \
                                          'More info: /help'
        UNABLE_TO_CONFIRM_TASK_BY_ANY_USER = 'Forbidden. Only reviewer or admin could confirm review task.'
        CONTACT_ADMINISTRATOR = 'Please, contact administrator.'
        MESSAGE_FORWARD_NOT_FOUND = 'Message to forward not found. Looks like someone removed bot task from chat.'
        MESSAGE_TO_EDIT_NOT_FOUND = 'Message to edit not found. Looks like someone removed bot task from chat.'

