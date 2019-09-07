Welcome to the Item Catalog web application.

This app displays the items in the catalog along with the categories of the items. The categories are created in the backend by the admin using the database script. If a user choses to login ,the user can add , modify or delete items from the catalog. The modification or deletion is permitted only if the user is the creator of the item.
This application is built using Python 2.7, Flask, Google oauth2 , SQLAlchemy and SQLite database.

The different screens presented in the application are as follows:

Homepage
This page lists all the Categories in the system. It also lists the latest ten items that were added along with their category. For the logged in user, it lets the user add a new item.

Login / Logout
On the homepage , there is an option for the user to sign in to the application.
In this application, google oauth2 api end point integration has been added to enable the user to sign in using their gmail account.

Items
This page will list all the items for a given category. It also lets the user navigate back to the Homepage.

Item description.
When the user clicks an item, its description is displayed. There is also an option for the logged in user to either edit or delete the item.

Edit Item
When the user clicks the edit item from the Item description page, this page will be displayed if the user is the creator of the item. Here the user has the option to either update the item or cancel the changes.

Delete Item
When the user clicks the delete item from the Item description page, this page will be displayed if the user is the creator of the item. Here the user has the option to either delete the item or cancel the changes.

Error Page
This page is displayed when an unauthorized user is trying to edit or delete an item which has not been created by the user.

JSON endpoints
/category/JSON - lists all categories
http://localhost:5000/category/JSON
/category/<int:category_id>/items/JSON - list all items in a category
http://localhost:5000/category/1/items/JSON
/category/<int:category_id>/<int:item_id>/description/JSON - displays description of an item in a category
http://localhost:5000/category/1/1/description/JSON

How to run the application

Execute the following steps:
i)  python database_setup.py
ii) python lotsofcatalog.py
iii) python project.py
iv) Load the application in the browser by going to the
    url http://localhost:5000/
