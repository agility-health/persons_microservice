"""empty message

Revision ID: ec8a13c5ada9
Revises: 9c0170622b8a
Create Date: 2022-04-01 15:28:03.985860

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ec8a13c5ada9'
down_revision = '9c0170622b8a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phone')
    op.add_column('patient', sa.Column('phone', sa.String(length=14), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('patient', 'phone')
    op.create_table('phone',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('country_code', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('area_code', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('number', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('patient_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.id'], name='phone_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###