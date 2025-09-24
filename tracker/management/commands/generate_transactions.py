import random
from faker import Faker
from django.core.management.base import BaseCommand
from tracker.models import User, Transaction, Category

class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        self.stdout.write("Starting transaction generation...")

        income_categories = [
            'Salary',
            'Freelance',
            'Business',
            'Investment',
            'Rental Income',
            'Bonus',
            'Gift',
            'Refund',
            'Side Hustle',
            'Dividend'
        ]
        expense_categories = [
            'Food & Dining',
            'Transportation',
            'Groceries',
            'Shopping',
            'Entertainment',
            'Bills & Utilities',
            'Healthcare',
            'Education',
            'Travel',
            'Insurance',
            'Home & Garden',
            'Personal Care',
            'Subscriptions',
            'Gas',
            'Rent/Mortgage',
            'Phone',
            'Internet',
            'Gym/Fitness'
        ]

        categories = income_categories + expense_categories

        self.stdout.write("Creating categories...")
        
        created_count = 0
        for category in categories:
            category_obj, created = Category.objects.get_or_create(name=category)
            if created:
                created_count += 1
                self.stdout.write(f"Created category: {category}")

        self.stdout.write(f"Categories created: {created_count}, Total: {len(categories)}")

        self.stdout.write("Getting or creating user...")
        user = User.objects.filter(username="chetry08").first()
        if not user:
            user = User.objects.create_superuser(username="chetry08", email="test@example.com", password="test")
            self.stdout.write("Created user: chetry08")
        else:
            self.stdout.write("Using existing user: chetry08")

        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]

        self.stdout.write("Creating 20 transactions...")
        for i in range(20):
            Transaction.objects.create(
                category=random.choice(categories),
                user=user,
                amount=random.uniform(1, 5000),
                date=fake.date_between(start_date='-1y', end_date='today'),
                type=random.choice(types)
            )
            if (i + 1) % 5 == 0:
                self.stdout.write(f"Created {i + 1} transactions...")

        self.stdout.write(self.style.SUCCESS("Successfully generated 20 transactions!"))




