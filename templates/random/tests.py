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
            b"", result.data)


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


# Automate all test
if __name__ == "__main__":
    import unittest

    unittest.main()
