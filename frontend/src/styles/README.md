# Styles

Why it exists: this folder is reserved for reusable style documentation or extracted theme modules.

What it does: Phase 1 keeps executable global tokens in `src/app/globals.css` because Next.js imports global CSS from the app tree.

How it interacts: future shared style files can be imported by `globals.css` when the theme grows.
