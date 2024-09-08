# Ethan Cornwill T2A2 API Application

# SocialAPI

## Problem and Solution

**Problem:** The difficulty for developers to create social media features within their applications.

**Solution:** My API provides a comprehensive set of endpoints and functionalities to enable developers to easily integrate social media features into their applications. This includes user profiles, post creation and management, commenting and liking, following and unfollowing, and messaging.

## Task Allocation and Tracking

* **Project Management Tool:** Utilise a tool like Trello or Asana to create boards, tasks, and assign them to team members.
* **Task Breakdown:** Break down the project into smaller, manageable tasks, such as designing the database, implementing API endpoints, and testing.
* **Timelines:** Set deadlines for each task and track progress to ensure timely completion.
* **Collaboration:** Use tools like GitHub or GitLab for version control and collaboration among team members.

## Third-Party Services, Packages, and Dependencies

* **Flask:** Python web framework for building APIs.
* **SQLAlchemy:** ORM for interacting with the database.
* **JWT:** For token-based authentication and authorisation.
* **Marshmallow:** For data validation and serialisation.
* **PostgreSQL:** Relational database for storing user data, posts, comments, and other information.

## Database System Benefits and Drawbacks

**Benefits of PostgreSQL:**

* **Open-source:** Free to use and distribute.
* **Robust:** Reliable and scalable for handling large datasets.
* **Rich features:** Supports advanced features like full-text search, JSONB data type, and spatial data.
* **Active community:** Strong community support and resources available.

**Drawbacks of PostgreSQL:**

* **Learning curve:** Can be more complex to learn and configure compared to simpler databases.
* **Performance:** May require optimisation for very large datasets or high-traffic applications.

## R5: ORM Features and Functionalities

**SQLAlchemy:**

* **Object-relational mapping:** Maps Python classes to database tables.
* **Querying:** Provides a high-level API for querying the database using Python syntax.
* **Relationships:** Handles relationships between objects (e.g., one-to-many, many-to-many).
* **Migrations:** Automatically generates database schema changes based on model modifications.
* **Declarative syntax:** Uses a declarative style for defining models and relationships.

## R6: Entity Relationship Diagram (ERD)

![ERD](./docs/erd.png)

The ERD illustrates the relationships between entities in the database:

* **User:** A user has many posts, comments, and likes.
* **Post:** A post belongs to a user and can have many comments and likes.
* **Comment:** A comment belongs to a user and a post.
* **Like:** A like belongs to a user and a post.
* **Follow:** A follow relationship connects two users.

These relationships help ensure data integrity and consistency in the database.

## R7: Implemented Models and Relationships

**Models:**

* **User:** `id`, `username`, `email`, `password_hash`
* **Post:** `id`, `user_id`, `content`, `created_at`, `updated_at`
* **Comment:** `id`, `user_id`, `post_id`, `content`, `created_at`, `updated_at`
* **Like:** `id`, `user_id`, `post_id`, `created_at`
* **Follow:** `id`, `follower_id`, `followed_id`

**Relationships:**

* A `User` has many `Posts`, `Comments`, and `Likes`.
* A `Post` belongs to a `User` and can have many `Comments` and `Likes`.
* A `Comment` belongs to a `User` and a `Post`.
* A `Like` belongs to a `User` and a `Post`.
* A `Follow` connects two `Users` (follower and followed).

**How Relationships Aid Implementation:**

* **Data integrity:** Relationships ensure data consistency and prevent inconsistencies. For example, a `Comment` must always belong to a `User` and a `Post`.
* **Efficient querying:** Relationships allow for efficient querying of related data. For example, to get all comments on a post, we can use the `post.comments` relationship.
* **Cascade operations:** Relationships can be used to cascade operations. For example, if a `User` is deleted, their associated `Posts`, `Comments`, and `Likes` can be automatically deleted.

## R8: API Endpoints

### **Users**

* **GET /users** - Get a list of all users.
* **GET /users/<user_id>** - Get a specific user.
* **POST /users** - Create a new user.
* **PUT /users/<user_id>** - Update a user.
* **DELETE /users/<user_id>** - Delete a user.

### **Posts**

* **GET /posts** - Get a list of all posts.
* **GET /posts/<post_id>** - Get a specific post.
* **POST /posts** - Create a new post.
* **PUT /posts/<post_id>** - Update a post.
* **DELETE /posts/<post_id>** - Delete a post.

### **Comments**

* **GET /posts/<post_id>/comments** - Get comments for a specific post.
* **POST /posts/<post_id>/comments** - Create a new comment on a post.
* **PUT /comments/<comment_id>** - Update a comment.
* **DELETE /comments/<comment_id>** - Delete a comment.

### **Likes**

* **POST /posts/<post_id>/likes** - Like a post.
* **DELETE /posts/<post_id>/likes** - Unlike a post.

### **Follows**

* **POST /users/<user_id>/follow** - Follow a user.
* **DELETE /users/<user_id>/follow** - Unfollow a user.

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
