# Ethan Cornwill T2A2 API Application

## Documentation Requirements

Documentation for this project must be supplied as a single markdown file named README.md. This file should contain:

### R1 Explain the problem that this app will solve, and explain how this app solves or addresses the problem.

### R2 Describe the way tasks are allocated and tracked in your project.

### R3 List and explain the third-party services, packages and dependencies used in this app.

### R4 Explain the benefits and drawbacks of this app’s underlying database system.

### R5 Explain the features, purpose and functionalities of the object-relational mapping system (ORM) used in this app.

### R6 Design an entity relationship diagram (ERD) for this app’s database, and explain how the relations between the diagrammed models will aid the database design. 
- This should focus on the database design BEFORE coding has begun, eg. during the project planning or design phase.

### R7 Explain the implemented models and their relationships, including how the relationships aid the database implementation.
- This should focus on the database implementation AFTER coding has begun, eg. during the project development phase.

### R8 Explain how to use this application’s API endpoints. Each endpoint should be explained, including the following data for each endpoint:

- HTTP verb
- Path or route
- Any required body or header data
- Response

## Design Requirements

The web server must:

- Function as intended
- Store data in a persistent data storage medium (eg. a relational database)
- Appropriately validate and sanitise any data it interacts with
- Use appropriate HTTP web request verbs - following REST conventions - for various types of data manipulation 
- Cover the full range of CRUD functionality for data within the database
- The database manipulated by the web server must accurately reflect the entity relationship diagram created for the Documentation Requirements.
- The database tables or documents must be normalised
- API endpoints must be documented in your readme
- Endpoint documentation should include
  - HTTP request verbs
  - Required data where applicable 
  - Expected response data 
  - Authentication methods where applicable
 

## Code Requirements

The web server must:

* Use appropriate functionalities or libraries from the relevant programming language in its construction
* Use appropriate model methods to query the database
* Catch errors and handle them gracefully 
* Return appropriate error codes and messages to malformed requests
* Use appropriate functions or methods to sanitise & validate data
* Use D.R.Y coding principles
* All queries to the database must be commented with an explanation of how they work and the data they are intended to retrieve

