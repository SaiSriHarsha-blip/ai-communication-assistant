# API Layer

Why it exists: this folder will own HTTP clients and request adapters.

What it does: Phase 2 should place the Axios instance here so components never call Axios directly.

How it interacts: services will consume API clients from here, while hooks consume services.
