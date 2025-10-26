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
        """Example: Install Ansible Galaxy collections from a requirements file.

        This example demonstrates how to use the galaxy_install function to install
        Ansible collections specified in a requirements.yml file.
        """
        # Install collections from requirements.yml
        container = dag.ansible().galaxy_install(
            directory=example_data,
            requirements_file="requirements.yml"
        )

        # Verify ansible is available
        result = await container.with_exec(["ansible", "--version"]).stdout()

        return f"Galaxy collections installed successfully!\n\nAnsible version:\n{result}"

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
            directory=example_data,
            playbook="playbooks/hello.yml"
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
            tags=["info"]  # Only run tasks tagged with 'info'
        )

        return f"Advanced playbook execution with inventory, vars, and tags:\n\n{result}"
