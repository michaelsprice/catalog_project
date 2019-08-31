from flask import Flask, render_template, url_for, request, redirect
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

# Show a category items
@app.route('/category/<int:categories_id>/items')
@app.route('/category/<int:categories_id>/')
def showCategoryItem(categories_id):
   categoryToShow = session.query(Categories).filter_by(id=categories_id).one()
   itemsToShow = session.query(Items).filter_by(category_id = categories_id)
   return render_template('showCategoryItem.html', category = categoryToShow, items = itemsToShow)

# Create a new category item
@app.route('/category/<int:categories_id>/item/new', methods=['GET','POST'])
def createCategoryItem(categories_id):
   theCategory = session.query(Categories).filter_by(id=categories_id).one()
   if request.method == 'POST':
      newItem = theCategory(name = request.form['name'], description = request.form['description'], 
         categories_id = theCategory.id)
      session.add(newItem)
      session.commit()
      return redirect(url_for('showCategoryItem', categories_id = categories_id))
   else:
      return render_template('createCategoryItem.html', categories_id = categories_id) 

# Create a new category item BACKUP
# @app.route('/category/<int:categories_id>/item/new', methods=['GET','POST'])
# def createCategoryItem(categories_id):
#   category = session.query(Categories).filter_by(id=categories_id).one()
#   items = session.query(Items)
#   return render_template('createCategoryItem.html', category = category, items = items)

# Edit a category item
@app.route('/category/<int:categories_id>/<int:item_id>/edit')
def editCategoryItem(categories_id, item_id):
   category = session.query(Categories).filter_by(id=categories_id).one()
   editedItem = session.query(Items).filter_by(id = item_id).one()
   return render_template('editCategoryItem.html', category = category, items = editedItem)

# Delete a category item
@app.route('/category/<int:categories_id>/<int:item_id>/delete')
def deleteCategoryItem(categories_id, item_id):
   category = session.query(Categories).filter_by(id=categories_id).one()
   itemToDelete = session.query(Items).filter_by(id=item_id).one()
   return render_template('deleteCategoryItem.html', category = category, items = itemToDelete)

# Show an item and description
@app.route('/category/<int:categories_id>/<int:item_id>/description')
def showCategoryItemDescription(categories_id, item_id):
   category = session.query(Categories).filter_by(id=categories_id).one()
   itemToDelete = session.query(Items).filter_by(id=item_id).one()
   return render_template('showCategoryItemDescription.html', category = category, items = itemToDelete)



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
