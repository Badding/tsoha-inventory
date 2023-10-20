# tsoha-inventory 

This is an inventory management app designed for the tsoha course. With this app users can manage and track an organization's inventory through this application. The app interacts with the database, making the desired changes and searches.

## Features

- Sign in as a user.
- Admin can add and remove users and list all users.
- Add products.
- Create new sales; customers are added to the database if they are new.
- List orders and products.
- Provide detailed information about orders and products.
- Search for products by name.

## Installation

First step is to clone the repository to your computer

```bash
  git clone https://github.com/Badding/tsoha-inventory
  cd tsoha-inventory
```
Activate the Python environment and install dependencies from requirements.txt:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create database tables
```
psql < schema.sql
```

The app requires an .env file in the project's root directory. In this file, add your database URL and secret_key:
```
DATABASE_URL=
SECRET_KEY=
```

## Usage/Examples

To run the app
```
flask run
```

In the login screen, there is a button to fill the database with test products, sales, users, and customers.

In the app, the admin can create new users and is the only one who can see the Admin tab.

Default users for testing purposes:
```
admin/admin
manager/manager
sales/sales

```