# Implementation Tasks

## 1. Ansible Module Core Functions

- [x] 1.1 Research and select appropriate Ansible container base image (e.g., `cytopia/ansible:latest-tools`, `ansible/ansible-runner`, or build custom)
- [x] 1.2 Implement `galaxy_install()` function to execute ansible-galaxy collection install in a directory
- [x] 1.3 Implement `run_playbook()` function with required parameters: `directory: dagger.Directory`, `playbook: str`
- [x] 1.4 Add optional `inventory: str` parameter to `run_playbook()` with conditional CLI argument building
- [x] 1.5 Add optional `extra_vars: list[str]` parameter to `run_playbook()` and generate multiple `--extra-vars` flags
- [x] 1.6 Add optional `tags: list[str]` parameter to `run_playbook()` and generate comma-separated `--tags` argument
- [x] 1.7 Remove placeholder functions (`container_echo`, `grep_dir`) from `ansible/src/ansible/main.py`
- [x] 1.8 Add comprehensive docstrings to all functions explaining parameters and return types
- [x] 1.9 Test functions manually with `dagger call` to verify basic functionality

## 2. Test Module Setup

- [x] 2.1 Create `ansible/tests/` directory
- [x] 2.2 Initialize test module: `cd ansible/tests && dagger init --name=tests --sdk=python --source=.`
- [x] 2.3 Install parent module: `cd ansible/tests && dagger install ..`
- [x] 2.4 Implement test in `ansible/tests/src/tests/main.py` for `galaxy_install()` function
- [x] 2.5 Implement test for `run_playbook()` with minimal playbook
- [x] 2.6 Implement test for `run_playbook()` with inventory parameter
- [x] 2.7 Implement test for `run_playbook()` with extra_vars parameter
- [x] 2.8 Implement test for `run_playbook()` with tags parameter
- [x] 2.9 Implement test for `run_playbook()` with all parameters combined
- [x] 2.10 Implement `all()` function that runs all tests sequentially
- [x] 2.11 Execute tests: `dagger call -m ansible/tests all`
- [x] 2.12 Fix any test failures and verify all tests pass

## 3. Example Module Setup

- [x] 3.1 Create `ansible/examples/python/` directory
- [x] 3.2 Initialize examples module: `cd ansible/examples/python && dagger init --name=examples/python --sdk=python --source=.`
- [x] 3.3 Install parent module: `cd ansible/examples/python && dagger install ../..`
- [x] 3.4 Implement example in `ansible/examples/python/src/examples/main.py` demonstrating `galaxy_install()`
- [x] 3.5 Implement example demonstrating `run_playbook()` with basic usage
- [x] 3.6 Implement example demonstrating `run_playbook()` with advanced parameters (inventory, vars, tags)
- [x] 3.7 Test examples manually: `dagger call -m ansible/examples/python <example-function-name>`
- [x] 3.8 Verify examples produce expected output and serve as clear usage demonstrations

## 4. Documentation and Validation

- [x] 4.1 Update module docstrings to ensure they are clear and helpful for CLI `--help` output
- [x] 4.2 Verify all Dagger functions have proper type hints and follow naming conventions
- [x] 4.3 Run `dagger functions` to list all exposed functions and verify they appear correctly
- [x] 4.4 Create sample playbook directory for testing (can be minimal, ephemeral)
- [x] 4.5 Validate end-to-end workflow: install galaxy collections, then run a playbook
- [x] 4.6 Mark all tasks in this file as `[x]` when completed

## Dependencies and Parallelization

- **Sequential**: Tasks must be completed in order within each section
- **Parallelizable**: Sections 2 (Test Module) and 3 (Example Module) can be worked on in parallel after Section 1.9 is complete
- **Blockers**: Section 4 depends on completion of Sections 1, 2, and 3
