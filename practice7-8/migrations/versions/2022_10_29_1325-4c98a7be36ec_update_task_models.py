"""update task models

Revision ID: 4c98a7be36ec
Revises: 9e3348faf429
Create Date: 2022-10-29 13:25:36.380172

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "4c98a7be36ec"
down_revision = "9e3348faf429"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "task_priority",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("priority", sa.String(length=25), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__task_priority__id")),
        sa.UniqueConstraint(
            "priority", name=op.f("uq__task_priority__priority")
        ),
        schema="shop",
    )
    
    op.drop_constraint(
        "fk__task__priority__priority_id",
        "task",
        schema="shop",
        type_="foreignkey",
    )
    op.drop_table("priority", schema="shop")
    
    op.add_column(
        "task",
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        schema="shop",
    )
    op.add_column(
        "task",
        sa.Column(
            "executor_id", postgresql.UUID(as_uuid=True), nullable=False
        ),
        schema="shop",
    )
    op.drop_constraint(
        "fk__task__user__executor", "task", schema="shop", type_="foreignkey"
    )
    
    op.drop_constraint(
        "fk__task__user__author", "task", schema="shop", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk__task__user__author_id"),
        "task",
        "user",
        ["author_id"],
        ["id"],
        source_schema="shop",
        referent_schema="shop",
        initially="DEFERRED",
        deferrable=True,
    )
    op.create_foreign_key(
        op.f("fk__task__user__executor_id"),
        "task",
        "user",
        ["executor_id"],
        ["id"],
        source_schema="shop",
        referent_schema="shop",
        initially="DEFERRED",
        deferrable=True,
    )
    op.create_foreign_key(
        op.f("fk__task__task_priority__priority_id"),
        "task",
        "task_priority",
        ["priority_id"],
        ["id"],
        source_schema="shop",
        referent_schema="shop",
        initially="DEFERRED",
        deferrable=True,
    )
    op.drop_column("task", "author", schema="shop")
    op.drop_column("task", "executor", schema="shop")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "task",
        sa.Column(
            "executor", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        schema="shop",
    )
    op.add_column(
        "task",
        sa.Column(
            "author", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        schema="shop",
    )
    op.drop_constraint(
        op.f("fk__task__task_priority__priority_id"),
        "task",
        schema="shop",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk__task__user__executor_id"),
        "task",
        schema="shop",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk__task__user__author_id"),
        "task",
        schema="shop",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk__task__user__author",
        "task",
        "user",
        ["author"],
        ["id"],
        source_schema="shop",
        referent_schema="shop",
        initially="DEFERRED",
        deferrable=True,
    )
    op.create_foreign_key(
        "fk__task__priority__priority_id",
        "task",
        "priority",
        ["priority_id"],
        ["id"],
        source_schema="shop",
        referent_schema="shop",
        initially="DEFERRED",
        deferrable=True,
    )
    op.create_foreign_key(
        "fk__task__user__executor",
        "task",
        "user",
        ["executor"],
        ["id"],
        source_schema="shop",
        referent_schema="shop",
        initially="DEFERRED",
        deferrable=True,
    )
    op.drop_column("task", "executor_id", schema="shop")
    op.drop_column("task", "author_id", schema="shop")
    op.create_table(
        "priority",
        sa.Column(
            "id", postgresql.UUID(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "priority",
            sa.VARCHAR(length=25),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk__priority__id"),
        sa.UniqueConstraint("priority", name="uq__priority__priority"),
        schema="shop",
    )
    op.drop_table("task_priority", schema="shop")
    # ### end Alembic commands ###
