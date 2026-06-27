from src.application.dtos import ExternalTransferDTO, MoneyDTO, TransactionResponseDTO, TransferDTO
from src.domain.currency.entities import Currency
from src.domain.currency.repository import CurrencyRepository
from src.domain.shared.money import Money
from src.domain.transaction.entities import Transaction
from src.domain.transaction.repository import TransactionRepository
from src.domain.wallet.entities import Wallet, WalletSnapshot
from src.domain.wallet.repository import WalletRepository, WalletSnapshotRepository

class InsuficientFundsException(Exception):
    pass

class TransferHandler():
    def __init__(
            self,
            currency_repo: CurrencyRepository,
            wallet_repo: WalletRepository,
            snapshot_repo: WalletSnapshotRepository,
            transaction_repo: TransactionRepository,
        ):
        self.currency_repo=currency_repo
        self.wallet_repo=wallet_repo
        self.snapshot_repo=snapshot_repo
        self.transaction_repo=transaction_repo
    
    def transfer(
            self,
            source_id: str,
            transfer: TransferDTO,
        ):
        transaction = self.create_transaction(
            source_id=source_id,
            receiver_id=transfer.receiver_id,
            currency_code=transfer.currency_code,
            value=transfer.value
        )
        balance = self.get_post_transaction_balance(transfer.currency_code, source_id)

        return TransactionResponseDTO(
            sender=transaction.source.label,
            receiver=transaction.receiver.label,
            amount=MoneyDTO(currency_code=transaction.amount.currency.code, value=transaction.amount.value),
            balance=MoneyDTO(balance.currency.code, balance.value),
            uuid=transaction.uuid,
            timestamp=transaction.timestamp
        )

    def withdraw(
            self,
            transfer: ExternalTransferDTO,
            bank_id: str,
        ):
        transaction = self.create_transaction(
            source_id=transfer.wallet_id,
            receiver_id=bank_id,
            currency_code=transfer.currency_code,
            value=transfer.value
        )
        balance = self.get_post_transaction_balance(transfer.currency_code, transfer.wallet_id)

        return TransactionResponseDTO(
            sender=transaction.source.label,
            receiver=transaction.receiver.label,
            amount=MoneyDTO(currency_code=transaction.amount.currency.code, value=transaction.amount.value),
            balance=MoneyDTO(balance.currency.code, balance.value),
            uuid=transaction.uuid,
            timestamp=transaction.timestamp
        )
    
    def deposit(
            self,
            transfer: ExternalTransferDTO,
            bank_id: str,
        ):
        transaction = self.create_transaction(
            source_id=transfer.wallet_id,
            receiver_id=bank_id,
            currency_code=transfer.currency_code,
            value=transfer.value
        )
        balance = self.get_post_transaction_balance(transfer.currency_code, transfer.wallet_id)

        return TransactionResponseDTO(
            sender=transaction.source.label,
            receiver=transaction.receiver.label,
            amount=MoneyDTO(currency_code=transaction.amount.currency.code, value=transaction.amount.value),
            balance=MoneyDTO(balance.currency.code, balance.value),
            uuid=transaction.uuid,
            timestamp=transaction.timestamp
        )

    def get_post_transaction_balance(self, currency_code, wallet_id) -> Money:
        currency = get_currency_from_code(
                currency_code=currency_code,
                currency_repo=self.currency_repo
            )
        balance = get_wallet_cur_balance(
                snapshot_repo=self.snapshot_repo,
                transaction_repo=self.transaction_repo,
                wallet_id=wallet_id
        )
        return balance[currency]


    def create_transaction(
            self,
            source_id: str,
            receiver_id: str,
            currency_code:str,
            value:int
        ) -> Transaction:
        currency = self.currency_repo.get_by_code(currency_code)
        amount = Money(currency=currency, value=value)

        source_wallet: Wallet = self.wallet_repo.get_by_id(source_id)
        if not source_wallet.is_external_managed:
            cur_balance = get_wallet_cur_balance(snapshot_repo=self.snapshot_repo, wallet_id=source_id)
            balance_after_transaction = cur_balance.get(currency, Money(currency=currency, value=0)) - amount
            if balance_after_transaction < 0:
                raise InsuficientFundsException()

        receiver_wallet: Wallet = self.wallet_repo.get_by_id(receiver_id)
        
        transaction = Transaction(
            source=source_wallet,
            receiver=receiver_wallet,
            amount=amount
        )
        saved_transaction = self.transaction_repo.save(txn=transaction)
        return saved_transaction


def get_currency_from_code(currency_repo:CurrencyRepository, currency_code:str)-> Currency:
    currency = currency_repo.get_by_code(currency_code)
    return currency


def get_wallet_cur_balance(
        snapshot_repo: WalletSnapshotRepository,
        transaction_repo: TransactionRepository,
        wallet_id: str
    ) -> dict[Currency, Money]:
    latest_snapshot:WalletSnapshot = snapshot_repo.get_latest_by_wallet_id(wallet_id=wallet_id)
    latest_balance:dict[Currency, Money] = latest_snapshot.balance

    missing_transactions:list[Transaction] = transaction_repo.get_all_after_snapshot(latest_snapshot)

    for transaction in missing_transactions:
        cur = transaction.amount.currency
        if cur not in latest_balance:
            latest_balance[cur] = Money(cur, 0)
        latest_balance[cur] += transaction.amount

    return latest_balance
