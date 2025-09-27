import factory
from datetime import datetime
from tracker.models import User, Transaction, Category

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "user%d" % n)
    
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)
        
    name = factory.Iterator(
        ["Bills","Salary","Rent","Food","Subscriptions","Side Hustle"]
    )
    
class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
        
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    amount = 5 
    date = factory.Faker(
        "date_between",
        start_date = datetime(year=2023,month=1,day=1).date(),
        end_date = datetime.now().date()
    )
    type = factory.Iterator(
        [
            x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES
        ]
    )