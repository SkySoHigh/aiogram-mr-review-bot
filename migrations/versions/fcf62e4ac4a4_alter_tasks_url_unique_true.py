"""alter tasks.url unique -> true

Revision ID: fcf62e4ac4a4
Revises: 
Create Date: 2023-01-10 12:45:35.591779

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "fcf62e4ac4a4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("uq_url", "tasks", ["url"])


def downgrade() -> None:
    op.drop_constraint(
        "uq_url",
        "tasks",
    )
