import subprocess
import sys

from pathlib import Path


class SystemCtl(object):
    def __init__(self, service_name: str):
        self._service_name = service_name
        self._subprocess = subprocess

    def _run(self, command: str) -> None:
        full_command = ['systemctl', command, self._service_name]
        self._subprocess.run(full_command)

    def start(self) -> None:
        self._run('start')

    def stop(self) -> None:
        self._run('stop')

    def enable(self) -> None:
        self._run('enable')

    def disable(self) -> None:
        self._run('disable')

    def reload(self) -> None:
        self._subprocess.run(['systemctl', 'daemon-reload'])

    def install(self):
        self.reload()
        self.enable()
        self.start()

    def uninstall(self):
        self.stop()
        self.disable()


class SystemdService:
    def __init__(self, name: str):
        self._system_ctl = SystemCtl(service_name=name)

        self._name = name
        self._project_path = Path.cwd()

        service_file_name = f'{name}.service'
        self._unit_file = Path(self._project_path / service_file_name)
        self._unit_link = Path(f'/etc/systemd/system/{service_file_name}')

    def install(self, execution_args: str) -> None:
        service_content = f"""[Unit]
        Description={self._name.capitalize()}
        After=network.target

        [Service]
        WorkingDirectory={self._project_path}
        ExecStart={sys.executable} {execution_args}
        Restart=always

        [Install]
        WantedBy=multi-user.target
        """.replace('\t', '').replace('        ', '')

        self._unit_file.write_text(service_content)
        if not self._unit_link.exists():
            self._unit_link.symlink_to(self._unit_file)

        self._system_ctl.install()

    def uninstall(self) -> None:
        if self._unit_link.exists():
            self._system_ctl.uninstall()
            self._system_ctl.reload()

        if self._unit_link.exists():
            self._unit_link.unlink()

        if self._unit_file.exists():
            self._unit_file.unlink()
