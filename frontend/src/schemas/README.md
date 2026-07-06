# Schemas

Why it exists: Zod schemas centralize validation and runtime payload expectations.

What it does: Phase 2 should add form and response schemas for normal and clarification responses.

How it interacts: React Hook Form uses these schemas through zod resolvers; services can reuse response schemas.
