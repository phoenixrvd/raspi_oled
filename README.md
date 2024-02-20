# Raspi OLED

This project serves as a case study for a Raspberry Pi project, demonstrating the implementation of a complete application. The application must meet the following requirements:

| ID   | Requirement                                                                 |
|------|:----------------------------------------------------------------------------|
| A1.1 | The application must be written entirely in Python.                         |
| A1.2 | The display must show system information:                                   |
|      | - Time                                                                      |
|      | - IP address                                                                |
|      | - CPU load (Load average over the last 60 seconds)                          |
|      | - Available disk space                                                      |
|      | - CPU temperature                                                           |
| A1.3 | Development of the application must also be possible without real hardware. |
| A1.4 | The application must start automatically when the Raspberry Pi starts.      |
| A1.5 | The installation process must be automated.                                 |

As evident from the requirements, displaying system information on a display is the main functionality. However, a realistic application requires non-functional requirements beyond basic functionality, such as easy installation or the ability to develop the application locally (without real hardware) to reduce development time.

## Implementation

The implementation is based on the requirements from the requirements table. Each subsection addresses a requirement and describes its implementation.

### A1.1 - The application must be written entirely in Python.

The application was developed entirely in Python. As the system depends on several third-party libraries, `pipenv` was used to manage dependencies. This allows for installing the application in a virtual environment without overloading the developer's computer's operating system with Raspberry-specific packages. Dependencies are installed from the project directory with the command:

```shell
pipenv install
```

After installation, the application provides a CLI (Command Line Interface) that offers various commands for installation, maintenance, and testing. A complete list of commands and corresponding help can be displayed with the following command:

```shell
pipenv run python main.py --help
```

### A1.2 - The display must show system information.

A 128x64 pixel OLED display was used for the display. Communication with the display is done via the I2C interface, which is driven by the `luma.oled` library. Detailed information on the connections and the library can be found in the [Luma documentation](https://luma-oled.readthedocs.io/en/latest/).

The output is shown in the following image:

![Raspberry Pi OLED Display](./doc/preview.png)

### A1.3 - Development of the application must also be possible without real hardware.

To develop the application without real hardware, the `--emulate` flag was introduced. This makes it possible to save the display's output to an image file. Thus, the application can be developed without a Raspberry Pi and then deployed on the Raspberry Pi.

The emulation is started with the following command:

```shell
pipenv run python main.py --watch --emulate
```

### A1.4 - The application must start automatically when the Raspberry Pi starts.

It is important that in a monitoring application, hardware components start automatically after every system boot. Assuming that the Raspberry Pi uses a Debian-based operating system, there are several ways to automatically start the application. One way is to use `systemd` units. This makes troubleshooting easier with `journalctl` compared to cron.d if the application crashes in the background or fails to start.

### A1.5 - The installation process must be automated.

To deploy an application productively, often system-specific adjustments are necessary. In this case, it would be necessary to create and activate a `systemd` service, which, however, depends on the environment, such as the path to the Python installation or the application path. To simplify, a CLI command was provided that automates the installation and activation of the `systemd` service:

```shell
pipenv run sudo -E env PATH=$PATH python main.py --install
```

The uninstallation and deactivation of the `systemd` service is done with:

```shell
pipenv run sudo -E env PATH=$PATH python main.py --uninstall
```

It's also important to emphasize that the installation of services must be carried out with root rights. By using pipenv run sudo -E env PATH=$PATH, the Pipenv environment is passed to the installer. Thus, the installer knows where the Pipenv environment is located and will pass it on to the background process.

## Summary

This project demonstrates that in small applications, not only the provision of a main function is in focus but also the fulfillment of non-functional requirements that make the application practically usable.
