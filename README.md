# Item Catalog Project 
The Item Catalog Project will display a list of categories in a database. Clicking on a category will show you a list of items associated to that Category. Clicking on the item will show the item and the description. From there, you can edit or delete the item.

## Installation
1. Clone the reposity git@github.com:michaelsprice/catalog_project.git by running `git clone git@github.com:michaelsprice/catalog_project.git` in your terminal window. 

2. You will need to make sure you have a virtual machine installed and running (for info see [this page](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)). The following is using VirtualBox and Vagrant. 
-Once you have VirtualBox and Vagrant installed, make sure vagrant is running (inside of your terminal window, run `vagrant up` then `vagrant ssh`).

## Database Setup
1. Inside your terminal window, run `cd /vagrant/catalog`.
2. Run `python database_setup.py` [this will create your database].
3. Run `python populate_database.py` [this will populate your database with data].
4. Run `python application.py` [this will start the application on port 8000].
5. In your browser window, navigate to `http://localhost:8000` to get started.

## Usage
- When you are on http://localhost:8000, you are presented with the categories in the database. From here, you can login (with a google account) in order to add, edit or delete category items.
- Click on a category to see a list of items associated to that Category. 
- Click on the item to see the item and the description. From there, you can edit or delete the item (requires you to be logged in via google).
