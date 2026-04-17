from sqlalchemy.ext.asyncio import AsyncSession

class AsyncUnitOfWork:
    """
    Database Transaction Manager
    Aggregates DB Transactions, if they failed or an error occures on application, all db_txns should be rolledback. Either all persist, or None
    *(This transaction is related to DB only, it isn't related to Domain's Transaction)*
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self):
        # begin a DB transaction explicitly
        self._db_txns = await self.session.begin()

        return self

    async def __aexit__(self, exception_type, exception, traceback):
        if exception_type:
            await self._db_txns.rollback()
        else:
            await self._db_txns.commit()