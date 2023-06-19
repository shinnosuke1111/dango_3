"""empty message

Revision ID: 3e79710fe01f
Revises: 
Create Date: 2023-06-19 10:41:51.639423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e79710fe01f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('ruby', sa.String(length=64), nullable=False),
    sa.Column('dept', sa.String(length=64), nullable=False),
    sa.Column('group_name', sa.String(length=64), nullable=False),
    sa.Column('year', sa.String(length=4), nullable=False),
    sa.PrimaryKeyConstraint('account_id')
    )
    op.create_table('basic_information',
    sa.Column('basic_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('birth_month', sa.String(length=2), nullable=True),
    sa.Column('birth_day', sa.String(length=2), nullable=True),
    sa.Column('team', sa.String(length=64), nullable=True),
    sa.Column('hobby', sa.String(length=64), nullable=True),
    sa.Column('word', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.account_id'], ),
    sa.PrimaryKeyConstraint('basic_id')
    )
    op.create_table('message',
    sa.Column('tweet_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.account_id'], ),
    sa.PrimaryKeyConstraint('tweet_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    op.drop_table('basic_information')
    op.drop_table('accounts')
    # ### end Alembic commands ###
