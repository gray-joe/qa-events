"""create github data table

Creates a new table to store unprocessed GitHub action data
for historical / debugging purposes.

Revision ID: 68a712d8d862
Revises: 
Create Date: 2023-10-10 11:35:35.910825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68a712d8d862'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'github',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('timestamp', sa.DateTime),
        sa.Column('data', sa.JSON)
    )


def downgrade() -> None:
    op.drop_table('github_raw_data')
