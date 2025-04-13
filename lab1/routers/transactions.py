from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from typing import Optional, List
from models.models import Budget, Account, CategoryType, Transaction, TransactionDefault
from auth.connection import get_session
from datetime import datetime
from auth.auth import bearer_scheme

router = APIRouter(prefix="/transactions", tags=["Transactions"], dependencies=[Depends(bearer_scheme)])

@router.get("/", response_model=List[Transaction])
def list_transactions(session: Session = Depends(get_session)):
    return session.exec(select(Transaction)).all()

@router.post("/", response_model=Transaction)
def create_transaction(transaction: TransactionDefault, session: Session = Depends(get_session)):
    account = session.get(Account, transaction.account_id)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # проверка бюджета
    budget = session.exec(
        select(Budget)
        .where(Budget.user_id == account.user_id)
        .where(Budget.category == transaction.category)
        .where(Budget.month == transaction.date.month)
        .where(Budget.year == transaction.date.year)
    ).first()

    warning: Optional[str] = None

    if budget and transaction.category != CategoryType.salary:
        start_of_month = datetime(transaction.date.year, transaction.date.month, 1)
        end_of_month = (
            datetime(transaction.date.year, transaction.date.month + 1, 1)
            if transaction.date.month < 12
            else datetime(transaction.date.year + 1, 1, 1)
        )

        # все предыдущие транзакции за этот месяц
        total_spent = session.exec(
            select(Transaction)
            .where(Transaction.account_id == account.id)
            .where(Transaction.category == transaction.category)
            .where(Transaction.date >= start_of_month)
            .where(Transaction.date < end_of_month)
        ).all()

        spent_sum = sum(t.amount for t in total_spent)

        if spent_sum + transaction.amount > budget.limit:
            warning = (
                f"Budget exceeded: {(spent_sum + transaction.amount):.2f} > limit {budget.limit:.2f}"
            )

    # обновляем баланс 
    if transaction.category == CategoryType.salary:
        account.balance += transaction.amount
    else:
        if account.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        account.balance -= transaction.amount

    session.add(account) 


    transaction = Transaction.model_validate(transaction)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)

    return {
        "transaction": transaction,
        "warning": warning
    }
