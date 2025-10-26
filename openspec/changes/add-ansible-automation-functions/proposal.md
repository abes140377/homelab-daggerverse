# Proposal: Add Ansible Automation Functions

## Why

The current Ansible Dagger module only contains placeholder functions (`container_echo` and `grep_dir`) that don't provide actual Ansible automation capabilities. To enable homelab automation workflows, we need to implement core Ansible functionality including playbook execution, galaxy collection management, and comprehensive testing capabilities.

## What Changes

- **Add ansible-galaxy command execution** - Enable installation of Ansible collections and roles from a playbook directory
- **Add ansible-playbook execution** - Enable running Ansible playbooks with configurable parameters:
  - Playbook file selection
  - Inventory file specification
  - Extra variables (key=value pairs)
  - Tag filtering
- **Add test module** - Implement a `tests/` subdirectory with Dagger test functions following best practices
- **Add example module** - Create `examples/python/` subdirectory showcasing usage patterns

## Impact

- **Affected specs**: `ansible-automation` (new capability)
- **Affected code**:
  - `ansible/src/ansible/main.py` - Replace placeholder functions with Ansible automation functions
  - `ansible/tests/` - New test module directory
  - `ansible/examples/python/` - New examples directory
- **Breaking changes**: None (module is newly created and placeholder functions will be replaced)
