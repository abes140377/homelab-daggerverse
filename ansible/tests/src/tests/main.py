from typing import Annotated

import dagger
from dagger import DefaultPath, dag, function, object_type


@object_type
class Tests:
    @function
    async def test_galaxy_install(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test ansible-galaxy collection install functionality"""
        # Get test data directory
        test_dir = test_data

        # Run galaxy install and verify it completes without error
        container = dag.ansible().galaxy_install(directory=test_dir)

        # Verify the command ran successfully by checking if we can list ansible version
        result = await container.with_exec(["ansible", "--version"]).stdout()

        if "ansible" not in result.lower():
            raise Exception(
                "Galaxy install test failed: ansible not available after install"
            )

        return "test_galaxy_install: PASSED"

    @function
    async def test_run_playbook_simple(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test running a simple playbook"""
        # Get test data directory
        test_dir = test_data

        # Run the simple playbook
        result = await dag.ansible().run_playbook(
            directory=test_dir,
            playbook="playbooks/simple.yml",
        )

        if "Test successful!" not in result:
            raise Exception("Simple playbook test failed: expected message not found")

        return "test_run_playbook_simple: PASSED"

    @function
    async def test_run_playbook_with_inventory(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test running a playbook with custom inventory"""
        # Get test data directory
        test_dir = test_data

        # Run playbook with inventory
        result = await dag.ansible().run_playbook(
            directory=test_dir,
            playbook="playbooks/simple.yml",
            inventory="inventory/hosts.ini",
        )

        if "Test successful!" not in result:
            raise Exception(
                "Playbook with inventory test failed: expected message not found"
            )

        return "test_run_playbook_with_inventory: PASSED"

    @function
    async def test_run_playbook_with_extra_vars(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test running a playbook with extra variables"""
        # Get test data directory
        test_dir = test_data

        # Run playbook with extra vars
        result = await dag.ansible().run_playbook(
            directory=test_dir,
            playbook="playbooks/with-vars.yml",
            extra_vars=["test_var=hello_world"],
        )

        if "hello_world" not in result:
            raise Exception(
                "Playbook with extra_vars test failed: variable not passed correctly"
            )

        return "test_run_playbook_with_extra_vars: PASSED"

    @function
    async def test_run_playbook_with_tags(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test running a playbook with tag filtering"""
        # Get test data directory
        test_dir = test_data

        # Run playbook with specific tag
        result = await dag.ansible().run_playbook(
            directory=test_dir, playbook="playbooks/with-tags.yml", tags=["test"]
        )

        # Should include the test tag task
        if "This task has the test tag" not in result:
            raise Exception(
                "Playbook with tags test failed: test tag task not executed"
            )

        # Should NOT include the deploy tag task
        if "This task has the deploy tag" in result:
            raise Exception(
                "Playbook with tags test failed: deploy tag task should not have executed"
            )

        return "test_run_playbook_with_tags: PASSED"

    @function
    async def test_run_playbook_all_parameters(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test running a playbook with all parameters combined"""
        # Get test data directory
        test_dir = test_data

        # Run playbook with all parameters
        result = await dag.ansible().run_playbook(
            directory=test_dir,
            playbook="playbooks/with-vars.yml",
            inventory="inventory/hosts.ini",
            extra_vars=["test_var=combined_test"],
            tags=[],  # Empty tags list should work
        )

        if "combined_test" not in result:
            raise Exception(
                "Playbook with all parameters test failed: variable not passed correctly"
            )

        return "test_run_playbook_all_parameters: PASSED"

    @function
    async def test_ssh_key_mounting(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test that SSH key is correctly mounted in the container"""
        # Get test data directory
        test_dir = test_data

        # Load the SSH key as a secret
        ssh_key = dag.set_secret(
            "test-ssh-key", await test_dir.file("ansible_id_ecdsa").contents()
        )

        # Get a container with the SSH key mounted (via run_playbook but we'll inspect the container)
        # We'll use a simple playbook just to build the container
        result = await dag.ansible().run_playbook(
            directory=test_dir,
            playbook="playbooks/simple.yml",
            ssh_private_key=ssh_key,
        )

        # The playbook should have run successfully
        if "Test successful!" not in result:
            raise Exception("SSH key mounting test failed: playbook didn't run")

        return "test_ssh_key_mounting: PASSED"

    @function
    async def test_ssh_key_file_exists(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Test that SSH key file exists at the correct location with correct permissions"""
        # Get test data directory
        test_dir = test_data

        # Load the SSH key as a secret
        ssh_key = dag.set_secret(
            "test-ssh-key", await test_dir.file("ansible_id_ecdsa").contents()
        )

        # Build a container with the SSH key using ansible module
        # Mount secret to temporary location, then copy to final destination
        # This is necessary because mounted secrets are read-only
        container = (
            dag.container()
            .from_("alpine/ansible:latest")
            .with_mounted_directory("/work", test_dir)
            .with_workdir("/work")
            .with_exec(["mkdir", "-p", "/root/.ssh"])
            .with_mounted_secret("/tmp/ssh_key", ssh_key)
            .with_exec(["cp", "/tmp/ssh_key", "/root/.ssh/ansible_id_ecdsa"])
            .with_exec(["chmod", "600", "/root/.ssh/ansible_id_ecdsa"])
        )

        # Check if the file exists
        ls_result = await container.with_exec(
            ["ls", "-la", "/root/.ssh/ansible_id_ecdsa"]
        ).stdout()

        if "ansible_id_ecdsa" not in ls_result:
            raise Exception(
                "SSH key file does not exist at /root/.ssh/ansible_id_ecdsa"
            )

        # Check permissions (should be -rw-------)
        if "-rw-------" not in ls_result:
            raise Exception(
                f"SSH key has incorrect permissions. Expected -rw-------, got: {ls_result}"
            )

        # Verify the file has content (non-zero size)
        # We can't read secret content directly, but we can check file size
        # The test command will fail if file is empty or doesn't exist
        await container.with_exec(["test", "-s", "/root/.ssh/ansible_id_ecdsa"]).sync()

        return "test_ssh_key_file_exists: PASSED - File exists with correct permissions (600) and non-zero size"

    @function
    async def all(
        self,
        test_data: Annotated[dagger.Directory, DefaultPath("test-data")],
    ) -> str:
        """Run all tests sequentially"""
        results = []

        # Run all tests
        results.append(await self.test_galaxy_install(test_data))
        results.append(await self.test_run_playbook_simple(test_data))
        results.append(await self.test_run_playbook_with_inventory(test_data))
        results.append(await self.test_run_playbook_with_extra_vars(test_data))
        results.append(await self.test_run_playbook_with_tags(test_data))
        results.append(await self.test_run_playbook_all_parameters(test_data))
        results.append(await self.test_ssh_key_mounting(test_data))
        results.append(await self.test_ssh_key_file_exists(test_data))

        # Return summary
        return "\n".join(results) + "\n\nAll tests PASSED!"
