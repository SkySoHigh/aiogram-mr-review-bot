"""alter tasks, change int to bigint for all columns excluding id

Revision ID: dacf5ecf7879
Revises: fcf62e4ac4a4
Create Date: 2023-01-10 15:10:07.005258

"""
from alembic import op
from sqlalchemy import BigInteger, Integer

# revision identifiers, used by Alembic.
revision = "dacf5ecf7879"
down_revision = "fcf62e4ac4a4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("tasks", "chat_id", type_=BigInteger)
    op.alter_column("tasks", "publisher_msg_id", type_=BigInteger)
    op.alter_column("tasks", "publisher_id", type_=BigInteger)
    op.alter_column("tasks", "reply_msg_id", type_=BigInteger)
    op.alter_column("tasks", "reviewer_id", type_=BigInteger)


def downgrade() -> None:
    op.alter_column("tasks", "chat_id", type_=Integer)
    op.alter_column("tasks", "publisher_msg_id", type_=Integer)
    op.alter_column("tasks", "publisher_id", type_=Integer)
    op.alter_column("tasks", "reply_msg_id", type_=Integer)
    op.alter_column("tasks", "reviewer_id", type_=Integer)
