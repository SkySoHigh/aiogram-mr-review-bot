class EngLocale:
    class Common:
        GREETING_MSG = (
            "πHello, i am QA Review Bot reminder.\n" "For more info pls send me: /help"
        )

        HELP_MSG = (
            "This is QA Review Bot to distribute review tasks among testers.\n"
            "Please, send me link to MR via:\n"
            "/review *link*"
        )

        CHAT_ORIGIN_MSG = "From:"

    class Menu:
        MENU_HEADER = "Menu:"
        SHOW_USER_TASKS_BTN = "π’ Send my active tasks to pm"
        SHOW_ALL_TASKS_BTN = "π show all active tasks"
        SHOW_ADM_MENU_BTN = "π send menu to pm"

        SHOW_ALL_MY_TASKS_FOR_REVIEW = "π’ Show tasks - [i am reviewer]"
        SHOW_ALL_MY_TASKS_ON_REVIEW = "π’ Show tasks - [i am publisher]"

    class Task:
        # General
        ID = "Id"
        STATUS = "Status"
        URL = "Link"

        # When published
        PUBLISHED_AT = "Published at"
        PUBLISHED_BY = "Publisher"

        # When taken on review
        REVIEWED_BY = "Reviewer"
        TAKEN_TO_REVIEW_AT = "Taken to review at"

        # When on review
        SUBMITTED_TO_FINAL_REVIEW = "Submitted to confirm"
        REJECTED_AT = "Rejected at"

        # When completed
        COMPLETED_AT = "Completed at"
        COMPLETED_BY = "Final reviewer"

        # BTNS
        # \- When taken on review
        TAKE_BTN = "π¬ Take"

        # \- When on review
        SUBMIT_BTN = "β Submit to final review π"
        REJECT_BTN = "β Reject"
        RESUBMIT_BTN = " βοΈ Submit to review again"

        # \- When completed
        FINAL_CONFIRM_BTN = "π Confirm β"
        FINAL_REJECT_BTN = "π Reject β"

        # Notify
        TASK_MR_IS_REJECTED = "Review rejected π π© π§»"
        TASK_IS_READY_FOR_FINAL_REVIEW = "π¦Ύ Task is ready for final review π§"
        TASK_FIX_REQUIRED = "π₯π₯π₯ π  Fix required π₯π₯π₯"
        TASK_IS_READY_REVIEW_AFTER_FIX = "π  Review after fix is required"

        # Other
        NO_TASKS_FOR_REVIEW_MSG = "No tasks for review π€ π"
        NO_TASKS_ON_REVIEW_MSG = "No tasks on review π βοΈ"
        TASK_LIMIT_IS = "π€ Task query limit per time is"

    class Error:
        INCORRECT_REVIEW_SUBMIT_COMMAND = (
            "βοΈIncorrect command.\n"
            "Pls, send me review command with link to MR separated by whitespace.\n"
            "More info: /help"
        )
        SUBMITTED_URL_ALREADY_EXISTS = (
            "βοΈ Task with submitted url already registered.\n"
            "Please, use functionality to show all active tasks."
        )
        UNABLE_TO_INITIALIZE_CHAT = (
            "Bot can't initiate conversation with a user π­. Please, add me first π."
        )
        UNABLE_TO_SUBMIT_TASK_BY_ANY_USER = (
            "βοΈ Forbidden. Only reviewer or admin could submit task to final review."
        )

        UNABLE_TO_PASS_TASK_TO_REVIEW_BY_ANY_USER = (
            "βοΈ Forbidden. Only reviewer or admin could submit task to final review."
        )
        UNABLE_TO_REJECT_TASK_FROM_FINAL_REVIEW_BY_ANY_USER = (
            "βοΈ Forbidden. Only reviewer or admin could reject task from review."
        )
        UNABLE_TO_RESUBMIT_TASK_TO_REVIEW_BY_ANY_USER = (
            "βοΈ Forbidden. Only publisher or admin could resubmit task."
        )

        UNABLE_TO_SELF_REVIEW = "βοΈ Forbidden. You can't review yourself πΏ"
        ADMIN_RIGHTS_REQUIRED = "βοΈ Forbidden. Admins rights required"

        CONTACT_ADMINISTRATOR = "π² Please, contact administrator."
        MESSAGE_FORWARD_NOT_FOUND = "βοΈ Message to forward not found. Looks like someone removed bot task from chat."
        MESSAGE_TO_EDIT_NOT_FOUND = "βοΈ Message to edit not found. Looks like someone removed bot task from chat."
        TO_MANY_UNFINISHED_TASKS = "To many unfinished tasks"
        ERROR_MSG_WILL_BE_REMOVED_IN = "π Error msg will be removed in"

        THROTTLING_WARN = "β‘οΈTo many requests.\n" "β³Please try again in: "
