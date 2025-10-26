<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository is a **Daggerverse** - a collection of [Dagger](https://dagger.io) modules for homelab automation. Dagger is a programmable CI/CD engine that runs pipelines in containers.

## Repository Structure

The repository follows a **monorepo pattern** where each top-level directory is an independent Dagger module:

```
homelab-daggerverse/
├── ansible/          # Dagger module for Ansible
├── ansible-lint/     # Dagger module for Ansible Lint
└── <future modules>
```

Each module follows the **Dagger Python SDK structure**:

```
<module-name>/
├── dagger.json           # Dagger module configuration (name, engine version, SDK)
├── pyproject.toml        # Python project config with dagger-io dependency
├── src/<module>/main.py  # Main module code with @object_type and @function decorators
└── sdk/                  # Embedded Python SDK (Go runtime + Python codegen)
    ├── runtime/          # Go code for Python runtime execution
    │   ├── main.go       # SDK entrypoint
    │   ├── python.go     # Python runtime orchestration
    │   ├── image.go      # Container image management
    │   └── ...
    ├── codegen/          # Python code generation
    └── src/dagger/       # Dagger Python SDK client library
```

## Development Commands

### Working with Dagger Modules

**Prerequisites**: Dagger CLI is managed via `mise` (see `mise.toml`):
```bash
mise install  # Install dagger 0.19.3
```

**Module Development**:
```bash
# From a module directory (e.g., ansible/ or ansible-lint/)
cd <module-name>

# Initialize a new module
dagger init --name=<module-name> --sdk=python

# Prepare module for local development
dagger develop

# List available functions in the module
dagger functions

# Call a function
dagger call <function-name> --arg=value

# Install a dependency module
dagger install <module-path>

# Update module dependencies
dagger update
```

**Testing Functions**:
```bash
# Example: Test the container-echo function
dagger call container-echo --string-arg="hello world"

# Example: Test the grep-dir function
dagger call grep-dir --directory-arg=. --pattern="import"
```

## Module Architecture

### Python Module Pattern

Each Dagger module is a Python class decorated with `@object_type`, containing methods decorated with `@function`:

```python
import dagger
from dagger import dag, function, object_type

@object_type
class ModuleName:
    @function
    def some_function(self, arg: str) -> dagger.Container:
        """Function docstring becomes Dagger function description"""
        return dag.container().from_("alpine:latest").with_exec(["echo", arg])
```

**Key Concepts**:
- `@object_type`: Marks the class as a Dagger module
- `@function`: Exposes a method as a callable Dagger function
- `dag`: The Dagger API client for accessing core functionality
- Type hints are required and map to Dagger types (`dagger.Container`, `dagger.Directory`, `str`, etc.)

### SDK Embedding

Each module embeds its own Python SDK in the `sdk/` directory:
- **Go runtime** (`sdk/runtime/`): Executes the Python module in containers
- **Python codegen** (`sdk/codegen/`): Generates Python client code from Dagger schema
- **Python SDK** (`sdk/src/dagger/`): The client library for interacting with Dagger API

The SDK is installed as an editable dependency (`pyproject.toml`):
```toml
[tool.uv.sources]
dagger-io = { path = "sdk", editable = true }
```

### Python Version

All modules require **Python 3.13+** (see `pyproject.toml` in each module).

## Common Development Workflows

### Creating a New Module

1. Create a new directory at the repository root
2. Initialize the module:
   ```bash
   cd <new-module-name>
   dagger init --name=<new-module-name> --sdk=python
   ```
3. Implement functions in `src/<module-name>/main.py`
4. Test with `dagger call <function-name>`

### Modifying an Existing Module

1. Navigate to the module directory
2. Edit `src/<module-name>/main.py`
3. Run `dagger develop` if you've changed the module structure
4. Test changes with `dagger call`

### Using uv for Dependency Management

The Python SDK supports `uv` for faster dependency management. Configure in `pyproject.toml`:
```toml
[tool.dagger]
use-uv = true
```

## Important Notes

- Each module is **independent** with its own `dagger.json` and dependencies
- Module names use **kebab-case** for directories (e.g., `ansible-lint`)
- Python class names use **PascalCase** (e.g., `AnsibleLint`)
- Dagger function names are **kebab-case** in CLI (e.g., `container-echo`)
- All modules currently use **Dagger engine v0.19.3**
