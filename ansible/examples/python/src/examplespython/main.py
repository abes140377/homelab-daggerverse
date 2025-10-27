from typing import Annotated

import dagger
from dagger import DefaultPath, dag, function, object_type


@object_type
class Examplespython:
    @function
    async def galaxy_install_example(
        self,
        example_data: Annotated[dagger.Directory, DefaultPath("example-data")],
    ) -> str:
        """Example: Install Ansible Galaxy collections and roles from a requirements file.

        This example demonstrates how to use the galaxy_install function to install
        both Ansible collections and roles specified in a requirements.yml file.
        """
        # Install collections and roles from requirements.yml
        container = dag.ansible().galaxy_install(
            directory=example_data, requirements_file="requirements.yml"
        )

        # Verify ansible is available
        ansible_version = await container.with_exec(["ansible", "--version"]).stdout()

        # List installed collections
        collections = await container.with_exec(
            ["ansible-galaxy", "collection", "list"]
        ).stdout()

        # List installed roles
        roles = await container.with_exec(["ansible-galaxy", "role", "list"]).stdout()

        return f"""Galaxy collections and roles installed successfully!

Ansible version:
{ansible_version}

Installed collections:
{collections}

Installed roles:
{roles}
"""

    @function
    async def simple_playbook_example(
        self,
        example_data: Annotated[dagger.Directory, DefaultPath("example-data")],
    ) -> str:
        """Example: Run a simple Ansible playbook.

        This example shows the basic usage of run_playbook to execute
        a simple playbook that prints a hello message.
        """
        # Run the simple hello playbook
        result = await dag.ansible().run_playbook(
            directory=example_data, playbook="playbooks/hello.yml"
        )

        return f"Simple playbook execution:\n\n{result}"

    @function
    async def advanced_playbook_example(
        self,
        example_data: Annotated[dagger.Directory, DefaultPath("example-data")],
    ) -> str:
        """Example: Run a playbook with inventory, variables, and tags.

        This example demonstrates advanced usage with all available parameters:
        - Custom inventory file
        - Extra variables for runtime configuration
        - Tag filtering to run specific tasks
        """
        # Run playbook with all parameters
        result = await dag.ansible().run_playbook(
            directory=example_data,
            playbook="playbooks/advanced.yml",
            inventory="inventory/hosts.ini",
            extra_vars=["environment=production", "app_version=2.1.0"],
            tags=["info"],  # Only run tasks tagged with 'info'
        )

        return (
            f"Advanced playbook execution with inventory, vars, and tags:\n\n{result}"
        )

    @function
    async def playbook_with_galaxy_collections_example(
        self,
        example_data: Annotated[dagger.Directory, DefaultPath("example-data")],
    ) -> str:
        """Example: Run a playbook with automatic Galaxy collection and role installation.

        This example demonstrates how to automatically install required Ansible
        Galaxy collections and roles before running a playbook using the requirements_file parameter.
        """
        # Run playbook with requirements file - collections and roles will be installed automatically
        result = await dag.ansible().run_playbook(
            directory=example_data,
            playbook="playbooks/hello.yml",
            requirements_file="requirements.yml",
        )

        return f"Playbook execution with Galaxy collections and roles:\n\n{result}"

    @function
    async def playbook_with_roles_example(
        self,
        example_data: Annotated[dagger.Directory, DefaultPath("example-data")],
    ) -> str:
        """Example: Run a playbook that verifies installed Ansible roles.

        This example demonstrates:
        1. Automatic installation of roles from requirements.yml
        2. Verification that roles are correctly installed
        3. Using assertions to ensure role availability
        """
        # Run playbook that checks for installed roles
        result = await dag.ansible().run_playbook(
            directory=example_data,
            playbook="playbooks/with-role.yml",
            requirements_file="requirements.yml",
        )

        return f"Playbook execution with role verification:\n\n{result}"

    @function
    async def list_installed_roles_example(
        self,
        example_data: Annotated[dagger.Directory, DefaultPath("example-data")],
    ) -> str:
        """Example: List all installed Ansible roles after galaxy install.

        This example shows how to inspect what roles have been installed
        from the requirements.yml file.
        """
        # Install roles and collections
        container = dag.ansible().galaxy_install(
            directory=example_data, requirements_file="requirements.yml"
        )

        # List all installed roles with details
        roles_list = await container.with_exec(
            ["ansible-galaxy", "role", "list"]
        ).stdout()

        # Show the requirements file content for reference
        requirements_content = await example_data.file("requirements.yml").contents()

        return f"""Installed Ansible Roles:

Requirements file (requirements.yml):
{requirements_content}

Installed roles:
{roles_list}
"""
