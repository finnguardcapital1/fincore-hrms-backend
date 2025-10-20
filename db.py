import os
from playhouse.db_url import connect
from .configs import settings

db = connect(os.getenv("DATABASE_URL", settings.DATABASE_URL))
