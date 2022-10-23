from uuid import uuid4
from datetime import date, datetime

from typing import Tuple, Any, List, Optional, Union, Type, Callable, TypeVar

from sqlalchemy import (
    MetaData,
    Column,
    String,
    Date,
    UniqueConstraint,
    CheckConstraint,
    PrimaryKeyConstraint,
    Index,
    ForeignKey,
    Numeric,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID, TEXT

from sqlalchemy.orm import as_declarative, declared_attr

convention = {
    "ix": "ix__%(column_0_N_name)s",
    "uq": "uq__%(table_name)s__%(column_0_N_name)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(referred_table_name)s__%(column_0_name)s",
    "pk": "pk__%(table_name)s__%(column_0_N_name)s",
}

metadata = MetaData(naming_convention=convention)
SCHEMA = "shop"

_T_Model = TypeVar("_T_Model")

_T_ColumnCollectionConstraint = Union[
    Index, PrimaryKeyConstraint, UniqueConstraint, CheckConstraint
]
_T_TableExtra = Union[
    _T_ColumnCollectionConstraint,
    Callable[[Type[_T_Model]], _T_ColumnCollectionConstraint],
]


@as_declarative(metadata=metadata)
class Base:
    __extra__: Tuple[Any, ...]
    __schema__: str = SCHEMA

    def __init_subclass__(
        cls, *args, extra: Optional[List[_T_TableExtra]] = None, **kwargs
    ) -> None:
        if extra is None:
            extra = []

        cls.__extra__ = tuple(obj(cls) if callable(obj) else obj for obj in extra)

    @declared_attr
    def __table_args__(cls):
        return (
            *cls.__extra__,
            {"schema": cls.__schema__},
        )


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False)
    password_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )


class Group(Base):
    __tablename__ = "group"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False)


class UserGroup(Base, extra=[PrimaryKeyConstraint("user_id", "group_id")]):
    __tablename__ = "user_group"

    user_id = Column(UUID(as_uuid=True), nullable=False)
    group_id = Column(UUID(as_uuid=True), nullable=False)


class Organization(Base):
    __tablename__ = "organization"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)
    location = Column(String(50), nullable=False, index=True)
    postal_code = Column(String(20), nullable=True)
    first_contract_date = Column(Date, nullable=True)


class ContactPerson(
    Base,
    extra=[
        UniqueConstraint("first_name", "second_name", "email"),
        Index("first_name", "second_name"),
    ],
):
    __tablename__ = "contact_person"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    tel = Column(String(15), nullable=True)
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.organization.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )


class EquipmentPosition(Base):
    __tablename__ = "equipment_positions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(TEXT, nullable=True)
    price = Column(Numeric(10, 2, asdecimal=False), nullable=False)


class EquipmentBalance(Base):
    __tablename__ = "equipment_balance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    position_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.equipment_positions.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )
    serial_number = Column(String(100), nullable=False, unique=True)


class Contract(Base):
    __tablename__ = "contract"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    description = Column(TEXT, nullable=True)
    type_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.contract_type.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.organization.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )


class ContractType(Base):
    __tablename__ = "contract_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(20), nullable=False, unique=True)


class ContractEquipment(
    Base, extra=[PrimaryKeyConstraint("contract_id", "equipment_id")]
):
    __tablename__ = "contract_equipment"

    contract_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.contract.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )
    equipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.equipment_balance.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )


class Task(Base):
    __tablename__ = "task"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(100), nullable=False)
    description = Column(TEXT, nullable=True)
    priority_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.priority.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )
    type_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.task_type.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )
    open_date = Column(Date, nullable=False, default=date.today)
    close_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    author = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.user.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )
    executor = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.user.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )
    contract_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.contract.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=True,
    )
    contact_person_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            f"{SCHEMA}.contact_person.id",
            deferrable=True,
            initially="DEFERRED",
        ),
        nullable=False,
    )


class TaskType(Base):
    __tablename__ = "task_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(25), nullable=False, unique=True)


class Priority(Base):
    __tablename__ = "priority"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    priority = Column(String(25), nullable=False, unique=True)
