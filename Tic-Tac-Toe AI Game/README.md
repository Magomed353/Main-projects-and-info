# Tic-Tac-Toe AI API

A Flask REST API for playing Tic-Tac-Toe against a computer opponent using the Minimax algorithm.

The project focuses on layered architecture, dependency injection, game logic, and managing multiple games through an HTTP API.

## Features

- Creating games with unique UUIDs.
- Submitting player moves as updated board states.
- Generating computer moves using Minimax.
- Detecting wins and draws.
- Checking that previously placed computer marks remain unchanged.
- Storing multiple games in memory.
- Separating API handling, business logic, and data access.

## Technologies

- **Python 3**
- **Flask** — HTTP routing and JSON responses.
- **Minimax** — evaluating possible moves.
- **threading.Lock** — synchronizing repository reads and writes.
- **uuid** — generating game identifiers.

## Architecture

The application is organized into four layers:

| Layer | Responsibility |
| --- | --- |
| `web` | HTTP routes, request and response models, and mapping between web and domain models. |
| `domain` | Game models, service interface, move validation, and Minimax logic. |
| `datasource` | Storage models, an in-memory repository, and mapping between storage and domain models. |
| `di` | A custom container that creates and reuses repository and service instances. |

Separate models and mappers keep HTTP handling and storage details outside the game logic.

## Project Structure

```text
src/
├── web/
│   ├── model/
│   │   └── game_web.py
│   ├── mapper/
│   │   └── game_mapper_web.py
│   └── route/
│       └── controller.py
├── domain/
│   ├── model/
│   │   └── model.py
│   └── service/
│       ├── service.py
│       └── service_impl.py
├── datasource/
│   ├── model/
│   │   └── storage.py
│   ├── mapper/
│   │   └── game_mapper.py
│   └── repository/
│       ├── repository.py
│       └── repository_impl.py
└── di/
    └── container.py
```

## Installation

Python 3 and `pip` are required.

Install Flask from the project root:

```bash
python -m pip install Flask
```

## Running the Application

From the project root:

```bash
cd src
python -m web.route.controller
```

Run the application as a module from `src` so that imports between the project layers resolve correctly.

The development server starts at `http://127.0.0.1:5000` with debug mode enabled.

The project provides an HTTP API. Requests can be sent using an API client such as Postman.

## Board Representation

The board is represented as a 3×3 integer matrix:

| Value | Meaning |
| --- | --- |
| `0` | Empty cell |
| `1` | Player mark |
| `2` | Computer mark |

Example:

```json
[
  [1, 0, 0],
  [0, 2, 0],
  [0, 0, 0]
]
```

## API Endpoints

### Create a Game

```http
POST /game/new
```

Creates a new game with an empty board. No request body is required.

Example response:

```json
{
  "uuid": "123e4567-e89b-42d3-a456-426614174000",
  "field": [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
  ]
}
```

The UUID above is illustrative. Use the identifier returned by the server in subsequent requests.

### Submit a Move

```http
POST /game/{uuid}
Content-Type: application/json
```

Send the complete board after adding a player mark. Preserve all marks from the previous server response.

Example first move:

```json
{
  "field": [
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
  ]
}
```

The server checks the submitted board, generates a computer move, saves the updated game, and returns:

| Field | Description |
| --- | --- |
| `uuid` | The game identifier. |
| `field` | The board after the computer move. |
| `status` | `true` if the game has ended; otherwise `false`. |

Use the returned board as the starting point for the next player move.

### Error Responses

The API returns an `error` field for explicitly handled errors.

| HTTP status | Description |
| --- | --- |
| `400` | The move changes a previously placed computer mark. |
| `404` | No game exists with the supplied UUID. |

Example:

```json
{
  "error": "Неверный ход"
}
```

Error messages are currently returned in Russian.

## Game Storage

Games are stored in an in-memory dictionary inside the repository. Repository reads and writes are protected with `threading.Lock`.

Each game is identified by its UUID, allowing the application to maintain multiple independent games.

## Current Limitations

- Games are lost when the server restarts, and storage is not shared between separate server processes.
- Board validation currently protects existing computer marks. Board dimensions, cell values, move counts, and submissions after game completion are not fully handled.
- The response indicates whether the game has ended but does not separately identify the winner or a draw.

## Skills Practiced

- Building a Flask HTTP API.
- Implementing recursive game-tree search with Minimax.
- Designing a layered application.
- Separating interfaces from implementations.
- Mapping data between application layers.
- Applying the repository pattern and dependency injection.
- Managing shared in-memory data.
- Processing JSON requests and responses.
