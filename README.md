# CODING-ASSIGNMENT
created a simple API that will work with Users, Clients and Companies
This API serves as a backend for managing users, clients, and companies. It provides endpoints to perform CRUD (Create, Read, Update, Delete) operations on users, clients, and companies.

Endpoints
1)Users
/users: Retrieve a list of all users or search for users by username.
/users/<user_id>: Update a user's information.


2)Clients
/clients: Create a new client or retrieve a list of all clients.
/clients/<client_id>: Update a client's information.
/clients/search: Search for clients by user ID or company name.


3)Companies
/companies: Retrieve a list of all companies or search for companies by employee range.


USAGES
Use the appropriate HTTP methods (GET, POST, PUT, PATCH) along with the endpoints to interact with the API.
Send requests with JSON payloads for creating or updating resources.
Retrieve data from the API by accessing the endpoints with appropriate parameters.



Authentication
This API does not currently implement authentication. Ensure that it is deployed securely and only accessible to authorized users.


Error Handling
The API returns appropriate HTTP status codes and error messages for invalid requests or server errors.
