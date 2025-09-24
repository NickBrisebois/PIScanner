#!/usr/bin/env python3

import os
import sys
import venv

import argparse

SERVICE_FILE = """
[Unit]
Description=PIScanner Service
After=network.target

[Service]
Type=simple
ExecStart={venv_dir}/bin/python3 -m piscanner_client --server-uri=http://192.168.100.205:8000
Restart=always

[Install]
WantedBy=multi-user.target
"""

def install_systemd_service(venv_dir: str):
    with open("/etc/systemd/system/piscanner.service", "w") as f:
        _ = f.write(SERVICE_FILE.format(venv_dir=venv_dir))

    _ = os.system("systemctl daemon-reload")
    _ = os.system("systemctl enable piscanner.service")
    _ = os.system("systemctl start piscanner.service")


def build_and_install(venv_dir: str):
    print("Creating virtual environment at", venv_dir)
    venv.create(venv_dir, with_pip=True)

    print("Installing build dependencies")
    _ = os.system(f"{venv_dir}/bin/python -m pip install build")

    print("Building...")
    _ = os.system(f"{venv_dir}/bin/python -m build")

    print("Installing...")
    _ = os.system(f"{venv_dir}/bin/pip install --force-reinstall dist/*.whl")


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root.")
        sys.exit(1)

    if not os.path.exists("/etc/systemd/system"):
        print("piscanner_client requires systemd")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Install PIScanner client")
    _ = parser.add_argument("--install-dir", type=str, default="/opt/piscanner_client", help="Where to install the PIScanner client script")
    args = parser.parse_args()

    install_dir: str = args.install_dir
    venv_dir = os.path.join(install_dir, "venv")
    build_and_install(venv_dir=venv_dir)

    install_systemd_service(venv_dir=venv_dir)
