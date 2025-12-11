import uuid

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql as pg


class Base(orm.DeclarativeBase):
    pass


user_permissions = sa.Table(
    'user_permissions',
    Base.metadata,
    sa.Column('user_id', sa.ForeignKey('users.id'), primary_key=True),
    sa.Column('permission_id', sa.ForeignKey(
        'permissions.id'), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=False)
    surname: orm.Mapped[str] = orm.mapped_column(
        sa.String(255), nullable=False)
    patronymic: orm.Mapped[str] = orm.mapped_column(
        sa.String(255), nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(255), nullable=False, unique=True)
    password: orm.Mapped[str] = orm.mapped_column(
        sa.String(255), nullable=False)
    is_active: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=True
    )

    permissions: orm.Mapped[list['Permission']] = orm.relationship(
        secondary=user_permissions, back_populates='users', lazy='selectin')


class Permission(Base):
    __tablename__ = 'permissions'

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(255), nullable=False, unique=True)
    description: orm.Mapped[str | None] = orm.mapped_column(
        sa.Text, nullable=True)
    create: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False)
    read: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False)
    update: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False)
    delete: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, nullable=False, default=False)
    business_entity: orm.Mapped[str] = orm.mapped_column(
        sa.String(255), nullable=False)

    users: orm.Mapped[list['User']] = orm.relationship(
        secondary=user_permissions, back_populates='permissions', lazy='selectin')


class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'

    jti: orm.Mapped[uuid.UUID] = orm.mapped_column(
        pg.UUID(as_uuid=True), primary_key=True)
