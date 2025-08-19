"""fix- Renamed roles column to role

Revision ID: ab119a3c862f
Revises: 
Create Date: 2025-08-07 19:37:17.303338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab119a3c862f'
down_revision: Union[str, Sequence[str], None] = '6196e1036eee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'users', 
        'roles',      
        new_column_name='role', 
    )


def downgrade() -> None:
    op.alter_column(
        'users', 
        'role',      
        new_column_name='roles', 
    )
