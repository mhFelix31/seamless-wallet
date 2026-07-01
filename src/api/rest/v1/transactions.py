from fastapi import APIRouter, Depends

from src.api.dependencies import (
    get_currency_repository,
    get_snapshot_repository,
    get_source_id,
    get_transaction_repository,
    get_wallet_repository,
)
from src.application.dtos import (
    ExternalTransferDTO,
    TransactionResponseDTO,
    TransferDTO,
)
from src.application.use_cases import TransferHandler
from src.domain.currency.repository import CurrencyRepository
from src.domain.transaction.repository import TransactionRepository
from src.domain.wallet.repository import WalletRepository, WalletSnapshotRepository

router = APIRouter()


# Deposit from outside
@router.post("/deposit", response_model=TransactionResponseDTO)
async def deposit(
    transfer_dto: ExternalTransferDTO,
    bank_id: str = Depends(get_source_id),
    currency_repo: CurrencyRepository = Depends(get_currency_repository),
    wallet_repo: WalletRepository = Depends(get_wallet_repository),
    snapshot_repo: WalletSnapshotRepository = Depends(get_snapshot_repository),
    transaction_repo: TransactionRepository = Depends(get_transaction_repository),
):
    handler = TransferHandler(
        currency_repo=currency_repo,
        wallet_repo=wallet_repo,
        snapshot_repo=snapshot_repo,
        transaction_repo=transaction_repo,
    )
    return handler.deposit(transfer=transfer_dto, bank_id=bank_id)


# Withdraw to outside
@router.post("/withdraw")
async def withdraw(
    transfer_dto: ExternalTransferDTO,
    bank_id: str = Depends(get_source_id),
    currency_repo: CurrencyRepository = Depends(get_currency_repository),
    wallet_repo: WalletRepository = Depends(get_wallet_repository),
    snapshot_repo: WalletSnapshotRepository = Depends(get_snapshot_repository),
    transaction_repo: TransactionRepository = Depends(get_transaction_repository),
):
    handler = TransferHandler(
        currency_repo=currency_repo,
        wallet_repo=wallet_repo,
        snapshot_repo=snapshot_repo,
        transaction_repo=transaction_repo,
    )
    return handler.withdraw(transfer=transfer_dto, bank_id=bank_id)


# Transfer to internal account
@router.post("/transfer")
async def transfer(
    transfer_dto: TransferDTO,
    source_id: str = Depends(get_source_id),
    currency_repo: CurrencyRepository = Depends(get_currency_repository),
    wallet_repo: WalletRepository = Depends(get_wallet_repository),
    snapshot_repo: WalletSnapshotRepository = Depends(get_snapshot_repository),
    transaction_repo: TransactionRepository = Depends(get_transaction_repository),
):
    handler = TransferHandler(
        currency_repo=currency_repo,
        wallet_repo=wallet_repo,
        snapshot_repo=snapshot_repo,
        transaction_repo=transaction_repo,
    )
    return handler.transfer(source_id=source_id, transfer=transfer_dto)
