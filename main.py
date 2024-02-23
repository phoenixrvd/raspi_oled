#!/usr/bin/env python3

import argparse

from install import SystemdService
from monitor import Monitor


def main() -> None:
    parser = argparse.ArgumentParser(description='Run the monitor')
    parser.add_argument('--emulate', action='store_true', help='Run in emulation mode. Save the output into preview.png')
    parser.add_argument('--watch', action='store_true', help='Run the update loop')
    parser.add_argument('--interval', type=float, default=10, help='Interval in seconds between updates on watch mode')
    parser.add_argument('--install', action='store_true', help='Install the program as a service')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall the program as a service')
    parser.add_argument('--device', type=str, default='ssd1306', help='The device driver to use')
    args = parser.parse_args()

    service_name = 'display-sh1106'

    if args.install:
        execution_args = ['main.py --watch']

        if args.interval:
            execution_args.append(f'--interval {args.interval}')
        if args.emulate:
            execution_args.append('--emulate')
        if args.device:
            execution_args.append(f'--device {args.device}')

        SystemdService(name=service_name).install(' '.join(execution_args))
    elif args.uninstall:
        SystemdService(name=service_name).uninstall()
    elif args.watch:
        Monitor(emulator=args.emulate, device=args.device).watch(args.interval)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
