# Ansible Dagger Module - Python Examples

This directory contains Python examples demonstrating how to use the Ansible Dagger module.

## Available Examples

### 1. Galaxy Install Example
**Function:** `galaxy-install-example`

Demonstrates how to install both Ansible Galaxy collections and roles from a `requirements.yml` file.

```bash
dagger call -m examples/python galaxy-install-example
```

**What it does:**
- Installs collections and roles from requirements.yml
- Shows Ansible version
- Lists all installed collections
- Lists all installed roles

---

### 2. Simple Playbook Example
**Function:** `simple-playbook-example`

Shows the most basic usage of running an Ansible playbook.

```bash
dagger call -m examples/python simple-playbook-example
```

**What it does:**
- Runs a simple "Hello World" playbook
- Demonstrates minimal configuration

---

### 3. Advanced Playbook Example
**Function:** `advanced-playbook-example`

Demonstrates advanced playbook execution with multiple parameters.

```bash
dagger call -m examples/python advanced-playbook-example
```

**What it does:**
- Uses a custom inventory file
- Passes extra variables at runtime
- Filters tasks using tags
- Shows all parameters working together

---

### 4. Playbook with Galaxy Collections Example
**Function:** `playbook-with-galaxy-collections-example`

Shows automatic installation of Galaxy collections and roles before playbook execution.

```bash
dagger call -m examples/python playbook-with-galaxy-collections-example
```

**What it does:**
- Automatically installs dependencies from requirements.yml
- Runs the playbook with all dependencies available
- Demonstrates the `requirements_file` parameter

---

### 5. Playbook with Roles Example
**Function:** `playbook-with-roles-example`

Demonstrates verification of installed Ansible roles.

```bash
dagger call -m examples/python playbook-with-roles-example
```

**What it does:**
- Installs roles from requirements.yml
- Verifies that roles are correctly installed
- Uses Ansible assertions to validate role availability
- Shows role installation status

---

### 6. List Installed Roles Example
**Function:** `list-installed-roles-example`

Shows how to inspect installed roles after galaxy install.

```bash
dagger call -m examples/python list-installed-roles-example
```

**What it does:**
- Displays the requirements.yml content
- Lists all installed roles with versions
- Helps verify what was installed

---

## Example Data Structure

```
example-data/
├── requirements.yml          # Galaxy collections and roles
├── inventory/
│   └── hosts.ini            # Ansible inventory file
└── playbooks/
    ├── hello.yml            # Simple hello world playbook
    ├── advanced.yml         # Playbook with tags and variables
    └── with-role.yml        # Playbook that verifies installed roles
```

## Requirements File Format

The `requirements.yml` file supports both collections and roles:

```yaml
---
collections:
  - name: community.general
    version: ">=3.0.0"

roles:
  - name: geerlingguy.docker
    version: 7.4.1
  - name: geerlingguy.pip
    version: 3.0.0
```

## Key Features Demonstrated

✅ **Galaxy Collections Installation** - Install Ansible collections from Galaxy
✅ **Galaxy Roles Installation** - Install Ansible roles from Galaxy
✅ **Simple Playbook Execution** - Run basic playbooks
✅ **Advanced Parameters** - Use inventory, variables, and tags
✅ **Automatic Dependency Installation** - Install requirements before running playbooks
✅ **Role Verification** - Validate that roles are correctly installed

## Running All Examples

You can run any example using:

```bash
# From the ansible module directory
cd ansible

# Run a specific example
dagger call -m examples/python <function-name>

# List all available examples
dagger functions -m examples/python
```

## Learn More

For production usage and more details, see the main Ansible module documentation.
