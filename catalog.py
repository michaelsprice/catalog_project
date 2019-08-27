from flask import Flask, render_template
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Items

engine = create_engine('sqlite:///catalog.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all categories
@app.route('/')
@app.route('/categories')
def showCategories():
   category = session.query(Categories)
   items = session.query(Items)
   return render_template('categories.html', category = category, items = items)

# Create a new category
@app.route('/category/new')
def newCategory():
   category = session.query(Categories)
   return render_template('newCategory.html', category = category)

# Edit a category
@app.route('/category/<int:categories_id>/edit')
def editCategory(categories_id):
   category = session.query(Categories)
   return render_template('editCategory.html', category = category)

# Delete a category
@app.route('/category/<int:categories_id>/delete')
def deleteCategory(categories_id):
   category = session.query(Categories)
   return render_template('deleteCategory.html', category = category)

# Show a category item
@app.route('/category/<int:categories_id>/item')
@app.route('/category/<int:categories_id>/')
def showCategoryItem(categories_id):
   category = session.query(Categories)
   items = session.query(Items)
   return render_template('showCategoryItem.html', category = category, items = items)

# Create a new category item
@app.route('/category/<int:categories_id>/item/new')
def createCategoryItem(categories_id):
   category = session.query(Categories)
   items = session.query(Items)
   return render_template('createCategoryItem.html', category = category, items = items)

# Edit a category item
@app.route('/category/<int:categories_id>/item/<int:item_id>/edit')
def editCategoryItem(categories_id, item_id):
   category = session.query(Categories)
   items = session.query(Items)
   return render_template('editCategoryItem.html', category = category, items = items)

# Delete a category item
@app.route('/category/<int:categories_id>/item/<int:item_id>/delete')
def deleteCategoryItem(categories_id, item_id):
   category = session.query(Categories)
   items = session.query(Items)
   return render_template('deleteCategoryItem.html', category = category, items = items)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)