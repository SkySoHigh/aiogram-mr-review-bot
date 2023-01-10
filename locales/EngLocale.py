class EngLocale:
    class Common:
        GREETING_MSG = (
            "😄Hello, i am QA Review Bot reminder.\n" "For more info pls send me: /help"
        )

        HELP_MSG = (
            "This is QA Review Bot to distribute review tasks among testers.\n"
            "Please, send me link to MR via:\n"
            "/review *link*"
        )

        CHAT_ORIGIN_MSG = "From:"

    class Menu:
        MENU_HEADER = "Menu:"
        SHOW_USER_TASKS_BTN = "🟢 Send my active tasks to pm"
        SHOW_ALL_TASKS_BTN = "🔐 show all active tasks"
        SHOW_ADM_MENU_BTN = "🔐 send menu to pm"

        SHOW_ALL_MY_TASKS = "🟢 Show my active tasks"

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
        TAKE_BTN = "🔬 Take"

        # \- When on review
        SUBMIT_BTN = "✅ Submit to final review 👀"
        REJECT_BTN = "❌ Reject"
        RESUBMIT_BTN = " ⚙️ Submit to review again"

        # \- When completed
        FINAL_CONFIRM_BTN = "🔐 Confirm ✅"
        FINAL_REJECT_BTN = "🔐 Reject ❌"

        # Notify
        TASK_MR_IS_REJECTED = "Review rejected 🙈 💩 🧻"
        TASK_IS_READY_FOR_FINAL_REVIEW = "🦾 Task is ready for final review 🧐"
        TASK_FIX_REQUIRED = "🔥🔥🔥 🛠 Fix required 🔥🔥🔥"
        TASK_IS_READY_REVIEW_AFTER_FIX = "🛠 Review after fix is required"

        # Other
        NO_TASKS_MSG = "There is no tasks on review! 😎 🎉"
        TASK_LIMIT_IS = "💤 Task query limit per time is"

    class Error:
        INCORRECT_REVIEW_SUBMIT_COMMAND = (
            "⛔️Incorrect command.\n"
            "Pls, send me review command with link to MR separated by whitespace.\n"
            "More info: /help"
        )
        UNABLE_TO_INITIALIZE_CHAT = (
            "Bot can't initiate conversation with a user 😭. Please, add me first 🙏."
        )
        UNABLE_TO_SUBMIT_TASK_BY_ANY_USER = (
            "⛔️ Forbidden. Only reviewer or admin could submit task to final review."
        )

        UNABLE_TO_PASS_TASK_TO_REVIEW_BY_ANY_USER = (
            "⛔️ Forbidden. Only reviewer or admin could submit task to final review."
        )
        UNABLE_TO_REJECT_TASK_FROM_FINAL_REVIEW_BY_ANY_USER = (
            "⛔️ Forbidden. Only reviewer or admin could reject task from review."
        )
        UNABLE_TO_RESUBMIT_TASK_TO_REVIEW_BY_ANY_USER = (
            "⛔️ Forbidden. Only publisher or admin could resubmit task."
        )

        UNABLE_TO_SELF_REVIEW = "⛔️ Forbidden. You can't review yourself 🗿"
        ADMIN_RIGHTS_REQUIRED = "⛔️ Forbidden. Admins rights required"

        CONTACT_ADMINISTRATOR = "📲 Please, contact administrator."
        MESSAGE_FORWARD_NOT_FOUND = "✉️ Message to forward not found. Looks like someone removed bot task from chat."
        MESSAGE_TO_EDIT_NOT_FOUND = "✉️ Message to edit not found. Looks like someone removed bot task from chat."
        TO_MANY_UNFINISHED_TASKS = "To many unfinished tasks"
        ERROR_MSG_WILL_BE_REMOVED_IN = "🕐 Error msg will be removed in"
