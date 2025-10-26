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
├── ansible/          # Dagger module for Ansible automation
│   ├── tests/        # Test module for ansible
│   └── examples/     # Example module showcasing usage
├── ansible-lint/     # Dagger module for Ansible Lint
├── openspec/         # Specification and change management
└── <future modules>
```

Each module follows the **Dagger Python SDK structure**:

```
<module-name>/
├── dagger.json           # Dagger module configuration (name, engine version, SDK)
├── pyproject.toml        # Python project config with dagger-io dependency
├── src/<module>/main.py  # Main module code with @object_type and @function decorators
├── tests/                # Test module (optional, follows same structure)
│   ├── dagger.json
│   ├── src/tests/main.py
│   └── test-data/        # Test fixtures (playbooks, inventories, etc.)
├── examples/             # Example module (optional, follows same structure)
│   └── python/
│       ├── dagger.json
│       ├── src/examplespython/main.py
│       └── example-data/ # Example fixtures
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
# Ansible module examples
cd ansible

# Install Ansible Galaxy collections
dagger call galaxy-install --directory=/path/to/playbook --requirements-file=requirements.yml

# Run an Ansible playbook
dagger call run-playbook --directory=/path/to/playbook --playbook=site.yml

# Run playbook with inventory
dagger call run-playbook --directory=/path/to/playbook --playbook=site.yml --inventory=inventory/hosts.ini

# Run playbook with extra variables
dagger call run-playbook --directory=/path/to/playbook --playbook=site.yml --extra-vars=env=production --extra-vars=version=2.0

# Run playbook with tag filtering
dagger call run-playbook --directory=/path/to/playbook --playbook=site.yml --tags=deploy --tags=config
```

**Running Tests**:
```bash
# Run all tests for the ansible module
cd ansible
dagger call -m tests all

# Run specific test
dagger call -m tests test-run-playbook-simple
```

**Running Examples**:
```bash
# Run examples to see module usage
cd ansible
dagger call -m examples/python simple-playbook-example
dagger call -m examples/python advanced-playbook-example
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

### Testing and Example Modules

Following Dagger best practices, modules can include test and example submodules:

**Test Module Pattern** (`tests/`):
- Create tests as Dagger functions that call the main module
- Use `dagger install ..` to depend on parent module
- Include test data in `test-data/` directory
- Run all tests with `dagger call -m tests all`

**Example Module Pattern** (`examples/python/`):
- Demonstrate real-world usage of the module
- Examples are executable and serve as living documentation
- Include example data in `example-data/` directory

## Current Modules

### Ansible Module

**Purpose**: Execute Ansible playbooks and manage Galaxy collections in containerized environments

**Available Functions**:
- `galaxy-install` - Install Ansible Galaxy collections from requirements.yml
  - Parameters: `directory` (Directory), `requirements-file` (str, default: "requirements.yml")
  - Returns: Container with collections installed

- `run-playbook` - Execute Ansible playbooks with full parameter support
  - Parameters:
    - `directory` (Directory) - Playbook directory
    - `playbook` (str) - Playbook file path
    - `inventory` (str, optional) - Inventory file path
    - `extra-vars` (list[str], optional) - Variables in key=value format
    - `tags` (list[str], optional) - Tag filters
  - Returns: Playbook execution output (str)

**Container Image**: `alpine/ansible:latest`

**Test Coverage**: 6 comprehensive tests covering all parameter combinations

### Ansible-Lint Module

**Status**: Placeholder module (contains example functions)

**TODO**: Implement ansible-lint functionality

## Important Notes

- Each module is **independent** with its own `dagger.json` and dependencies
- Module names use **kebab-case** for directories (e.g., `ansible-lint`)
- Python class names use **PascalCase** (e.g., `AnsibleLint`)
- Dagger function names are **kebab-case** in CLI (e.g., `container-echo`)
- All modules currently use **Dagger engine v0.19.3**
