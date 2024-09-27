# Ethan Cornwill T2A2 API Application

# SocialAPI

## Problem and Solution

**Problem:** The difficulty for developers to create social media features within their applications.

**Solution:** My API provides a comprehensive set of endpoints and functionalities to enable developers to easily integrate social media features into their applications. This includes user profiles, post creation and management, commenting and liking, following and unfollowing, and messaging.

## Task Allocation and Tracking

### Project Planning

This project utilised GitHub Projects to manage the project.
Between September 8th and 15th, the project was created, and initial planning was completed.

While working on the project I realised that some features that I was initially planning to create would be far too complex and outside of the scope of the project, as such, I decided instead to focus more on other parts of the project to enhance their functionality.

- [GitHub Projects](https://github.com/finneh4249/t2a2-api-application/projects/1)

![timeline](./docs/planning/timeline.png)
![main_board](./docs/planning/main_board.png)

### Milestones

![milestone1](./docs/planning/milestone1.png)
![milstones](./docs/planning/milestones.png)

### Milestone 1: Planning

![issue_2](./docs/planning/issue_2.png)

### Milestone 2: User Management

![issue_3](./docs/planning/issue_3.png)

### Milestone 3: Post Management

![issue_4](./docs/planning/issue_4.png)
![issue_12](./docs/planning/issue_12.png)

### Milestone 4: Comments and Notifications

![issue_5](./docs/planning/issue_5.png)
![issue_6](./docs/planning/issue_6.png)

### Milestone 5: Following and Friends

![issue_7](./docs/planning/issue_7.png)

### Milestone 6: Search and Analytics (Not Implemented)

![issue_8](./docs/planning/issue_8.png)
![issue_9](./docs/planning/issue_9.png)

### Milestone 7: Testing and Deployment

![issue_10](./docs/planning/issue_10.png)
![issue_10_2](./docs/planning/issue_10_2.png)
![issue_11](./docs/planning/issue_11.png)
![issue_13](./docs/planning/issue_13.png)

## Third-Party Services, Packages, and Dependencies

- **Flask:** Python web framework for building APIs.
- **SQLAlchemy:** ORM for interacting with the database.
- **JWT:** For token-based authentication and authorisation.
- **Marshmallow:** For data validation and serialisation.
- **PostgreSQL:** Relational database for storing user data, posts, comments, and other information.

## Database System Benefits and Drawbacks

### Benefits of PostgreSQL:

- **Open-source:** Free to use and distribute.
- **Robust:** Reliable and scalable for handling large datasets.
- **Rich features:** Supports advanced features like full-text search, JSONB data type, and spatial data.
- **Active community:** Strong community support and resources available.

### Drawbacks of PostgreSQL:

- **Learning curve:** Can be more complex to learn and configure compared to simpler databases.
- **Performance:** May require optimisation for very large datasets or high-traffic applications.

## ORM Features and Functionalities

### SQLAlchemy:

- **Object-relational mapping:** Maps Python classes to database tables.
- **Querying:** Provides a high-level API for querying the database using Python syntax.
- **Relationships:** Handles relationships between objects (e.g., one-to-many, many-to-many).
- **Migrations:** Automatically generates database schema changes based on model modifications.
- **Declarative syntax:** Uses a declarative style for defining models and relationships.

## Entity Relationship Diagram (ERD)

### Intial ERD

![ERD](./docs/init_erd.png)

The ERD illustrates the draft of the relationships between entities in the database. During the development process, the ERD was modified to reflect changes in the entities, and relationships.

### Final ERD

![ERD](./docs/final_erd.png)

## Implemented Models and Relationships

### Models:

- **User:** `id`, `username`, `email`, `password_hash`, `bio`, `is_admin`, `is_confirmed`, `confirmed_on`
- **Post:** `id`, `user_id`, `content`, `created_at`, `updated_at`
- **Comment:** `id`, `user_id`, `post_id`, `content`, `created_at`, `updated_at`
- **Like:** `id`, `user_id`, `post_id`, `created_at`
- **Follow:** `id`, `follower_id`, `followed_id`

### Relationships:

- A `User` has many `Posts`, `Comments`, and `Likes`.
- A `Post` belongs to a `User` and can have many `Comments` and `Likes`.
- A `Comment` belongs to a `User` and a `Post`.
- A `Like` belongs to a `User` and a `Post`.
- A `Follow` connects two `Users` (follower and followed).

### How Relationships Aid Implementation:

- **Data integrity:** Relationships ensure data consistency and prevent inconsistencies. For example, a `Comment` must always belong to a `User` and a `Post`.
- **Efficient querying:** Relationships allow for efficient querying of related data. For example, to get all comments on a post, we can use the `post.comments` relationship.
- **Cascade operations:** Relationships can be used to cascade operations. For example, if a `User` is deleted, their associated `Posts`, `Comments`, and `Likes` can be automatically deleted.

## API Endpoints

### **Users**

- **GET /users**

  - **HTTP Method:** GET
  - **Request Parameters:**
    - `page` (optional): Page number for pagination
    - `per_page` (optional): Number of users per page
  - **Authorization**: JWT token required in the `Authorization` header.
  - **Response Format:** JSON array of user objects (id, username, email, profile_picture, bio)
  - **Example Request:**
    ```
    curl -H "Authorization: Bearer <your_token>" http://localhost:5000/users
    ```
  - **Example Response:**
    ```json
    [
      {
        "id": 1,
        "username": "user1",
        "email": "user1@example.com",
        "profile_picture": "https://example.com/profile1.jpg",
        "bio": "This is user 1."
      },
      {
        "id": 2,
        "username": "user2",
        "email": "user2@example.com",
        "profile_picture": "https://example.com/profile2.jpg",
        "bio": "This is user 2."
      }
    ]
    ```

- **GET /users/{user_id}/profile**

  - **HTTP Method:** GET
  - **Request Parameters:**
    - `user_id`: ID of the user to retrieve

  * **Authorization:** JWT token required in the `Authorization` header

  - **Response Format:** JSON object representing the user
  - **Example Request:**
    ```
    curl -H "Authorization: Bearer <your_token>" http://localhost:5000/users/1
    ```
  - **Example Response:**
    ```json
    {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "profile_picture": "https://example.com/profile1.jpg",
      "bio": "This is user 1."
    }
    ```

- **PUT/PATCH /users/{user_id}/profile**

  - **HTTP Method:** PUT / PATCH
  - **Request Parameters:**
    - `user_id`: ID of the user to update
    - `username` (optional)
    - `email` (optional)
    - `bio` (optional)
  - **Response Format:** JSON object representing the updated user
  - **Example Request:**
    ```
    curl -X PUT http://localhost:5000/users/1 -d '{"username": "updateduser"}'
    ```
  - **Example Response:**
    ```json
    {
      "id": 1,
      "username": "updateduser",
      "email": "user1@example.com",
      "profile_picture": "https://example.com/profile1.jpg",
      "bio": "This is user 1."
    }
    ```

- **GET /users/{user_id}/timeline**

  - **HTTP Method:** GET
  - **Request Parameters:**
    - `user_id`: ID of the user to retrieve
  - **Authorization**: JWT token required in the `Authorization` header
  - **Response Format:** JSON array of post objects (id, user_id, content, created_at, updated_at, likes_count, comments_count)
  - **Example Request:**
    ```
    curl -H "Authorization: Bearer <your_token>" http://localhost:5000/users/1/timeline
    ```
  - **Example Response:**

    ```json
    [
      {
        "id": 1,
        "user_id": 1,
        "content": "Hello, World!",
        "created_at": "2022-01-01T00:00:00",
        "updated_at": "2022-01-01T00:00:00",
        "likes_count": 0,
        "comments_count": 0
      }
    ]
    ```

### **Authentication**

- **POST /auth/login**
  - **HTTP Method:** POST
  - **Request Parameters:**
    - `username`: The username of the user
    - `password`: The password of the userq
  - **Response Format:** JSON object representing the logged-in user
  - **Example Request:**
  ```bash
  curl -X POST http://localhost:5000/auth/login -d '{"username": "john_doe", "password": "password123"}'
  ```
  - **Example Response:**
  ```json
  {
    "message": "User john_doe logged in successfully",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzE2Nzk2MCwianRpIjoiZWQ3N2ZmNzQtNTk5Mi00ZjFmLWIyNTQtODA4N2JiMDg2Mjg3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNzI3MTY3OTYwLCJjc3JmIjoiNmFjMGM0M2EtYTZlMy00ZmI2LTg0MjgtOGEwYTkwOWYzMjBkIiwiZXhwIjoxNzI3MTY4ODYwfQ.TVAA-Up3g6MQUFPsYlQZZ23vBUcYsQTNwID2McvxR7U"
  }
  ```
- **POST /auth/register**

  - **HTTP Method:** POST
  - **Request Parameters:**
    - `username`: Username of the new user
    - `email` Email address of the new user
    - `password` Password of the new user
    - `bio` (optional) Bio of the new user
  - **Response Format:** JSON object representing the newly created user
  - **Example Request:**
    ```
    curl -X POST http://localhost:5000/auth/register -d '{"username": "newuser", "email": "newuser@example.com", "password": "password123"}'
    ```
  - **Example Response:**
    ```json
    {
  "message": "User created successfully",
  "user": {
    "id": 3,
    "username": "newuser",
    "email": "newuser@example.com"
  },
  "confirmation_url": "http://localhost:5555/auth/confirm/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzQxNTEzOCwianRpIjoiN2I4YzdhYjgtYjNiZS00YzMxLWJjZjQtODdkZTJjNzBkZjVmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NSwibmJmIjoxNzI3NDE1MTM4LCJjc3JmIjoiMTI4ZDMyYzItNDc5Ni00MTYxLTk2ZGEtODAzYmZkZmMxMjQzIiwiZXhwIjoxNzI3NDE2MDM4fQ.RDPX_RIAJ7MoM3F103Q8cYS_8v_6SNMbaw9c3GI_9yY"
}
    ```

- **POST /auth/confirm/{token}**
  - **HTTP Method:** POST
  - **Request Parameters:**
    - `token`: Token to confirm the user's email address
  - **Response Format:** No response body
  - **Example Request:**
  ```bash
  curl -X POST http://localhost:5000/auth/confirm/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzQxNTEzOCwianRpIjoiN2I4YzdhYjgtYjNiZS00YzMxLWJjZjQtODdkZTJjNzBkZjVmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NSwibmJmIjoxNzI3NDE1MTM4LCJjc3JmIjoiMTI4ZDMyYzItNDc5Ni00MTYxLTk2ZGEtODAzYmZkZmMxMjQzIiwiZXhwIjoxNzI3NDE2MDM4fQ.RDPX_RIAJ7MoM3F103Q8cYS_8v_6SNMbaw9c3GI_9yY
  ```
  - **Example Response:**
  ```json
  {
    "message": "Email confirmed successfully"
  }
  ```
  - 
- **GET /auth/forgot-password**
  - **HTTP Method:** GET
  - **Request Parameters:**
    - `?user_id`: ID of the user to reset the password
  - **Response Format:** No response body
  - **Example Request:**
  ```bash
  curl -X GET http://localhost:5000/auth/forgot-password?user_id=1
  ```
  - **Example Response:**
   ```json
   {
     "message": "Password reset link created. Normally this would be sent to your email. For the purposes of this assignment, the link will be displayed here.",
     "reset_url": "http://localhost:5000/auth/reset-password/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzQxNTEzOCwianRpIjoiN2I4YzdhYjgtYjNiZS00YzMxLWJjZjQtODdkZTJjNzBkZjVmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NSwibmJmIjoxNzI3NDE1MTM4LCJjc3JmIjoiMTI4ZDMyYzItNDc5Ni00MTYxLTk2ZGEtODAzYmZkZmMxMjQzIiwiZXhwIjoxNzI3NDE2MDM4fQ.RDPX_RIAJ7MoM3F103Q8cYS_8v_6SNMbaw9c3GI_9yY"
   }
   ```
- **PUT/PATCH /auth/reset-password/{token}**
  - **HTTP Method:** PUT/PATCH
  - **Request Parameters:**
    - `token`: (In URL) Token to reset the user's password
    - `password`: New password for the user.
  - **Example Request:**
```bash
curl -X http://localhost:5000/auth/reset-password/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyNzQxNTEzOCwianRpIjoiN2I4YzdhYjgtYjNiZS00YzMxLWJjZjQtODdkZTJjNzBkZjVmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NSwibmJmIjoxNzI3NDE1MTM4LCJjc3JmIjoiMTI4ZDMyYzItNDc5Ni00MTYxLTk2ZGEtODAzYmZkZmMxMjQzIiwiZXhwIjoxNzI3NDE2MDM4fQ.RDPX_RIAJ7MoM3F103Q8cYS_8v_6SNMbaw9c3GI_9yY
```
  - **Example Response:**
  ```json
  {
    "message": "Password reset successful",
    "user":{
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "bio": "I like trainZ",
      "is_admin": false,
      "is_confirmed": true,
      "created_at": "2022-02-22T20:30:00.000000",
    }
  }
  ```
- **PUT/PATCH /auth/change-password**
  - **HTTP Method:** PUT/PATCH
  - **Request Parameters:**
    - `old_password`: Old password for the user.
    - `new_password`: New password for the user.
  - **Authorization**: JWT token required in the `Authorization` header
  - **Example Request:**
  ```bash
  curl -X http://localhost:5000/auth/change-password -H "Authorization: Bearer <your_token>" -d '{"old_password": "old_password", "new_password": "new_password"}'
  ```
  - **Example Response:**
  ```json
  {
    "message": "Password changed successfully",
    "user":{
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "bio": "I like trainZ",
      "is_admin": false,
      "is_confirmed": true,
      "created_at": "2022-02-22T20:30:00.000000",
    }
  }
  ```
-
- **DELETE /auth/unregister**

  - **HTTP Method:** DELETE
  - **Request Parameters:**
    - `user_id`: ID of the user to delete
  - **Authorization**: JWT token required in the `Authorization` header
  - **Response Format:** No response body
  - **Example Request:**
    ```
    curl -X DELETE http://localhost:5000/users/1 -H "Authorization: Bearer <your_token>"
    ```

### **Posts**

- **GET /posts**

  - **HTTP Method:** GET
  - **Request Parameters:**
    - `page` (optional): Page number for pagination
    - `per_page` (optional): Number of posts per page
  - **Authorization**: JWT token required in the `Authorization` header, `Administration` permissions are also required to access this endpoint.
  - **Response Format:** JSON array of post objects (id, user_id, content, created_at, updated_at, likes_count, comments_count)
  - **Example Request:**
    ```
    curl http://localhost:5000/posts -H "Authorization: Bearer <your_token>"
    ```
  - **Example Response:**
    ```json
    [
      {
        "id": 1,
        "user_id": 1,
        "content": "This is a post.",
        "created_at": "2023-12-31T23:59:59Z",
        "updated_at": "2023-12-31T23:59:59Z",
        "likes_count": 0,
        "comments_count": 0
      },
      {
        "id": 2,
        "user_id": 2,
        "content": "Another post.",
        "created_at": "2023-12-31T23:59:58Z",
        "updated_at": "2023-12-31T23:59:58Z",
        "likes_count": 1,
        "comments_count": 2
      }
    ]
    ```

- **GET /posts/{post_id}**

  - **HTTP Method:** GET
  - **Request Parameters:**
    - `post_id`: ID of the post to retrieve
  - **Authorization:** JWT token required in the `Authorization` header
  - **Requires Administrator Permissions**: Yes
  - **Response Format:** JSON object representing the post
  - **Example Request:**
    ```
    curl http://localhost:5000/posts/1 -H "Authorization: Bearer <your_token>"
    ```
  - **Example Response:**
    ```json
    {
      "id": 1,
      "user_id": 1,
      "content": "This is a post.",
      "created_at": "2023-12-31T23:59:59Z",
      "updated_at": "2023-12-31T23:59:59Z",
      "likes_count": 0,
      "comments_count": 0
    }
    ```

- **POST /posts**

  - **HTTP Method:** POST
  - **Request Parameters:**
    - `content`
  - **Authorization**: JWT token required in the `Authorization` header
  - **Response Format:** JSON object representing the newly created post
  - **Example Request:**
    ```
    curl -X POST http://localhost:5000/posts -H "Authorization: Bearer <your_token>" -d '{"content": "This is a new post."}'
    ```
  - **Example Response:**
    ```json
    {
      "id": 3,
      "user_id": 1,
      "content": "This is a new post.",
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "likes_count": 0,
      "comments_count": 0
    }
    ```

- **PUT / PATCH /posts/{post_id}**

  - **HTTP Method:** PUT / PATCH
  - **Request Parameters:**
    - `post_id`: ID of the post to update
    - `content`
  - **Response Format:** JSON object representing the updated post
  - **Example Request:**
    ```
    curl -X PUT http://localhost:5000/posts/1 -H "Authorization: Bearer <your_token>" -d '{"content": "Updated post content."}'
    ```
  - **Example Response:**
    ```json
    {
      "id": 1,
      "user_id": 1,
      "content": "Updated post content.",
      "created_at": "2023-12-31T23:59:59Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "likes_count": 0,
      "comments_count": 0
    }
    ```

- **DELETE /posts/{post_id}**

  - **HTTP Method:** DELETE
  - **Request Parameters:**
    - `post_id`: ID of the post to delete
  - **Response Format:** No response body
  - **Example Request:**
    ```bash
    curl -X DELETE http://localhost:5000/posts/1 -H "Authorization: Bearer <your_token>"
    ```
### **Feed**

- **GET /feed**
  - **HTTP Method:** GET
  - **Request Parameters:**
    - `?page`: (Optional) Page number of the feed
    - `?per_page`: (Optional) Number of posts per page
  - **Authorization**: JWT token required in the `Authorization` header
  - **Example Request:**
```bash
curl http://localhost:5000/feed -H "Authorization: Bearer <your_token>"
```
  - **Example Response:**
```json
  [
  {
    "id": 3,
    "title": "Superman Test Post",
    "content": "This is a big good juju test post on the ethanc account!\nI like trains!",
    "likes_count": 0,
    "comments_count": 0,
    "created_at": "2024-09-24T18:29:50.058701",
    "updated_at": "2024-09-24T18:29:58.624499",
    "author": {
      "id": 4,
      "username": "ethanc"
    },
    "likes": [],
    "comments": []
  },
  {
    "id": 2,
    "title": "Another Post",
    "content": "This is my second post. Created by the User",
    "likes_count": 1,
    "comments_count": 1,
    "created_at": "2024-09-24T05:00:18.568652",
    "updated_at": null,
    "author": {
      "id": 2,
      "username": "user"
    },
    "likes": [
      {
        "id": 1,
        "user_id": 1
      }
    ],
    "comments": [
      {
        "id": 1,
        "user_id": 1,
        "content": "This is a comment on the second post.",
        "created_at": "2024-09-24T05:00:18.569052",
        "updated_at": null
      }
    ]
  },
  {
    "id": 1,
    "title": "Hello, World!",
    "content": "This is my first post. Created by the Admin!",
    "likes_count": 2,
    "comments_count": 2,
    "created_at": "2024-09-24T05:00:18.568466",
    "updated_at": null,
    "author": {
      "id": 1,
      "username": "admin"
    },
    "likes": [
      {
        "id": 2,
        "user_id": 2
      },
      {
        "id": 3,
        "user_id": 4
      }
    ],
    "comments": [
      {
        "id": 2,
        "user_id": 2,
        "content": "This is a comment on the first post.",
        "created_at": "2024-09-24T05:00:18.569164",
        "updated_at": null
      },
      {
        "id": 4,
        "user_id": 4,
        "content": "This is a big good juju test comment on the first post!",
        "created_at": "2024-09-24T18:21:22.664342",
        "updated_at": null
      }
    ]
  }
]
```
- **GET /feed/following**
  - **HTTP Method:** GET
  - **Request Parameters:**
    - `?page`: (Optional) Page number of the feed
    - `?per_page`: (Optional) Number of posts per page
  - **Authorization**: JWT token required in the `Authorization` header
  - **Example Request:**
```bash
curl http://localhost:5000/feed/following -H "Authorization: Bearer <your_token>"
```
  - **Example Response:**
```json
  [
  {
    "id": 3,
    "title": "Superman Test Post",
    "content": "This is a big good juju test post on the ethanc account!\nI like trains!",
    "likes_count": 0,
    "comments_count": 0,
    "created_at": "2024-09-24T18:29:50.058701",
    "updated_at": "2024-09-24T18:29:58.624499",
    "author": {
      "id": 4,
      "username": "ethanc"
    },
    "likes": [],
    "comments": []
  },
  {
    "id": 2,
    "title": "Another Post",
    "content": "This is my second post. Created by the User",
    "likes_count": 1,
    "comments_count": 1,
    "created_at": "2024-09-24T05:00:18.568652",
    "updated_at": null,
    "author": {
      "id": 2,
      "username": "user"
    },
    "likes": [
      {
        "id": 1,
        "user_id": 1
      }
    ],
    "comments": [
      {
        "id": 1,
        "user_id": 1,
        "content": "This is a comment on the second post.",
        "created_at": "2024-09-24T05:00:18.569052",
        "updated_at": null
      }
    ]
  },
  {
    "id": 1,
    "title": "Hello, World!",
    "content": "This is my first post. Created by the Admin!",
    "likes_count": 2,
    "comments_count": 2,
    "created_at": "2024-09-24T05:00:18.568466",
    "updated_at": null,
    "author": {
      "id": 1,
      "username": "admin"
    },
    "likes": [
      {
        "id": 2,
        "user_id": 2
      },
      {
        "id": 3,
        "user_id": 4
      }
    ],
    "comments": [
      {
        "id": 2,
        "user_id": 2,
        "content": "This is a comment on the first post.",
        "created_at": "2024-09-24T05:00:18.569164",
        "updated_at": null
      },
      {
        "id": 4,
        "user_id": 4,
        "content": "This is a big good juju test comment on the first post!",
        "created_at": "2024-09-24T18:21:22.664342",
        "updated_at": null
      }
    ]
  }
]
```
### **Comments**

- **GET /posts/{post_id}/comments**

  - **HTTP Method:** GET
  - **Request Parameters:**
    - `post_id`: ID of the post to get comments for
    - `page` (optional): Page number for pagination
    - `per_page` (optional): Number of comments per page
  - **Response Format:** JSON array of comment objects (id, user_id, post_id, content, created_at, updated_at)
  - **Example Request:**
    ```bash
    curl http://localhost:5000/posts/1/comments -H "Authorization: Bearer <your_token>"
    ```
  - **Example Response:**
    ```json
    [
      {
        "id": 1,
        "user_id": 2,
        "post_id": 1,
        "content": "Great post!",
        "created_at": "2024-01-01T00:01:00Z",
        "updated_at": "2024-01-01T00:01:00Z"
      },
      {
        "id": 2,
        "user_id": 3,
        "post_id": 1,
        "content": "I agree.",
        "created_at": "2024-01-01T00:02:00Z",
        "updated_at": "2024-01-01T00:02:00Z"
      }
    ]
    ```

- **POST /posts/{post_id}/comments**

  - **HTTP Method:** POST
  - **Request Parameters:**
    - `post_id`: ID of the post to comment on
    - `content`
  - **Response Format:** JSON object representing the newly created comment
  - **Example Request:**
    ```
    curl -X POST http://localhost:5000/posts/1/comments -H "Authorization: Bearer <your_token>" -d '{"content": "This is a comment."}'
    ```
  - **Example Response:**
    ```json
    {
      "id": 3,
      "user_id": 1,
      "post_id": 1,
      "content": "This is a comment.",
      "created_at": "2024-01-01T00:03:00Z",
      "updated_at": "2024-01-01T00:03:00Z"
    }
    ```

- **PUT /posts/{post_id}/comments/{comment_id}**

  - **HTTP Method:** PUT
  - **Request Parameters:**
    - `comment_id`: ID of the comment to update
    - `content` (optional)
  - **Response Format:** JSON object representing the updated comment
  - **Example Request:**
    ```
    curl -X PUT http://localhost:5000/comments/1 -H "Authorization: Bearer <your_token>" -d '{"content": "Updated comment."}'
    ```
  - **Example Response:**
    ```json
    {
      "id": 1,
      "user_id": 2,
      "post_id": 1,
      "content": "Updated comment.",
      "created_at": "2024-01-01T00:01:00Z",
      "updated_at": "2024-01-01T00:03:00Z"
    }
    ```

- **DELETE /posts/{post_id}comments/{comment_id}**

  - **HTTP Method:** DELETE
  - **Request Parameters:**
    - `comment_id`: ID of the comment to delete
  - **Response Format:** No response body
  - **Example Request:**
    ```
    curl -X DELETE http://localhost:5000/comments/1 -H "Authorization: Bearer <your_token>"
    ```

### **Likes**

- **POST /posts/{post_id}/like**

  - **HTTP Method:** POST
  - **Request Parameters:**
    - `post_id`: ID of the post to like
  - **Response Format:** No response body
  - **Example Request:**
    ```
    curl -X POST http://localhost:5000/posts/1/likes -H "Authorization: Bearer <your_token>"
    ```

- **DELETE /posts/{post_id}/like**

  - **HTTP Method:** DELETE
  - **Request Parameters:**
    - `post_id`: ID of the post to unlike
  - **Response Format:** No response body
  - **Example Request:**
    ```
    curl -X DELETE http://localhost:5000/posts/1/likes -H "Authorization: Bearer <your_token>"
    ```
  - **Example Response:**
```json
  {
    "message": "Post unliked successfully"
  }
  ```

- **GET /posts/{post_id}/likes**

  - **HTTP Method:** GET
  - **Request Parameters:**
  - **Response Format:** No response body
  - **Example Request:**
  ```bash
  curl http://localhost:5000/posts/1/likes -H "Authorization: Bearer <your_token>"
  ```
  - **Example Response:**
  ```json
  {
    "likes": [
      {
        "id": 1,
        "user_id": 1,
        "post_id": 1
      },
      {
        "id": 2,
        "user_id": 2,
        "post_id": 1
      }
    ]
  }
  ```

### **Follows**

- **POST /users/{user_id}/follow**

  - **HTTP Method:** POST
  - **Request Parameters:**
    - `user_id`: ID of the user to follow
  - **Response Format:** No response body
  - **Example Request:**
    ```
    curl -X POST http://localhost:5000/users/2/follow
    ```

- **DELETE /users/{user_id}/follow**

  - **HTTP Method:** DELETE
  - **Request Parameters:**
    - `user_id`: ID of the user to unfollow
  - **Response Format:** No response body
  - **Example Request:**
    ```
    curl -X DELETE http://localhost:5000/users/2/follow
    ```

**Remember to replace `http://localhost:5000` with the actual URL of your API.**

## Prerequisites

- Python 3.6 or later
- PostgreSQL database
- `pip` package manager
- Virtual Environment

## Installation

1. **Install PostgreSQL:**

   - **Windows:** Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/). Follow the installation instructions.
   - **macOS:** Use Homebrew to install PostgreSQL:
     ```bash
     brew install postgresql
     ```
   - **Linux:** Consult your distribution's package manager for installation instructions.

2. **Create a PostgreSQL user and database:**

   - Open the PostgreSQL command-line interface (psql).
   - Create a new user:
     ```sql
     CREATE USER your_username WITH PASSWORD 'your_password';
     ```
   - Create a new database:
     ```sql
     CREATE DATABASE social_media_api;
     ```
   - Grant privileges to the user:
     ```sql
     GRANT ALL PRIVILEGES ON DATABASE social_media_api TO your_username;
     ```
   - Connect to the database:

   ```sql
       \connect social_media_api
   ```

   - Grant privileges to the user with the public schema:

   ```sql
   GRANT USAGE ON SCHEMA public TO your_username;
   ```

3. **Clone the repository:**

   ```bash
   git clone https://github.com/finneh4249/t2a2-api-application.git
   ```

4. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\bin\activate.ps1
   ```

5. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Configure database settings:**
   Update the `.env.example` file with your database connection details, including the username, password, database name, and host.
   Rename the `.env.example` file to `.env`.

7. **Create the database:**
  In order to create the database, use the following commands:

  ```bash
    flask cli db_create
  ```
This command will create all the tables in the database, and seed it with default values.

8. **Run the application:**
  ```bash
  flask run
  ```
9.  **Access API endpoints:**
   Use your preferred HTTP client (e.g., Postman, curl, Insomnia, etc) to interact with the API endpoints.

## Additional Information

- **Authentication:** Use token-based authentication for user authorisation.
- **Error handling:** The API returns appropriate HTTP status codes and error messages.
- **Pagination:** For large result sets, pagination is supported.
- **Rate limiting:** To prevent abuse, rate limiting is implemented.
- **Confirmation Emails:** To keep simplicity in the program, confirmation emails are not sent to the user, however, a confirmation link is returned in the endpoint. This is a simulated behaviour for simplicities sake for this assignment.

### Error Handling

The API implements robust error handling to provide informative feedback to clients in case of exceptions or unexpected situations. When an error occurs, the API returns a JSON response with a descriptive error message and an appropriate HTTP status code.

```py
@user_controller.route('/users/<user_id>')
def get_user(user_id):
  user = User.query.get(user_id)
  if user is None:
    return {"message": "User not found"}, 404
```

In this example, the code attempts to retrieve the user with the specified user_id. If the user is not found, a `404 Not Found` error is raised. 
Other errors that may commonly occur during the execution of the code are handled in the same way, for example, a `401 Unauthorized` error is returned if the user is not the owner of the requested resource.

With the exception of a `Marshamallow Validation Error`, if any other exception occurs, a generic `500 Internal Server Error` is returned with an error message.

### CLI Commands

The CLI commands are provided for convenience. You can use them to create or drop the database, and create a new user, or admin user.

```bash
flask cli db_create # Creates all tables in the database.
flask cli db_drop # Drops all tables in the database.
flask cli create_user <username> <email> <password> <bio> [--admin] # Creates a user, use the --admin flag to create an admin user.
flask cli delete_user <username> # Deletes the selected user from the database.
```