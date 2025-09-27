import pytest
from tracker.factories import TransactionFactory

@pytest.fixture
def transactions():
    import random
    return TransactionFactory.create_batch(20,amount = random.randint(0,100))