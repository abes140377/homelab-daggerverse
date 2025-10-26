![banner](https://cdn.jsdelivr.net/gh/fluent-ci-templates/.github@main/assets/images/space_scene_space_landmarks_cartoon_style_725cc795-15b3-4bd7-8f17-9a7ee35417b9.png)

# Daggerverse 🪐 🌌

A collection of [Dagger](https://dagger.io) modules for homelab automation. Dagger is a programmable CI/CD engine that runs pipelines in containers, providing reproducible, cacheable, and portable automation workflows.

## 📦 Available Modules

### Ansible

Execute Ansible playbooks and manage Galaxy collections in containerized environments.

**Functions:**
- `galaxy-install` - Install Ansible Galaxy collections from requirements.yml
- `run-playbook` - Execute playbooks with support for inventory, extra variables, and tag filtering

**Quick Start:**
```bash
cd ansible

# Install Galaxy collections
dagger call galaxy-install --directory=/path/to/playbook

# Run a playbook
dagger call run-playbook --directory=/path/to/playbook --playbook=site.yml

# Run with all options
dagger call run-playbook \
  --directory=/path/to/playbook \
  --playbook=site.yml \
  --inventory=inventory/hosts.ini \
  --extra-vars=env=production \
  --extra-vars=version=2.0 \
  --tags=deploy
```

**Test Coverage:** 6 comprehensive tests ✅

### Ansible-Lint

*(Coming Soon)* - Ansible linting and best practices validation

## 🚀 Getting Started

### Prerequisites

Install Dagger using [mise](https://mise.jdx.dev/):

```bash
# Install mise if not already installed
curl https://mise.run | sh

# Install Dagger (defined in mise.toml)
mise install
```

**Required:**
- Python 3.13+
- Docker or Podman (for Dagger containers)

### Using a Module

```bash
# Navigate to a module directory
cd ansible

# List available functions
dagger functions

# Call a function
dagger call <function-name> --arg=value
```

### Running Tests

```bash
# Run all tests for a module
cd ansible
dagger call -m tests all

# Run a specific test
dagger call -m tests test-run-playbook-simple
```

### Exploring Examples

```bash
# Run examples to see usage patterns
cd ansible
dagger call -m examples/python simple-playbook-example
dagger call -m examples/python advanced-playbook-example
```

## 🏗️ Development

### Module Structure

This repository follows a monorepo pattern where each top-level directory is an independent Dagger module:

```
homelab-daggerverse/
├── ansible/              # Ansible automation module
│   ├── src/              # Main module code
│   ├── tests/            # Test module
│   └── examples/         # Example module
├── ansible-lint/         # Ansible linting module
└── openspec/             # Specification management
```

Each module is a Python package with:
- `dagger.json` - Module configuration
- `pyproject.toml` - Python dependencies
- `src/<module>/main.py` - Module functions
- `sdk/` - Embedded Dagger Python SDK

### Creating a New Module

```bash
# Create module directory
mkdir my-module
cd my-module

# Initialize Dagger module
dagger init --name=my-module --sdk=python

# Implement functions in src/my-module/main.py
```

### Module Development Workflow

```bash
# Navigate to module
cd <module-name>

# Edit source code
vim src/<module-name>/main.py

# Regenerate SDK if structure changed
dagger develop

# Test changes
dagger call <function-name>
```

### Testing Best Practices

Following Dagger best practices, modules include test submodules:

```bash
# Create test module
mkdir tests
cd tests
dagger init --name=tests --sdk=python --source=.
dagger install ..

# Implement tests in src/tests/main.py
# Run tests
dagger call -m tests all
```

## 📋 Python Module Pattern

Each Dagger module is a Python class with decorated methods:

```python
import dagger
from dagger import dag, function, object_type

@object_type
class MyModule:
    @function
    async def my_function(
        self,
        directory: dagger.Directory,
        config_file: str = "config.yml"
    ) -> str:
        """Function description shown in CLI help"""
        return await (
            dag.container()
            .from_("alpine:latest")
            .with_mounted_directory("/work", directory)
            .with_workdir("/work")
            .with_exec(["cat", config_file])
            .stdout()
        )
```

**Key Concepts:**
- `@object_type` - Marks the class as a Dagger module
- `@function` - Exposes a method as a callable function
- `dag` - Pre-initialized Dagger API client
- Type hints are required and map to Dagger types

## 🧪 Testing

All modules include comprehensive test coverage:

| Module | Tests | Status |
|--------|-------|--------|
| ansible | 6 tests | ✅ All passing |
| ansible-lint | - | 🚧 Pending |

Run tests with:
```bash
cd <module-name>
dagger call -m tests all
```

## 📚 Resources

- [Dagger Documentation](https://docs.dagger.io)
- [Dagger Python SDK](https://dagger-io.readthedocs.org)
- [Daggerverse](https://daggerverse.dev) - Public module registry
- [CLAUDE.md](./CLAUDE.md) - Detailed development guide

## 🔧 Configuration

Dagger CLI version is managed via `mise.toml`:
```toml
[tools]
dagger = "0.19.3"
```

Python modules use `uv` for dependency management (configured in `pyproject.toml`).

## 🤝 Contributing

This is a personal homelab collection, but feel free to use these modules as inspiration for your own Daggerverse!

## 📝 License

See individual module LICENSE files for details.

---

**Note:** This repository uses [OpenSpec](./openspec/) for managing feature proposals and specifications. See `openspec/AGENTS.md` for details on the development workflow.
