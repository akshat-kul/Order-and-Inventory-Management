# Navtech-Assignment

Firstly a signup-login system is added for assigning the role of admin and user to various users logging into the application.
Secondly, different endpoints are created such as 'orders', 'inventory' and 'retrieve_orders'

1) Orders endpoint is created for placing a single or multiple orders by user and orders are directly saved into the database.
2) Inventory endpoint is created in which admin can upload csv file for listing the item and price of the products in the database. If a similar product already exists, it'll update the new price of that particular item. Due to some issue I was unable to add the missing item in the table.
3) Retrieving order endpoint is created where admin can view the orders that are placed in the order of 3 months and they are returned in the json format.

Usage of Signup-Login system:
When user signups, they have to asssign a role to them that is of admin or user and if user is assigned as admin then only it can upload csv file and view the orders. So both of the endpoints are locked for admin only and they can't be viewed or used by users.

To check whether who's admin, jwt_identity is being used.

I've uploaded the postman json file as well for checking and using my endpoints.
