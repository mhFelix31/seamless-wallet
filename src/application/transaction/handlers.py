class CreateTransactionHandler:
    def __init__(self, repository, async_unit_of_work):
        self.repo = repository
        self.uow = async_unit_of_work

    async def handle(self, db_txn):
        async with self.uow:
            await self.repo.save(db_txn)
