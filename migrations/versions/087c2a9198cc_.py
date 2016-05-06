"""empty message

Revision ID: 087c2a9198cc
Revises: e54b620851e1
Create Date: 2016-05-05 23:53:08.526756

"""

# revision identifiers, used by Alembic.
revision = '087c2a9198cc'
down_revision = 'e54b620851e1'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('author', 'is_author',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.add_column('comment', sa.Column('comment_author', sa.String(length=100), nullable=True))
    op.drop_column('comment', 'author')
    op.alter_column('post', 'live',
               existing_type=mysql.TINYINT(display_width=1),
               type_=sa.Boolean(),
               existing_nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'live',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    op.add_column('comment', sa.Column('author', mysql.VARCHAR(length=100), nullable=True))
    op.drop_column('comment', 'comment_author')
    op.alter_column('author', 'is_author',
               existing_type=sa.Boolean(),
               type_=mysql.TINYINT(display_width=1),
               existing_nullable=True)
    ### end Alembic commands ###
