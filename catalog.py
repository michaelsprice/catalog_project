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
   #category = session.query(Categories)
   #items = session.query(Items)
   return "Page for new category"
   #return render_template('categories.html', category = category, items = items)

# Edit a category
@app.route('/category/<int:categories_id>/edit')
def editCategory():
   #category = session.query(Categories)
   #items = session.query(Items)
   return "Page for edit a category"
   #return render_template('categories.html', category = category, items = items)


# Delete a category


# Show a category item


# Create a new category item


# Edit a category item


# Delete a category item



if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)