from sqlalchemy import create_engine, engine
from backend.utils import SETTINGS


async def connect_db() -> engine:
    """
    Function to return sqlalchemy engine, connected to DB

    Parameters
    ----------

    Returns
    -------
    engine : sqlalchemy.engine
    Engine connected to postgres DB
    """
    return create_engine(SETTINGS.heroku_postgres_uri, echo=False)
