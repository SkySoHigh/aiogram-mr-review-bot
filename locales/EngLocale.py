class EngLocale:
    class Common:
        GREETING_MSG = f'Hello, i am QA Review Bot reminder.\n' \
                       f'For more info pls send me: /help'

        HELP_MSG = f'This is QA Review Bot to distribute review tasks among testers.' \
                   f'Please, send me link to MR via:\n' \
                   f'/review *link*'

        CHAT_ORIGIN_MSG = 'From:'

    class Menu:
        MENU_HEADER = 'Menu:'
        SHOW_USER_TASKS_BTN = 'Send my active tasks to pm'
        SHOW_ALL_TASKS_BTN = '[Admin] show all active tasks'
        SHOW_ADM_MENU_BTN = '[Admin] send menu to pm'

    class Task:
        # General
        ID = 'Id'
        STATUS = 'Status'
        URL = 'Link'

        # When published
        PUBLISHED_AT = 'Published at'
        PUBLISHED_BY = 'Publisher'

        # When taken on review
        REVIEWED_BY = 'Reviewer'
        TAKEN_TO_REVIEW_AT = 'Taken to review at'

        # When on review
        SUBMITTED_TO_FINAL_REVIEW = 'Submitted to confirm:'

        # When completed
        COMPLETED_AT = 'Completed at'
        COMPLETED_BY = 'Final reviewer'

        # BTNS
        # \- When taken on review
        TAKE_BTN = 'Take'

        # \- When on review
        SUBMIT_BTN = 'Submit'

        # \- When completed
        CONFIRMED_BTN = '[Admin] Confirm'
        REJECT_BTN = '[Admin] Reject'

        # Notify
        TASK_MR_IS_REJECTED = 'Review rejected'
        TASK_IS_READY_FOR_FINAL_REVIEW = 'Task is ready for final review'

        # Other
        NO_TASKS_MSG = 'There is no tasks on review!'
        TASK_LIMIT_IS = 'Task query limit per time is'

    class Error:
        UNABLE_TO_INITIALIZE_CHAT = 'Bot can\'t initiate conversation with a user. Please, add me first.'
        INCORRECT_REVIEW_SUBMIT_COMMAND = 'Incorrect command.\n' \
                                          'Pls, send me review command with link to MR separated by whitespace.\n' \
                                          'More info: /help'
        UNABLE_TO_SUBMIT_TASK_BY_ANY_USER = 'Forbidden. Only reviewer or admin could submit task to final review.'
        UNABLE_TO_SELF_REVIEW = 'Forbidden. You can\'t review yourself'
        ADMIN_RIGHTS_REQUIRED = 'Forbidden. Admins rights required'

        CONTACT_ADMINISTRATOR = 'Please, contact administrator.'
        MESSAGE_FORWARD_NOT_FOUND = 'Message to forward not found. Looks like someone removed bot task from chat.'
        MESSAGE_TO_EDIT_NOT_FOUND = 'Message to edit not found. Looks like someone removed bot task from chat.'
        TO_MANY_UNFINISHED_TASKS = 'To many unfinished tasks'
        ERROR_MSG_WILL_BE_REMOVED_IN = 'Error msg will be removed in'
