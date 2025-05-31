# Pygame Project Coding Convention

## 1. File and Folder Structure

- Use lowercase letters and underscores for file and folder names (e.g., `main_menu.py`, `game_assets/`).
- Group related modules in packages.

## 2. Naming Conventions

- Use `snake_case` for variables and functions.
- Use `PascalCase` for class names.
- Use `UPPER_CASE` for constants.

## 3. Imports

- Standard library imports first, then third-party (e.g., `pygame`), then local imports.
- Each import on a separate line.

## 4. Code Formatting

- Indent with 4 spaces.
- Limit lines to 79 characters.
- Use blank lines to separate functions and classes.

## 5. Functions and Classes

- Each function should have a docstring describing its purpose.
- Keep functions short and focused.
- Use `self` for instance methods in classes.

## 6. Comments

- Use comments to explain non-obvious code.
- Update comments when code changes.

## 7. Pygame Specifics

- Group all event handling in a dedicated function or method.
- Use constants for event types and screen dimensions.
- Load assets (images, sounds) in a separate module or function.
