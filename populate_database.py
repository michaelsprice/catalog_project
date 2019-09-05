from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Items

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Soccer 1
category1 = Categories(name="Soccer")
session.add(category1)
session.commit()

categoryItem1 = Items(
    name="Shinguards",
    description="They protect your shins, duh.",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Soccer Ball",
    description="The ball that you kick during the game.",
    category=category1)
session.add(categoryItem2)
session.commit()

# Basketball 2
category2 = Categories(name="Basketball")
session.add(category2)
session.commit()

categoryItem3 = Items(
    name="Air Pump",
    description="Pump up the ball.",
    category=category2)
session.add(categoryItem3)
session.commit()

categoryItem4 = Items(
    name="Basketball",
    description="The ball that you play with during the game of basketball.",
    category=category2)
session.add(categoryItem4)
session.commit()

# Baseball 3
category3 = Categories(name="Baseball")
session.add(category3)
session.commit()

categoryItem5 = Items(
    name="Bat",
    description="Hit the ball.",
    category=category3)
session.add(categoryItem5)
session.commit()

categoryItem6 = Items(
    name="Baseball",
    description="The ball that you play with during the game of baseball.",
    category=category3)
session.add(categoryItem6)
session.commit()

# Frisbee 4
category4 = Categories(name="Frisbee")
session.add(category4)
session.commit()

categoryItem7 = Items(
    name="Cones",
    description="Used to mark off the field.",
    category=category4)
session.add(categoryItem7)
session.commit()

categoryItem8 = Items(
    name="Frisbee",
    description="The think you throw.",
    category=category4)
session.add(categoryItem8)
session.commit()

# Snowboarding 5
category5 = Categories(name="Snowboarding")
session.add(category5)
session.commit()

categoryItem9 = Items(
    name="Goggles",
    description="They protect your eyes.",
    category=category5)
session.add(categoryItem9)
session.commit()

categoryItem10 = Items(
    name="Snowboard",
    description="Strap in your feet and go down the hill.",
    category=category5)
session.add(categoryItem10)
session.commit()

# Rock Climbing 6
category6 = Categories(name="Rock Climbing")
session.add(category6)
session.commit()

categoryItem11 = Items(
    name="Climbing shoes",
    description="Helps you get up the rock.",
    category=category6)
session.add(categoryItem11)
session.commit()

categoryItem12 = Items(
    name="Carabiner",
    description="Keeps you connected to the rope",
    category=category6)
session.add(categoryItem12)
session.commit()

# Foosball 7
category7 = Categories(name="Foosball")
session.add(category7)
session.commit()

categoryItem13 = Items(
    name="Foosball table",
    description="How you play the game.",
    category=category7)
session.add(categoryItem13)
session.commit()

categoryItem14 = Items(
    name="Foosball Ball",
    description="Ball used during the game.",
    category=category7)
session.add(categoryItem14)
session.commit()

# Skating 8
category8 = Categories(name="Skating")
session.add(category8)
session.commit()

categoryItem15 = Items(
    name="Skates",
    description="Put em on your feet.",
    category=category8)
session.add(categoryItem15)
session.commit()

categoryItem16 = Items(
    name="Skate strings",
    description="Keeps them tight around your feet.",
    category=category8)
session.add(categoryItem16)
session.commit()

# Hockey 9
category9 = Categories(name="Hockey")
session.add(category9)
session.commit()

categoryItem17 = Items(
    name="Puck",
    description="What you use during the game.",
    category=category9)
session.add(categoryItem17)
session.commit()

categoryItem18 = Items(
    name="Hockey Stick",
    description="Used to pass the puck around.",
    category=category9)
session.add(categoryItem18)
session.commit()

print ("added categories & items!")
