"""empty message

Revision ID: 0cc70702907d
Revises: b2104cf89cbd
Create Date: 2024-05-27 15:12:46.366804

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0cc70702907d'
down_revision = 'b2104cf89cbd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('image')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', mysql.VARCHAR(length=200), nullable=True))

    # ### end Alembic commands ###
