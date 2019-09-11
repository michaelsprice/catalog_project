from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Items, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(
    id=1,
    name="Cory Chenault",
    email="CoryJChenault@jourrapide.com",
    picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Soccer 1
category1 = Categories(user_id=1, name="Soccer")
session.add(category1)
session.commit()

categoryItem1 = Items(
    user_id=1,
    name="Shinguards",
    description="They protect your shins, duh.",
    category=category1)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    user_id=1,
    name="Soccer Ball",
    description="The ball that you kick during the game.",
    category=category1)
session.add(categoryItem2)
session.commit()

# Basketball 2
category2 = Categories(user_id=1, name="Basketball")
session.add(category2)
session.commit()

categoryItem3 = Items(
    user_id=1,
    name="Air Pump",
    description="Pump up the ball.",
    category=category2)
session.add(categoryItem3)
session.commit()

categoryItem4 = Items(
    user_id=1,
    name="Basketball",
    description="The ball that you play with during the game of basketball.",
    category=category2)
session.add(categoryItem4)
session.commit()

# Baseball 3
category3 = Categories(user_id=1, name="Baseball")
session.add(category3)
session.commit()

categoryItem5 = Items(
    user_id=1,
    name="Bat",
    description="Hit the ball.",
    category=category3)
session.add(categoryItem5)
session.commit()

categoryItem6 = Items(
    user_id=1,
    name="Baseball",
    description="The ball that you play with during the game of baseball.",
    category=category3)
session.add(categoryItem6)
session.commit()

# Frisbee 4
category4 = Categories(user_id=1, name="Frisbee")
session.add(category4)
session.commit()

categoryItem7 = Items(
    user_id=1,
    name="Cones",
    description="Used to mark off the field.",
    category=category4)
session.add(categoryItem7)
session.commit()

categoryItem8 = Items(
    user_id=1,
    name="Frisbee",
    description="The thing you throw.",
    category=category4)
session.add(categoryItem8)
session.commit()

# Snowboarding 5
category5 = Categories(user_id=1, name="Snowboarding")
session.add(category5)
session.commit()

categoryItem9 = Items(
    user_id=1,
    name="Goggles",
    description="They protect your eyes.",
    category=category5)
session.add(categoryItem9)
session.commit()

categoryItem10 = Items(
    user_id=1,
    name="Snowboard",
    description="Strap in your feet and go down the hill.",
    category=category5)
session.add(categoryItem10)
session.commit()

# Rock Climbing 6
category6 = Categories(user_id=1, name="Rock Climbing")
session.add(category6)
session.commit()

categoryItem11 = Items(
    user_id=1,
    name="Climbing shoes",
    description="Helps you get up the rock.",
    category=category6)
session.add(categoryItem11)
session.commit()

categoryItem12 = Items(
    user_id=1,
    name="Carabiner",
    description="Keeps you connected to the rope",
    category=category6)
session.add(categoryItem12)
session.commit()

# Foosball 7
category7 = Categories(user_id=1, name="Foosball")
session.add(category7)
session.commit()

categoryItem13 = Items(
    user_id=1,
    name="Foosball table",
    description="How you play the game.",
    category=category7)
session.add(categoryItem13)
session.commit()

categoryItem14 = Items(
    user_id=1,
    name="Foosball Ball",
    description="Ball used during the game.",
    category=category7)
session.add(categoryItem14)
session.commit()

# Skating 8
category8 = Categories(user_id=1, name="Skating")
session.add(category8)
session.commit()

categoryItem15 = Items(
    user_id=1,
    name="Skates",
    description="Put em on your feet.",
    category=category8)
session.add(categoryItem15)
session.commit()

categoryItem16 = Items(
    user_id=1,
    name="Skate strings",
    description="Keeps them tight around your feet.",
    category=category8)
session.add(categoryItem16)
session.commit()

# Hockey 9
category9 = Categories(user_id=1, name="Hockey")
session.add(category9)
session.commit()

categoryItem17 = Items(
    user_id=1,
    name="Puck",
    description="What you use during the game.",
    category=category9)
session.add(categoryItem17)
session.commit()

categoryItem18 = Items(
    user_id=1,
    name="Hockey Stick",
    description="Used to pass the puck around.",
    category=category9)
session.add(categoryItem18)
session.commit()

print ("added categories & items!")
