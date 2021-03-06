"""empty message

Revision ID: ebea8005f6f8
Revises: 
Create Date: 2018-09-30 17:53:42.614749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebea8005f6f8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bk',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bkname', sa.String(length=20), nullable=False),
    sa.Column('bknum', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('frontuser',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('telephone', sa.String(length=11), nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('_password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('realname', sa.String(length=50), nullable=True),
    sa.Column('avatar', sa.String(length=100), nullable=True),
    sa.Column('signature', sa.String(length=100), nullable=True),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'SECRET', 'UNKNOW', name='genderenum'), nullable=True),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('telephone'),
    sa.UniqueConstraint('username')
    )
    op.create_table('lbt',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bannerName', sa.String(length=20), nullable=False),
    sa.Column('imglink', sa.String(length=200), nullable=False),
    sa.Column('link', sa.String(length=200), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('imglink'),
    sa.UniqueConstraint('link')
    )
    op.create_table('roel',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('roelname', sa.String(length=20), nullable=False),
    sa.Column('desc', sa.String(length=200), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('roelname')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('_password', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=False),
    sa.Column('join_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('cms_role_user',
    sa.Column('cms_role_id', sa.Integer(), nullable=False),
    sa.Column('cms_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cms_role_id'], ['roel.id'], ),
    sa.ForeignKeyConstraint(['cms_user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('cms_role_id', 'cms_user_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cms_role_user')
    op.drop_table('user')
    op.drop_table('roel')
    op.drop_table('lbt')
    op.drop_table('frontuser')
    op.drop_table('bk')
    # ### end Alembic commands ###
