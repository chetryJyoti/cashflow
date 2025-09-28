import pytest
from tracker.factories import TransactionFactory, UserFactory

@pytest.fixture
def transactions():
    import random
    return TransactionFactory.create_batch(20,amount = random.randint(0,100))

@pytest.fixture
def user_transactions():
    user = UserFactory()
    return TransactionFactory.create_batch(20,user=user)