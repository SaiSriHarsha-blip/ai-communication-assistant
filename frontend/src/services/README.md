# Service Layer

Why it exists: services keep backend use cases separate from React rendering.

What it does: Phase 2 should add message generation functions that preserve the FastAPI contract.

How it interacts: hooks call services, services call the API layer, and components call hooks.
