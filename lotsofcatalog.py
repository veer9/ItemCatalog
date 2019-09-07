from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, Item, User

engine = create_engine('sqlite:///catalogueitemswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

#Menu for UrbanBurger
category1 = Category(name = "Soccer")

session.add(category1)
session.commit()

item1 = Item(name = "Ball", description = "A football is a ball inflated with air that is used to play one of the various sports known as football.",  category = category1,user_id=1)

session.add(item1)
session.commit()


item2 = Item(name = "Shoes", description = "Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football. Those designed for grass pitches have studs on the outsole to aid grip.",  category = category1,user_id=1 )

session.add(item2)
session.commit()


item3 = Item(name = "Socks", description = "These soccer socks are made up of nylon and spandex, which keeps them lightweight and snug on your feet. They feature Adidas' ClimaLite technology which absorbs moisture, while also having a ClimaCool mesh which promotes breathability and gives your feet a very cool and dry run.",  category = category1, user_id=1)

session.add(item3)
session.commit()


item4 = Item(name = "Shin Guard", description = "A shin guard is a thick piece of material that you wear inside your socks to protect the lower part of your leg when you are playing a game such as soccer.",  category = category1, user_id=1)

session.add(item4)
session.commit()

User2 = User(name="Yash Mehta", email="yash_mehta017@yahoo.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')



#Menu for Super Stir Fry
category1 = Category(name = "BasketBall")

session.add(category1)
session.commit()

item1 = Item(name = "Ball", description = "A basketball is a spherical ball used in basketball games. During the game, the ball must be bounced continuously (dribbling), thrown through the air to other players (passing) or thrown towards the basket (shooting).",  category = category1, user_id=2)

session.add(item1)
session.commit()


item2 = Item(name = "Shoes", description = "basketball shoes need to be able handle multi-directional footwork, provide shock absorption and grip. Laces also hold the tongue of the shoe in place which prevents friction of the laces over the tendons on top of the foot and ankle.",  category = category1, user_id=2)

session.add(item2)
session.commit()


item3 = Item(name = "Socks", description = "TA pair of socks is a pair of socks is a pair of socks. It's like a basketball shoe now, the socks have strategically cushioned zones for the left and right foot to provide support and comfort.",  category = category1, user_id=2)

session.add(item3)
session.commit()


item4 = Item(name = "Shorts", description = "Originally, basketball was played in any type of athletic attire, ranging from track suits to football uniforms.In 1984, Michael Jordan asked for longer shorts and helped popularize the move away from tight, short shorts toward the longer, baggier shorts worn by basketball players today.",  category = category1, user_id=2)

session.add(item4)
session.commit()





#Menu for Panda Garden
category1 = Category(name = "Baseball")

session.add(category1)
session.commit()

item1 = Item(name = "Ball", description = "A baseball is a ball used in the sport of the same name. The ball features a rubber or cork center, wrapped in yarn, and covered, in the words of the Official Baseball Rules with two strips of white horsehide or cowhide, tightly stitched together.",  category = category1, user_id=2)

session.add(item1)
session.commit()


item2 = Item(name = "Shoes", description = "A baseball shoe, as defined by the Dickson Baseball Dictionary (3rd Ed), is a special type of shoe designed and worn by baseball players that features cleats for traction and a full set of laces for support.",  category = category1, user_id=2)

session.add(item2)
session.commit()


item3 = Item(name = "Socks", description = "These socks are made up of nylon and spandex, which keeps them lightweight and snug on your feet. They feature Adidas ClimaLite technology which absorbs moisture, while also having a ClimaCool mesh which promotes breathability and gives your feet a very cool and dry run.",  category = category1, user_id=2)

session.add(item3)
session.commit()


item4 = Item(name = "Shin Guard", description = "A shin guard is a thick piece of material that you wear inside your socks to protect the lower part of your leg when you are playing a game such as baseball.",  category = category1, user_id=2)

session.add(item4)
session.commit()




#Menu for Tony's Bistro
category1 = Category(name = "Frisbee ")

session.add(category1)
session.commit()

item1 = Item(name = "Disc", description = "A frisbee (pronounced FRIZ-bee, origin of the term dates to 1957, also called a flying disc or simply a disc) is a gliding toy or sporting item that is generally plastic and roughly 8 to 10 inches (20 to 25 cm) in diameter with a pronounced lip.",  category = category1, user_id=2)

session.add(item1)
session.commit()


item2 = Item(name = "Shoes", description = "Frisbee cleats or shoes in North America, are an item of footwear worn when playing frisbee. Those designed for grass pitches have studs on the outsole to aid grip.",  category = category1, user_id=2)

session.add(item2)
session.commit()


item3 = Item(name = "Socks", description = "These socks are made up of spandex, which keeps them lightweight and snug on your feet. They feature ClimaLite technology which absorbs moisture, while also having a ClimaCool mesh which promotes breathability and gives your feet a very cool and dry run.",  category = category1, user_id=2)

session.add(item3)
session.commit()


item4 = Item(name = "Shin Guard", description = "A shin guard is a thick piece of material that you wear inside your socks to protect the lower part of your leg when you are playing a game such as frisbee.",  category = category1, user_id=2)

session.add(item4)
session.commit()





#Menu for Andala's
category1 = Category(name = "Snowboarding")

session.add(category1)
session.commit()

item1 = Item(name = "Snowboard", description = "Snowboards are boards where both feet are secured to the same board, which are wider than skis, with the ability to glide on snow. Snowboards widths are between 6 and 12 inches or 15 to 30 centimeters.",  category = category1, user_id=2)

session.add(item1)
session.commit()


item2 = Item(name = "Boots", description = "Snowboard boots are designed to conform to your feet specifically, so owning your own pair will be far more comfortable. Snowboard boots come in regular shoe sizes, but sizing can vary among different companies.",  category = category1, user_id=2)

session.add(item2)
session.commit()


item3 = Item(name = "Socks", description = "Snowboard socks typically employ wool, merino wool, or synthetic materials that pull moisture and sweat away from your feet, and wet feet means cold feet.This is why thin snowboard socks are preferred by many riders.",  category = category1, user_id=2)

session.add(item3)
session.commit()


item4 = Item(name = "Jacket", description = "Snowboard jackets are waterproof, to keep you dry, and breathable, to let out the moisture (sweat) that your body produces when riding.",  category = category1, user_id=2)

session.add(item4)
session.commit()





#Menu for Auntie Ann's
category1 = Category(name = "Rock Climbing' ")

session.add(category1)
session.commit()

item1 = Item(name = "rope", description = "Dynamic ropes are designed to stretch to absorb the impact of a falling climber. Static ropes stretch very little, making them very efficient in situations like lowering an injured climber, ascending a rope, or hauling a load up.",  category = category1, user_id=2)

session.add(item1)
session.commit()


item2 = Item(name = "Shoes", description = " climbing shoe is a specialized type of footwear designed for rock climbing. Typical climbing shoes have a close fit, little if any padding, and a smooth, sticky rubber sole with an extended rubber rand. Unsuited to walking and hiking, climbing shoes are typically donned at the base of a climb.",  category = category1, user_id=2)

session.add(item2)
session.commit()


item3 = Item(name = "webbing and cords", description = "Modern webbing or tape is made of nylon or Spectra/Dyneema, or a combination of the two. Climbing-specific nylon webbing is generally tubular webbing, that is, it is a tube of nylon pressed flat.",  category = category1,user_id=2)

session.add(item3)
session.commit()


item4 = Item(name = "helmet", description = "The climbing helmet is a piece of safety equipment that primarily protects the skull against falling debris (such as rocks or dropped pieces of protection) and impact forces during a fall.",  category = category1, user_id=2)

session.add(item4)
session.commit()




#Menu for Cocina Y Amor
category1 = Category(name = "Skating ")

session.add(category1)
session.commit()

item1 = Item(name = "skates", description = "Roller skates are shoes, or bindings that fit onto shoes, that are worn to enable the wearer to roll along on wheels. The first roller skate was effectively an ice skate with wheels replacing the blade.",  category = category1,user_id=2)

session.add(item1)
session.commit()


item2 = Item(name = "Helmet", description = "The climbing helmet is a piece of safety equipment that primarily protects the skull against impact forces during a fall.",  category = category1, user_id=2)

session.add(item2)
session.commit()


item3 = Item(name = "Socks", description = "These soccer socks are made up of nylon and spandex, which keeps them lightweight and snug on your feet. They feature Adidas' ClimaLite technology which absorbs moisture, while also having a ClimaCool mesh which promotes breathability and gives your feet a very cool and dry run.",  category = category1, user_id=2)

session.add(item3)
session.commit()


item4 = Item(name = "Shin Guard", description = "A shin guard is a thick piece of material that you wear inside your socks to protect the lower part of your leg when you are roller skating.",  category = category1, user_id=2)

session.add(item4)
session.commit()



print "added menu items!"
