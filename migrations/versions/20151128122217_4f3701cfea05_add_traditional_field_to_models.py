"""Add traditional field to models.

Revision ID: 4f3701cfea05
Revises: 4f8982b79976
Create Date: 2015-11-28 12:22:17.701742

"""

# revision identifiers, used by Alembic.
revision = '4f3701cfea05'
down_revision = '4f8982b79976'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('author', sa.Column('intro_tr', sa.Text(), nullable=True))
    op.add_column('author', sa.Column('name_tr', sa.String(length=50), nullable=True))
    op.add_column('collection', sa.Column('desc_tr', sa.Text(), nullable=True))
    op.add_column('collection', sa.Column('full_name_tr', sa.String(length=200), nullable=True))
    op.add_column('collection', sa.Column('name_tr', sa.String(length=200), nullable=True))
    op.alter_column('collection', 'kind_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               existing_server_default=sa.text(u"'0'"))
    op.create_unique_constraint(None, 'collection', ['name_tr'])
    op.create_unique_constraint(None, 'collection', ['full_name_tr'])
    op.add_column('collection_kind', sa.Column('name_tr', sa.String(length=50), nullable=True))
    op.create_unique_constraint(None, 'collection_kind', ['name_tr'])
    op.alter_column('collection_work', 'collection_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               existing_server_default=sa.text(u"'0'"))
    op.alter_column('collection_work', 'work_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True,
               existing_server_default=sa.text(u"'0'"))
    op.add_column('dynasty', sa.Column('intro_tr', sa.Text(), nullable=True))
    op.add_column('dynasty', sa.Column('name_tr', sa.String(length=50), nullable=True))
    op.add_column('quote', sa.Column('quote_tr', sa.Text(), nullable=True))
    op.add_column('work', sa.Column('content_tr', sa.Text(), nullable=True))
    op.add_column('work', sa.Column('foreword_tr', sa.Text(), nullable=True))
    op.add_column('work', sa.Column('intro_tr', sa.Text(), nullable=True))
    op.add_column('work', sa.Column('mobile_content_tr', sa.Text(), nullable=True))
    op.add_column('work', sa.Column('mobile_title_tr', sa.String(length=50), nullable=True))
    op.add_column('work', sa.Column('title_suffix_tr', sa.String(length=50), nullable=True))
    op.add_column('work', sa.Column('title_tr', sa.String(length=50), nullable=True))
    op.add_column('work_type', sa.Column('cn_tr', sa.String(length=50), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('work_type', 'cn_tr')
    op.drop_column('work', 'title_tr')
    op.drop_column('work', 'title_suffix_tr')
    op.drop_column('work', 'mobile_title_tr')
    op.drop_column('work', 'mobile_content_tr')
    op.drop_column('work', 'intro_tr')
    op.drop_column('work', 'foreword_tr')
    op.drop_column('work', 'content_tr')
    op.drop_column('quote', 'quote_tr')
    op.drop_column('dynasty', 'name_tr')
    op.drop_column('dynasty', 'intro_tr')
    op.alter_column('collection_work', 'work_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               existing_server_default=sa.text(u"'0'"))
    op.alter_column('collection_work', 'collection_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               existing_server_default=sa.text(u"'0'"))
    op.drop_constraint(None, 'collection_kind', type_='unique')
    op.drop_column('collection_kind', 'name_tr')
    op.drop_constraint(None, 'collection', type_='unique')
    op.drop_constraint(None, 'collection', type_='unique')
    op.alter_column('collection', 'kind_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False,
               existing_server_default=sa.text(u"'0'"))
    op.drop_column('collection', 'name_tr')
    op.drop_column('collection', 'full_name_tr')
    op.drop_column('collection', 'desc_tr')
    op.drop_column('author', 'name_tr')
    op.drop_column('author', 'intro_tr')
    ### end Alembic commands ###
