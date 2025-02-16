"""posts

Revision ID: 700ec5f88976
Revises: 1fb8b9dc4196
Create Date: 2025-02-16 16:34:26.453390

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "700ec5f88976"
down_revision: Union[str, None] = "1fb8b9dc4196"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "microblog_posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("text", sa.String(length=350), nullable=True),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_microblog_posts")),
    )
    op.create_index(
        op.f("ix_microblog_posts_id"), "microblog_posts", ["id"], unique=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_microblog_posts_id"), table_name="microblog_posts")
    op.drop_table("microblog_posts")
    # ### end Alembic commands ###
