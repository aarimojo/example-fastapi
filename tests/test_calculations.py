import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()
@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("a, b, c", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_calculations(a, b, c):
    print('Test add function')
    assert add(a, b) == c

def test_substract():
    print('Test add function')
    sum = subtract(5, 3)
    assert sum == 2

def test_multiply():
    print('Test add function')
    sum = multiply(5, 3)
    assert sum == 15

def test_divide():
    print('Test add function')
    sum = divide(35, 5)
    assert sum == 7

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(25)
    assert bank_account.balance == 25

def test_bank_deposit(bank_account):
    bank_account.deposit(25)
    assert bank_account.balance == 75

def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert bank_account.balance == 55


@pytest.mark.parametrize("deposit, withdraw, balance", [
    (200, 100, 100),
    (20, 20, 0)
])
def test_bank_transaction(zero_bank_account, deposit, withdraw, balance):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == balance

def test_insuficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(150)