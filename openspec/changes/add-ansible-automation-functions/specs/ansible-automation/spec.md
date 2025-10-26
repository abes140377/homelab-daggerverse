# Ansible Automation Capability

## ADDED Requirements

### Requirement: Ansible Galaxy Collection Installation

The Ansible module SHALL provide a function to execute ansible-galaxy commands in a playbook directory, enabling installation of collections and roles.

#### Scenario: Install collections from requirements file

- **WHEN** a playbook directory contains a `requirements.yml` or `collections/requirements.yml` file
- **THEN** the function executes `ansible-galaxy collection install -r requirements.yml` in the directory
- **AND** returns a Container with the installed collections

#### Scenario: Install collections in custom directory

- **WHEN** provided with a playbook directory parameter
- **THEN** the function mounts the directory into a container with Ansible installed
- **AND** executes ansible-galaxy commands within that mounted directory context

### Requirement: Ansible Playbook Execution

The Ansible module SHALL provide a function to execute ansible-playbook commands with configurable parameters including playbook selection, inventory, variables, and tags.

#### Scenario: Execute playbook with default settings

- **WHEN** provided with a playbook directory and a playbook filename
- **THEN** the function executes `ansible-playbook <playbook>` in the directory
- **AND** returns the execution output as a string

#### Scenario: Execute playbook with custom inventory

- **WHEN** provided with a playbook, inventory file path, and playbook directory
- **THEN** the function executes `ansible-playbook -i <inventory> <playbook>`
- **AND** uses the specified inventory file from the directory

#### Scenario: Execute playbook with extra variables

- **WHEN** provided with a playbook and an array of extra variables in `key=value` format
- **THEN** the function executes `ansible-playbook --extra-vars <key1=value1> --extra-vars <key2=value2> <playbook>`
- **AND** passes all variables to the playbook execution

#### Scenario: Execute playbook with tag filtering

- **WHEN** provided with a playbook and an array of tags
- **THEN** the function executes `ansible-playbook --tags <tag1>,<tag2>,<tag3> <playbook>`
- **AND** only runs tasks matching the specified tags

#### Scenario: Execute playbook with combined parameters

- **WHEN** provided with playbook, inventory, extra variables, and tags
- **THEN** the function executes `ansible-playbook -i <inventory> --extra-vars <vars> --tags <tags> <playbook>`
- **AND** applies all parameters in a single execution

### Requirement: Container Base Image

The Ansible module SHALL use an appropriate base container image that includes Ansible and its dependencies.

#### Scenario: Use official Ansible container image

- **WHEN** executing Ansible commands
- **THEN** the module uses a container image with Ansible pre-installed (e.g., `cytopia/ansible:latest-tools` or similar)
- **AND** the image includes ansible-playbook and ansible-galaxy binaries

#### Scenario: Ensure Python runtime availability

- **WHEN** executing Ansible commands
- **THEN** the container image includes Python 3.x runtime required by Ansible
- **AND** includes common Ansible dependencies (jinja2, PyYAML, etc.)

### Requirement: Directory Mounting

The Ansible module SHALL accept a playbook directory as a Dagger Directory type and mount it appropriately for Ansible execution.

#### Scenario: Mount playbook directory

- **WHEN** provided with a playbook directory parameter of type `dagger.Directory`
- **THEN** the function mounts the directory into the container at a predictable path (e.g., `/work`)
- **AND** sets the working directory to the mounted path before executing Ansible commands

#### Scenario: Preserve directory permissions

- **WHEN** mounting a playbook directory
- **THEN** the mounted directory preserves file permissions needed for Ansible execution
- **AND** inventory files, playbooks, and variable files remain readable

### Requirement: Test Module Implementation

The Ansible module SHALL include a test module following Dagger best practices to validate module functionality.

#### Scenario: Test module structure

- **WHEN** the module is developed
- **THEN** a `tests/` subdirectory exists with its own Dagger module configuration
- **AND** the tests module is initialized with `dagger init --name=tests --sdk=python --source=.`
- **AND** the tests module installs the parent Ansible module via `dagger install ..`

#### Scenario: Test functions validate behavior

- **WHEN** test functions are executed
- **THEN** each test function calls the Ansible module functions via `dag.ansible()`
- **AND** validates expected behavior by checking return values
- **AND** raises exceptions when validation fails

#### Scenario: All-tests runner function

- **WHEN** the test module is implemented
- **THEN** an `all()` function exists that runs all test functions
- **AND** the function can be executed with `dagger call -m tests all`

### Requirement: Example Module Implementation

The Ansible module SHALL include example modules showcasing practical usage patterns.

#### Scenario: Python examples module structure

- **WHEN** the module is developed
- **THEN** an `examples/python/` subdirectory exists with its own Dagger module configuration
- **AND** the examples module is initialized with `dagger init --name=examples/python --sdk=python --source=.`
- **AND** the examples module installs the parent Ansible module via `dagger install ../..`

#### Scenario: Examples demonstrate real usage

- **WHEN** example functions are implemented
- **THEN** each example demonstrates a practical use case (e.g., installing galaxy collections, running a simple playbook)
- **AND** examples are executable and produce visible output
- **AND** examples serve as living documentation for module users
