import dagger
from dagger import dag, function, object_type


@object_type
class Ansible:
    @function
    def galaxy_install(
        self,
        directory: dagger.Directory,
        requirements_file: str = "requirements.yml",
    ) -> dagger.Container:
        """Install Ansible Galaxy collections from a requirements file.

        Args:
            directory: Directory containing the Ansible playbook and requirements file
            requirements_file: Path to the requirements file (default: requirements.yml)

        Returns:
            A container with the collections installed
        """
        return (
            dag.container()
            .from_("alpine/ansible:latest")
            .with_mounted_directory("/work", directory)
            .with_workdir("/work")
            .with_exec(
                ["ansible-galaxy", "collection", "install", "-r", requirements_file]
            )
        )

    @function
    async def run_playbook(
        self,
        directory: dagger.Directory,
        playbook: str,
        inventory: str = "",
        extra_vars: list[str] | None = None,
        tags: list[str] | None = None,
        ssh_private_key: dagger.Secret | None = None,
        requirements_file: str = "",
    ) -> str:
        """Execute an Ansible playbook with optional parameters.

        Args:
            directory: Directory containing the Ansible playbook
            playbook: Path to the playbook file (relative to directory)
            inventory: Path to inventory file (optional)
            extra_vars: List of extra variables in key=value format (optional)
            tags: List of tags to filter tasks (optional)
            ssh_private_key: SSH private key for SSH connections (optional)
            requirements_file: Path to requirements file for galaxy collections (optional)

        Returns:
            The stdout output from the playbook execution
        """
        # Start building the command
        cmd = ["ansible-playbook"]

        # Add inventory if provided
        if inventory:
            cmd.extend(["-i", inventory])

        # Add extra vars if provided
        if extra_vars:
            for var in extra_vars:
                cmd.extend(["--extra-vars", var])

        # Add tags if provided
        if tags:
            cmd.extend(["--tags", ",".join(tags)])

        # Add the playbook file
        cmd.append(playbook)

        # Build the container - use galaxy_install if requirements file is provided
        if requirements_file:
            container = self.galaxy_install(directory, requirements_file)
        else:
            container = (
                dag.container()
                .from_("alpine/ansible:latest")
                .with_mounted_directory("/work", directory)
                .with_workdir("/work")
            )

        # Mount SSH key if provided
        if ssh_private_key:
            # Mount secret to temporary location, then copy to final destination
            # This is necessary because mounted secrets are read-only
            container = (
                container.with_exec(["mkdir", "-p", "/root/.ssh"])
                .with_mounted_secret("/tmp/ssh_key", ssh_private_key)
                .with_exec(["cp", "/tmp/ssh_key", "/root/.ssh/ansible_id_ecdsa"])
                .with_exec(["chmod", "600", "/root/.ssh/ansible_id_ecdsa"])
            )

        # Execute the playbook
        return await container.with_exec(cmd).stdout()
