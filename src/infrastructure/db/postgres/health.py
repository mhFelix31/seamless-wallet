from sqlalchemy import text
from src.application.ports.health import HealthCheck


class SQLAlchemyHealthCheck(HealthCheck):
    def __init__(self, engine):
        self.engine = engine
    
    async def is_healthy(self) -> bool:
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except Exception as ex:
            print(ex)
            return False