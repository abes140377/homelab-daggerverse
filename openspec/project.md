# Project Context

## Purpose

This project is a **Daggerverse** - a collection of reusable [Dagger](https://dagger.io) modules for homelab automation. Dagger is a programmable CI/CD engine that runs pipelines in containers, providing reproducible, cacheable, and portable automation workflows.

The goal is to build and maintain a personal library of Dagger modules that can be composed together to automate homelab infrastructure tasks, configuration management, and deployment pipelines.

## Tech Stack

### Core Technologies
- **Dagger Engine**: v0.19.3 (managed via mise)
- **Python**: 3.13+ (primary SDK language)
- **Dagger Python SDK**: Embedded in each module via `sdk/` directory
- **uv**: Python package manager (faster alternative to pip)
- **mise**: Tool version management (replaces asdf)

### Development Tools
- **mise.toml**: Defines tool versions (Dagger 0.19.3)
- **Git**: Version control
- **OCI Container Runtime**: Docker/Podman for Dagger execution

## Project Conventions

### Repository Structure

**Monorepo Pattern**: Each top-level directory is an independent Dagger module.

```
homelab-daggerverse/
├── ansible/              # Dagger module for Ansible automation
├── ansible-lint/         # Dagger module for Ansible Lint
├── <future-modules>/     # Additional modules as needed
├── openspec/             # Specification and change management
├── mise.toml             # Tool version definitions
├── CLAUDE.md             # AI assistant guidance
└── README.md             # Project overview
```

### Module Structure

Each Dagger module follows this standard layout:

```
<module-name>/
├── dagger.json                    # Module configuration (name, engine version, SDK)
├── pyproject.toml                 # Python project config
├── src/<module_name>/             # Module source code
│   ├── __init__.py
│   └── main.py                    # Main module with @object_type and @function
└── sdk/                           # Embedded Dagger Python SDK
    ├── runtime/                   # Go runtime for Python execution
    │   ├── main.go                # SDK entrypoint
    │   ├── python.go              # Python orchestration
    │   └── ...
    ├── codegen/                   # Python code generation
    └── src/dagger/                # Dagger Python client library
```

### Code Style

#### Naming Conventions
- **Directories**: `kebab-case` (e.g., `ansible-lint`)
- **Python Classes**: `PascalCase` (e.g., `AnsibleLint`)
- **Python Functions**: `snake_case` (e.g., `def grep_dir`)
- **Dagger CLI Functions**: `kebab-case` (e.g., `dagger call grep-dir`)
- **Module Names**: Match directory name, converted to PascalCase for the main class

#### Python Patterns
- **Python Version**: Always `>=3.13` in `pyproject.toml`
- **Type Hints**: Required on all Dagger functions (maps to Dagger API types)
- **Async/Await**: Use for I/O operations and Dagger API calls
- **Decorators**:
  - `@object_type` on the main module class
  - `@function` on exposed Dagger functions
- **Docstrings**: Required on all functions (becomes CLI help text)

#### Example Function Pattern
```python
import dagger
from dagger import dag, function, object_type

@object_type
class ModuleName:
    @function
    async def example_function(
        self,
        string_arg: str,
        directory_arg: dagger.Directory
    ) -> str:
        """Brief description of what this function does"""
        return await (
            dag.container()
            .from_("alpine:latest")
            .with_mounted_directory("/mnt", directory_arg)
            .with_exec(["command", string_arg])
            .stdout()
        )
```

### Architecture Patterns

#### Module Independence
- Each module is **completely independent** with its own dependencies
- No shared code between modules (except embedded SDK)
- Modules can depend on other modules via `dagger install`

#### Container-Based Execution
- All Dagger functions run in isolated containers
- Containers are spawned by the Dagger Engine
- Provides reproducibility, caching, and security sandboxing

#### DAG Client Pattern
- Every function has access to `dag` - the pre-initialized Dagger API client
- Use `dag.container()`, `dag.directory()`, etc. to interact with Dagger API
- Chain operations fluently: `dag.container().from_("image").with_exec([...]).stdout()`

#### Lazy Evaluation
- Dagger operations build a graph, don't execute immediately
- Execution happens when you request output (`.stdout()`, `.export()`, etc.)
- Enables intelligent caching and parallelization

### Testing Strategy

#### Test Module Pattern
- Create `tests/` subdirectory with its own Dagger module
- Write tests as Dagger functions that call the main module
- Use `dagger install ..` to depend on parent module
- Tests execute in containers, ensuring reproducibility

#### Example Module Pattern
- Create `examples/<sdk>/` subdirectories for showcasing usage
- Examples become executable tests in Daggerverse
- Combine with test module for comprehensive coverage

#### Test Function Signature
- Standardize on returning `None` (Python) or error
- Generate inputs within the test function
- Use `async`/`await` for all async operations
- Raise exceptions on test failure

#### "All" Function Pattern
- Create an `all()` function that runs all tests
- Can run tests sequentially or in parallel (using `anyio.create_task_group()`)
- Run with: `dagger call -m tests all`

### Git Workflow

#### Branching Strategy
- **main**: Production-ready code
- **feature branches**: For new capabilities (follow OpenSpec process)
- **Direct commits**: Only for bug fixes, typos, non-breaking updates

#### Commit Conventions
- Use conventional commits format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Scope: Module name or `repo` for project-level changes
- Examples:
  - `feat(ansible): add playbook execution function`
  - `fix(ansible-lint): correct linting output parsing`
  - `docs(repo): update README with new modules`

#### OpenSpec Integration
- Use OpenSpec for planned feature work and breaking changes
- Changes tracked in `openspec/changes/<change-id>/`
- Specs represent deployed capabilities in `openspec/specs/<capability>/`
- Archive completed changes to `openspec/changes/archive/YYYY-MM-DD-<name>/`

## Domain Context

### Dagger Concepts

#### Dagger Modules
- Self-contained packages of Dagger functions
- Identified by `dagger.json` configuration file
- Can depend on other modules (local or remote)
- Published to Daggerverse for community sharing

#### Dagger Functions
- Regular code decorated with `@function`
- Exposed via CLI: `dagger call function-name`
- Type-safe with SDK bindings
- Execute in containers for isolation

#### Dagger API Types
- `dagger.Container`: Running container with filesystem and processes
- `dagger.Directory`: Collection of files and directories
- `dagger.File`: Single file reference
- `dagger.Secret`: Sensitive value (never logged or cached)
- `dagger.Service`: Long-running service (databases, servers)
- `dagger.CacheVolume`: Persistent cache across runs

#### Dagger Engine
- GraphQL API server that orchestrates containers
- Manages caching and parallelization automatically
- Runs as a privileged container itself
- Communicates with SDK via Unix socket or TCP

### Homelab Context

This Daggerverse targets **homelab** environments, which typically include:
- Self-hosted infrastructure (bare metal, VMs, containers)
- Configuration management (Ansible, Terraform)
- Monitoring and observability tools
- Network services (DNS, DHCP, reverse proxies)
- Media servers, file sharing, backups
- Kubernetes or Docker Swarm clusters

Current modules address:
- **ansible**: Running Ansible playbooks and ad-hoc commands
- **ansible-lint**: Linting Ansible content for best practices

Future modules might include:
- Terraform/OpenTofu automation
- Docker Compose deployment
- Kubernetes manifest validation
- Backup and restore operations
- Network configuration validation
- Certificate management (Let's Encrypt)

## Important Constraints

### Technical Constraints

1. **Python 3.13+ Required**: All modules must specify `requires-python = ">=3.13"`
2. **Dagger Engine v0.19.3**: Pinned version across all modules (see `mise.toml`)
3. **Container Runtime Required**: Dagger needs Docker, Podman, or compatible OCI runtime
4. **SDK Embedding**: Each module embeds its own SDK in `sdk/` (no global installation)
5. **No Host Access by Default**: Functions don't have access to host filesystem, env vars, or network unless explicitly passed as arguments

### Development Constraints

1. **Reproducibility First**: All operations must be reproducible across different machines
2. **Stateless Functions**: Dagger functions should not rely on external state
3. **Idempotent Operations**: Functions should be safe to run multiple times
4. **Cache-Friendly**: Design functions to maximize cache hits (stable inputs → stable outputs)

### Security Constraints

1. **Secrets Management**: Never hardcode secrets; use `dagger.Secret` type
2. **Least Privilege**: Containers run with minimal permissions
3. **No Ambient Authority**: Functions can't access host resources without explicit grants
4. **Third-Party Modules**: Sandboxed execution prevents malicious code from accessing host

## External Dependencies

### Required External Services
- **GitHub**: Source code hosting and collaboration
- **OCI Registry** (optional): For publishing container images built by modules
- **Daggerverse** (optional): For publishing modules to the public registry

### Module Dependencies
- **Dagger Python SDK**: Embedded in each module (`sdk/`)
- **uv_build**: Build backend specified in `pyproject.toml`
- **Base Container Images**: Modules use public images (Alpine, Ubuntu, etc.)

### Development Dependencies
- **mise**: Install with `curl https://mise.run | sh` or via package manager
- **Git**: Standard version control
- **Docker/Podman**: Container runtime for Dagger Engine

## Workflow Examples

### Creating a New Module

```bash
# 1. Create module directory
mkdir <module-name>
cd <module-name>

# 2. Initialize Dagger module
dagger init --name=<module-name> --sdk=python

# 3. Set up development environment
dagger develop

# 4. Implement functions in src/<module-name>/main.py
# (Edit the file with your Dagger functions)

# 5. Test the module
dagger functions  # List available functions
dagger call <function-name> --arg=value  # Call a function
```

### Modifying an Existing Module

```bash
# 1. Navigate to module
cd <module-name>

# 2. Edit source code
vim src/<module-name>/main.py

# 3. Update SDK if structure changed
dagger develop

# 4. Test changes
dagger call <function-name> --arg=value
```

### Using Modules in CI/CD

```bash
# Call a module function from any directory
dagger call -m ./ansible run-playbook \
  --playbook=./playbooks/site.yml \
  --inventory=./inventory/hosts

# Chain multiple modules
dagger call -m ./ansible-lint lint \
  --directory=./ansible-content | \
dagger call -m ./slack notify \
  --message=-
```

## Key Resources

### Documentation
- [Dagger Documentation](https://docs.dagger.io)
- [Dagger Python SDK API](https://dagger-io.readthedocs.org)
- [Dagger Python SDK Source](https://github.com/dagger/dagger/tree/main/sdk/python)
- [Daggerverse](https://daggerverse.dev) - Public module registry

### Project Files
- `CLAUDE.md`: Detailed guidance for AI assistants
- `mise.toml`: Tool version management
- `openspec/AGENTS.md`: OpenSpec workflow documentation
- Module `dagger.json`: Module configuration
- Module `pyproject.toml`: Python dependencies

### Community
- [Dagger Discord](https://discord.gg/dagger-io)
- [Dagger GitHub](https://github.com/dagger/dagger)
