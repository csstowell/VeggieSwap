# """Script to seed database."""

# import os
# import json
# from random import choice, randint
# from faker import Faker

# import crud
# import model
# import server

# initializing Faker instance
# fake = Faker()

# os.system("dropdb vegetables")
# os.system("createdb vegetables")

# model.connect_to_db(server.app)
# model.db.create_all()

# Load vegetable data from JSON file
with open("data/vegetables.json") as f:
    vegetable_data = json.loads(f.read())

# Create vegetables, store them in list so we can use them
# to create fake messages
vegetables_in_db = []
for vegetable in vegetable_data:
    name, quantity, description = (
        vegetable["name"],
        vegetable["quantity"],
        vegetable["description"],
    )

    db_vegetable = crud.create_vegetable_listing(name, quantity, description)
    vegetables_in_db.append(db_vegetable)


# Create 10 users; each user will make 10 messages
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)

    for _ in range(10):
        random_vegetable = choice(vegetables_in_db)
        message = fake.text()
        print(message)

        crud.create_message(sender_id, message, random_vegetable)
################################ TESTS.PY #####################################################
# from unittest import TestCase
# import os
# from flask_sqlalchemy import SQLAlchemy
# import datetime

# from server import app
# import crud
# import model


class ProjectTestsHomepage(TestCase):
    """Test homepage."""

    def setUp(self):
        """Setup homepage test."""

        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn(
            b"Empower You to Better Foresee Your Financial Future", result.data)


class ProjectTestsLogInProfileAccountDetails(TestCase):
    """Test Login, create new user, and profile page."""

    def setUp(self):
        """Setup database test."""

        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = 'key'

        os.system("createdb testpb")

        model.connect_to_db(app, "postgresql:///testpb")
        model.db.create_all()
        mock_data()    # def mock_data is close to the bottom of this page

    # Database ### - like unit test

    def test_crud_user_in_database(self):
        """Test database by looking up a user by using a function defined in crud."""

        test_user_email = "johnny@john"
        test_user = crud.get_user_by_email(test_user_email)
        self.assertEqual(test_user.user_id, 1)
        self.assertEqual(test_user.email, test_user_email)

    ### Log In Page ###

    def test_successful_login(self):
        """Test login with matched email and password for successful login."""

    # future_date = datetime.date.today() + datetime.timedelta(120)

    # crud.create_entry_log(1, n, "Income", "testing1: x1", 500)
    # crud.create_entry_log(2, n, "Income", "testing2: with q20Days",
    #                       1000, future_date, datetime.timedelta(20))
    # crud.create_entry_log(3, n, "Expense", "desc-testing3", -500)


# Automate all test
if __name__ == "__main__":
    import unittest

    unittest.main()
