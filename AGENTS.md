# Agent Development Guide

A file for [guiding AI coding agents](https://agents.md/).

## Project Overview

The project's goal is to port the original trilogy (Jak 1 -> Jak 3) to PC. Over 98% of the games were written in GOAL, a custom LISP language developed by Naughty Dog https://opengoal.dev/docs/reference/. Our strategy is:
- decompile the original game code into human-readable GOAL code
- develop our own compiler for GOAL and recompile the game code for x86-64
- create a tool to extract game assets into formats that can be easily viewed or modified
- create tools to repack game assets into a format that our port uses.

Our objectives are:
- make the port a "native application" on x86-64, with high performance. It shouldn't be emulated, interpreted, or transpiled.
- Our GOAL compiler's performance should be around the same as unoptimized C.
- try to match things from the original game and development as possible. For example, the original GOAL compiler supported live modification of code while the game is running, so we do the same, even though it's not required for just porting the game.
- support modifications. It should be possible to make edits to the code without everything else breaking.

At the moment we support **x86_64** on Windows, Linux and macOS (via Rosetta translation).  
### Project Structure

There are four main components to the project.

1. `goalc` - the GOAL compiler for x86-64
2. `decompiler` - our decompiler
3. `goal_src/` - the folder containing all OpenGOAL / GOOS code
4. `game` - aka the runtime written in C++

## Commands

Common commands that are useful.  We use https://taskfile.dev/ to make cross-platform build commands possible.

- `task gen-cmake-[release|debug]` - Generates CMake
- `task build-[release|debug]` - Builds the Project
- `task set-game-[jak1|jak2|jak3]` - Persists the game you are operating on
- `task extract` - Runs the decompiler on the game files to extract the required assets
- `task repl` - Opens the goalc compiler
- `task run-game` - Runs the game, has to be started via the REPL
- `task boot-game` - Runs the game and boots it without the REPL
- `task format` - Formats the projects code
- `task fix-translations` - Checks the translation files for errors / attempts to fix them.


#  Agent Instructions

## Sources of Truth
1. Actual source and definitions in this repository
2. Verified working patterns in the repository
3. OpenGOAL reference documentation
4. Existing project-specific AI reference documents

Never assume generic Common Lisp syntax or APIs
are compatible with GOAL.

## Before Implementing
- Read all applicable AGENTS.md instructions.
- Check git status and the existing diff.
- Find the current behavior and relevant functions.
- Search for callers, references, types, and methods.
- Identify shared code and initialization dependencies.
- Explain planned changes before implementing.
- If the task is explicitly research-only, do not edit.

## GOAL Rules
- Reuse existing types, functions, and conventions.
- Verify symbol names and method signatures.
- Preserve GOAL state-machine behavior.
- Avoid unrelated refactoring or formatting.
- Respect decompiler-managed source boundaries.
- Do not edit generated files unless necessary.
- Examine DGO changes and load-order dependencies.
- Do not replace working engine code with
  speculative implementations.

## Gameplay Rules
- Identify affected entities and game modes.
- Keep weapon changes scoped to intended weapons.
- Preserve projectile collision and damage behavior
  unless explicitly asked to change them.
- Protect vehicle physics and player controls from
  unrelated gameplay changes.
- Treat timing, animation, and state transitions
  as potentially frame-sensitive.

## Verification
- Run the appropriate build or compiler check.
- Read the complete relevant error messages.
- Correct errors introduced by the change.
- Run git diff --check and inspect the diff.
- Distinguish compile success from runtime success.
- Document any remaining in-game testing.

## Review
Look for:
- Incorrect GOAL types or method calls
- Changes affecting shared systems
- Broken states or transitions
- Incorrect damage and cooldown calculations
- DGO loading or initialization regressions
- Unintended behavior outside the requested scope

## Safety
- Never overwrite existing unrelated work.
- No commits, pushes, resets, or rebases without
  explicit authorization.
- No destructive commands without approval.
- Never include copyrighted game assets in commits.

## Completion Report
Provide:
1. Summary of changes
2. Files and functions modified
3. Build commands and observed results
4. Potential risks and side effects
5. In-game tests still required