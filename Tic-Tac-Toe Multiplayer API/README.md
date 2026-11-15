# Tic-Tac-Toe — Multiplayer API

A Flask REST API for playing Tic-Tac-Toe against a computer or another user.

The project extends the previous version by adding PostgreSQL persistence, user registration, HTTP Basic Auth, and a two-player mode.

## Features

- User registration with unique usernames and UUIDs.
- Authentication using HTTP Basic Auth.
- Authentication checks for game endpoints.
- Creating games against a computer or another user.
- Listing games waiting for a second player.
- Joining an existing game.
- Switching turns between players.
- Generating computer moves using Minimax.
- Detecting wins and draws.
- Storing users and game states in PostgreSQL.
- Retrieving game and user information by UUID.

## Technologies

- **Python 3.10+**
- **Flask** — HTTP routing and JSON responses.
- **PostgreSQL** — persistent user and game storage.
- **SQLAlchemy 2.x** — ORM and database access.
- **psycopg2** — PostgreSQL database driver.
- **HTTP Basic Auth** — request authentication.
- **Minimax** — computer move selection.
- **uuid** — user and game identifiers.

## Architecture

The application is organized into four layers:

| Layer | Responsibility |
| --- | --- |
| `web` | HTTP routes, request and response models, authentication checks, and data mapping. |
| `domain` | Game models, game states, Minimax logic, and the authentication service. |
| `datasource` | ORM models, PostgreSQL connectivity, repositories, and mappers. |
| `di` | Creating and connecting repositories and services through a dependency container. |

Mappers convert models between application layers. Repositories provide access to stored data.

## Project Structure

```text
src/
├── web/
│   ├── model/
│   ├── mapper/
│   └── route/
│       ├── controller.py
│       ├── auth_controller.py
│       └── auth_middleware.py
├── domain/
│   ├── model/
│   └── service/
├── datasource/
│   ├── database.py
│   ├── model/
│   ├── mapper/
│   └── repository/
└── di/
    └── container.py
```

## Installation

Python 3.10+, `pip`, and a running PostgreSQL server are required.

Install the dependencies from the project root:

```bash
python -m pip install Flask "SQLAlchemy>=2.0,<3.0" psycopg2-binary
```

### PostgreSQL Configuration

Create a database, for example:

```sql
CREATE DATABASE tictactoe;
```

Set the connection string in `src/datasource/database.py`:

```python
DATABASE_URL = "postgresql://USER:PASSWORD@localhost:5432/tictactoe"
```

Replace `USER` and `PASSWORD` with the credentials of a PostgreSQL user with the necessary database permissions.

The connection is configured directly in the file. Loading configuration from `.env` files or environment variables is not currently implemented.

The `users` and `games` tables are created automatically during application initialization. The database itself must already exist.

## Running the Application

Run the following commands from the project root:

```bash
cd src
python -m web.route.controller
```

Run the application from `src` so that imports between project layers resolve correctly.

The development server starts at `http://127.0.0.1:5000` with debug mode enabled.

Use Postman or another HTTP client to interact with the API.

## Authentication

### Registration

```http
POST /signup
Content-Type: application/json
```

Example request body:

```json
{
  "login": "alice",
  "password": "example-password"
}
```

Successful registration returns HTTP status `201`:

```json
{
  "status": "зарегистрирован"
}
```

### Login

```http
POST /login
Authorization: Basic <Base64(login:password)>
```

The server validates the credentials and returns the user’s UUID.

In Postman, select **Basic Auth** and enter the username and password. The client generates the header automatically.

Every protected request must include Basic Auth credentials. The `/login` endpoint returns a user UUID rather than an access token.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/signup` | Register a user. |
| `POST` | `/login` | Validate credentials and retrieve the user’s UUID. |
| `POST` | `/game/new` | Create a game. |
| `GET` | `/games` | List games with the `WAITING` status. |
| `POST` | `/game/{uuid}/join` | Join a game. |
| `POST` | `/game/{uuid}` | Submit a move. |
| `GET` | `/game/{uuid}` | Retrieve the current game state. |
| `GET` | `/user/{uuid}` | Retrieve a user’s UUID and username. |

All game endpoints and the user information endpoint require Basic Auth.

## Creating a Game

```http
POST /game/new
Content-Type: application/json
```

Example request for a game against another user:

```json
{
  "game_type": "VS_PLAYER"
}
```

Available modes:

| Value | Mode |
| --- | --- |
| `VS_COMPUTER` | Play against the computer. |
| `VS_PLAYER` | Play against another user. |

To play against the computer, send:

```json
{
  "game_type": "VS_COMPUTER"
}
```

The response contains the game UUID, board, game mode, and initial status.

## Board Representation

The board is represented as a 3×3 integer matrix:

| Value | Meaning |
| --- | --- |
| `0` | Empty cell. |
| `1` | First player’s mark. |
| `2` | Second player’s or computer’s mark. |

### Submitting a Move

```http
POST /game/{uuid}
Content-Type: application/json
```

Send the complete board after making your move:

```json
{
  "field": [
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
  ]
}
```

In `VS_COMPUTER` mode, the server generates a computer response. In `VS_PLAYER` mode, it passes the turn to the next player.

The response contains:

| Field | Description |
| --- | --- |
| `uuid` | Game identifier. |
| `field` | Updated board. |
| `status` | Result of the game completion check. |
| `current_turn` | Next player’s UUID or `null`. |

## Game States

The game model uses the following states:

| State | Description |
| --- | --- |
| `WAITING` | Waiting for a second player. |
| `PLAYER_TURN` | A player’s turn. |
| `DRAW` | The game ended in a draw. |
| `PLAYER_WIN` | One of the players won. |

The move endpoint may also return `CONTINUE` when the game is still in progress.

## Two-Player Example

1. Register two users, such as `alice` and `bob`.
2. As `alice`, create a game with the `VS_PLAYER` mode.
3. As `bob`, retrieve available games using `GET /games`.
4. Join the selected game using `POST /game/{uuid}/join`.
5. Take turns submitting updated boards through `POST /game/{uuid}`, using the corresponding player’s credentials.
6. Retrieve the game state using `GET /game/{uuid}`.

## Error Responses

| HTTP Status | Example Causes |
| --- | --- |
| `400` | An invalid move, an attempt to move out of turn, a finished game, or a full game. |
| `401` | Missing authentication or an incorrect username/password pair. |
| `404` | The game or user was not found. |
| `409` | A user with the specified username already exists. |

For explicitly handled errors, the server returns JSON:

```json
{
  "error": "Сейчас не ваш ход"
}
```

## Data Storage

PostgreSQL stores:

- Each user’s UUID, username, and password.
- Each game’s UUID and board.
- Game mode and status.
- Participants and their assigned symbols.
- The UUID of the player whose turn it is.

Data persists across application restarts. Tables are created through SQLAlchemy; database migrations are not currently implemented.

## Current Limitations

- Passwords are stored and compared without hashing.
- Board validation, game membership checks, and joining conditions require further work.
- Consistency between the stored game status and `current_turn` during move processing requires further work.
- A victory returns `PLAYER_WIN`, but the winner’s UUID is not stored or returned separately.

## Skills Practiced

- Building a Flask REST API.
- Connecting PostgreSQL and working with SQLAlchemy.
- Creating ORM models and repositories.
- Implementing user registration and HTTP Basic Auth.
- Protecting endpoints with decorators.
- Implementing game logic for two users.
- Using the Minimax algorithm.
- Designing a layered architecture.
- Applying dependency injection and mapping models between layers.
