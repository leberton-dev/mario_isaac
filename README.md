# Mario Isaac

A Binding of Isaac-like built with Ptthon and pygame.

## Setup

Requires [uv](https://docs.astral.sh/uv/)

```bash
uv sync
uv run python -m mario_isaac.main
```

## Architecture

- `src/mario_isaac/scene/` - scene stack (menu, gameplay) driven by `SceneManager`.
- `src/mario_isaac/ecs/` - entity-component-system: `EntityManager` stores components, `System` subclasses (input, movement, collision, rendering, AI) run each frame.
- `src/mario_isaac/room/` - dungeon layout: `RoomGrid` procedurally generates the room graph, `Room` holds per-room floor/walls/enemies.
- `src/mario_isaac/core/` - cross-cutting services: `Config`, `AssetManager`, `EventBus`.

### Design decisions
- `AIMovementSystem`, `WallCollisionSystem`, and `EntityCollisionSystem` depend directly on `RoomGrid` instead of representing walls as ECS entities. This is a deliberate choice not overseight.

## Developement

```bash
uv run pytest   # once test exist
uv run ruff check
```

