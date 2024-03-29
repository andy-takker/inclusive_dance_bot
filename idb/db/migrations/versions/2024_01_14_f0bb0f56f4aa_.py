"""empty message

Revision ID: f0bb0f56f4aa
Revises:
Create Date: 2024-01-14 10:49:52.849965

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f0bb0f56f4aa"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "submenu",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("weight", sa.Integer(), nullable=False),
        sa.Column("button_text", sa.String(length=64), nullable=False),
        sa.Column("message", sa.String(length=4000), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__submenu")),
    )
    op.create_table(
        "url",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("value", sa.String(length=2048), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__url")),
        sa.UniqueConstraint("slug", name=op.f("uq__url__slug")),
    )
    op.create_table(
        "user_type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__user_type")),
    )
    op.create_index(op.f("ix__user_type__name"), "user_type", ["name"], unique=True)
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=256), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("profile", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__users")),
    )
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("text", sa.String(length=4096), nullable=False),
        sa.Column("is_viewed", sa.Boolean(), nullable=False),
        sa.Column("viewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_answered", sa.Boolean(), nullable=False),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk__feedback__user_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__feedback")),
    )
    op.create_index(
        op.f("ix__feedback__user_id"), "feedback", ["user_id"], unique=False
    )
    op.create_table(
        "mailing",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.BigInteger(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("content", sa.String(length=3072), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"], ["users.id"], name=op.f("fk__mailing__author_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__mailing")),
    )
    op.create_index(
        op.f("ix__mailing__author_id"), "mailing", ["author_id"], unique=False
    )
    op.create_index(
        op.f("ix__mailing__scheduled_at"), "mailing", ["scheduled_at"], unique=False
    )
    op.create_table(
        "user_type_user",
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("user_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk__user_type_user__user_id__users")
        ),
        sa.ForeignKeyConstraint(
            ["user_type_id"],
            ["user_type.id"],
            name=op.f("fk__user_type_user__user_type_id__user_type"),
        ),
        sa.PrimaryKeyConstraint(
            "user_id", "user_type_id", name=op.f("pk__user_type_user")
        ),
    )
    op.create_table(
        "answer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("feedback_id", sa.Integer(), nullable=False),
        sa.Column("from_user_id", sa.BigInteger(), nullable=False),
        sa.Column("to_user_id", sa.BigInteger(), nullable=False),
        sa.Column("text", sa.String(length=4096), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["feedback_id"],
            ["feedback.id"],
            name=op.f("fk__answer__feedback_id__feedback"),
        ),
        sa.ForeignKeyConstraint(
            ["from_user_id"], ["users.id"], name=op.f("fk__answer__from_user_id__users")
        ),
        sa.ForeignKeyConstraint(
            ["to_user_id"], ["users.id"], name=op.f("fk__answer__to_user_id__users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__answer")),
    )
    op.create_index(
        op.f("ix__answer__feedback_id"), "answer", ["feedback_id"], unique=False
    )
    op.create_index(
        op.f("ix__answer__from_user_id"), "answer", ["from_user_id"], unique=False
    )
    op.create_index(
        op.f("ix__answer__to_user_id"), "answer", ["to_user_id"], unique=False
    )
    op.create_table(
        "mailing_user_type",
        sa.Column("mailing_id", sa.Integer(), nullable=False),
        sa.Column("user_type_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["mailing_id"],
            ["mailing.id"],
            name=op.f("fk__mailing_user_type__mailing_id__mailing"),
        ),
        sa.ForeignKeyConstraint(
            ["user_type_id"],
            ["user_type.id"],
            name=op.f("fk__mailing_user_type__user_type_id__user_type"),
        ),
        sa.PrimaryKeyConstraint(
            "mailing_id", "user_type_id", name=op.f("pk__mailing_user_type")
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("mailing_user_type")
    op.drop_index(op.f("ix__answer__to_user_id"), table_name="answer")
    op.drop_index(op.f("ix__answer__from_user_id"), table_name="answer")
    op.drop_index(op.f("ix__answer__feedback_id"), table_name="answer")
    op.drop_table("answer")
    op.drop_table("user_type_user")
    op.drop_index(op.f("ix__mailing__scheduled_at"), table_name="mailing")
    op.drop_index(op.f("ix__mailing__author_id"), table_name="mailing")
    op.drop_table("mailing")
    op.drop_index(op.f("ix__feedback__user_id"), table_name="feedback")
    op.drop_table("feedback")
    op.drop_table("users")
    op.drop_index(op.f("ix__user_type__name"), table_name="user_type")
    op.drop_table("user_type")
    op.drop_table("url")
    op.drop_table("submenu")
    # ### end Alembic commands ###
