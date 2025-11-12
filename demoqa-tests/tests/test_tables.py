from pages.tables_page import TablesPage
from faker import Faker

fake = Faker()

def test_add_table_user(page):
    tables = TablesPage(page)
    tables.open()

    email = fake.email()
    tables.add_user(
        fake.first_name(),
        fake.last_name(),
        email,
        fake.random_int(min=18, max=60),
        fake.random_int(min=2000, max=10000),
        fake.job()
    )
    tables.verify_user(email)
