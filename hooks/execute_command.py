# Copyright (c) 2021 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Hook that handles excutement command line from within the Flame process.
"""

from __future__ import absolute_import
import sgtk

import os

HookBaseClass = sgtk.get_hook_baseclass()


class ExecuteCommandHooks(HookBaseClass):
    def use_flame_execute_command(self):
        """
        Flame 2022.2+ provides a way to run a command line through the
        Autodesk Flame Multi-Purpose Daemon. This way of starting new processes
        is better since any native python subprocess command (os.system,
        subprocess, Popen, etc) will call fork() which will duplicate the
        process resources before calling exec(). This can be costly especially
        for a process like Flame.

        Note: Environment variables will not be forwarded to the command
        executed automatically, use /usr/bin/env if we have any env var
        of interest defined by is_env_var_forwaded(). Because of that it is
        not enabled by default since it could break legacy workflows that
        would be dependent of env vars.
        """
        return os.environ.get("SHOTGUN_FLAME_USE_EXECUTE_COMMAND", False)

    def is_env_var_forwaded(self, env_var):
        """
        Query if an env var should be forward to a new command line process.

        :param env_var: Environement variable name
        """
        forwarded_env_vars = ["SSL_CERT_FILE", "SSL_CERT_DIR"]
        if env_var in forwarded_env_vars:
            return True

        forwarded_env_var_prefixes = ["SHOTGUN_", "TK_", "SGTK_", "TANK_"]
        for prefix in forwarded_env_var_prefixes:
            if env_var.startswith(prefix):
                return True

        return False

    def execute_command(self, command, shell=False):
        """
        Execute a command line subprocess.

        :param command: String or sequence of strings of the command to execute
                        with its arguments.
        :param shell: If true, the command will be executed through the shell.
        :return: A tuple with the (return code, stdout, stderr)
        """
        try:
            import flame

            if "execute_command" in dir(
                flame
            ) and sgtk.platform.current_engine().execute_hook_method(
                "execute_command_hooks", "use_flame_execute_command"
            ):

                env_vars = []
                for env_var in os.environ.items():
                    if sgtk.platform.current_engine().execute_hook_method(
                        "execute_command_hooks",
                        "is_env_var_forwaded",
                        env_var=env_var[0],
                    ):
                        env_vars.append("=".join(env_var))

                if isinstance(command, list):
                    command = " ".join(command)
                if env_vars:
                    command = "/usr/bin/env " + " ".join(env_vars) + " " + command

                return flame.execute_command(
                    command=command,
                    blocking=True,
                    shell=shell,
                    capture_stdout=True,
                    capture_stderr=True,
                )
        except ImportError:
            pass
        import subprocess

        process = subprocess.Popen(
            command if isinstance(command, list) else command.split(" "),
            stdout=subprocess.PIPE,
            shell=shell,
            close_fds=True,
        )
        stdout, stderr = process.communicate()
        stdout = stdout.decode("utf-8") if stdout else None
        stderr = stderr.decode("utf-8") if stderr else None
        rc = process.returncode
        return rc, stdout, stderr
