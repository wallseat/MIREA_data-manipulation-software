"""set defaults

Revision ID: 842ae59fe36e
Revises: 67f0919277d3
Create Date: 2022-10-23 14:50:54.173621

"""
import secrets
import os

from alembic import op
import sqlalchemy as sa

from app.models import User, Group, UserGroup
from app.core.security import get_password_hash

# revision identifiers, used by Alembic.
revision = "842ae59fe36e"
down_revision = "67f0919277d3"
branch_labels = None
depends_on = None


def create_admin() -> None:
    connection = op.get_bind()

    admin_pass = secrets.token_urlsafe(16)

    admin_user_id = connection.execute(
        sa.insert(User).values(
            {"name": "admin", "password_hash": get_password_hash(admin_pass)}
        )
    ).inserted_primary_key[0]

    admin_group_id = connection.execute(
        sa.insert(Group).values({"name": "admin"})
    ).inserted_primary_key[0]

    connection.execute(
        sa.insert(UserGroup).values(
            {"user_id": admin_user_id, "group_id": admin_group_id}
        )
    )

    temp_file_name = "ADMIN_CREDENTIALS"

    with open(temp_file_name, "w") as f:
        f.write(
            f"READ AND SAVE PASSWORD, THIS FILE WILL BE DELETED\nadmin {admin_pass}"
        )

    input(f"Read {temp_file_name} then press any key\n")

    os.remove(temp_file_name)


def delete_admin() -> None:
    connection = op.get_bind()

    connection.execute(
        sa.delete(UserGroup).where(
            UserGroup.user_id
            == sa.select([User.id]).where(User.name == "admin").scalar_subquery()
        )
    )

    connection.execute(sa.delete(User).where(User.name == "admin"))

    connection.execute(sa.delete(Group).where(Group.name == "admin"))


def upgrade() -> None:
    create_admin()

    op.execute(sa.insert(Group).values([{"name": "worker"}, {"name": "manager"}]))


def downgrade() -> None:
    delete_admin()

    op.execute(sa.delete(Group).where(Group.name.in_(["worker", "manager"])))
