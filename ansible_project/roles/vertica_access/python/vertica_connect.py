import argparse
import datetime
import importlib
import logging
import os
import subprocess
import sys
import coloredlogs
import vertica_python

from enum import Enum

import boto3
from smart_open import smart_open
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Vertica_Access")
coloredlogs.install(level=logging.INFO, format="%(asctime)s [%(name)s] %(level)s %(message)s'")

class Database:
    def __init__(self, *, host: str, port: str, name: str, user: str, password: str):
        self.host = host
        self.port = port
        self.name = name
        self.user = user
        self.password = password

    def vsql(self, args):
        return vsql(database=self, args=args)


def check_executable(executable: str):
    """Check that executable exists on $PATH."""
    try:
        subprocess.run(
            [
                "which",
                executable,
            ],  # 'command -v' doesn't work in our Jenkins environment
            stdout=subprocess.PIPE,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.info("Could not find {}\n{}".format(executable, sys.stderr))
        sys.exit(1)

def vsql(*, database: Database, args: list):
    """Run vsql with some arguments against the provided database."""
    # WARNING: vsql does not always return non-zero code when there is an error! *sob*
    #          Bug filed with Vertica as VER-43593.
    r = subprocess.run(
        [
            "vsql",
            "-U",
            database.user,
            "-w",
            database.password,
            "-d",
            database.name,
            "-h",
            database.host,
            "-m",
            "require",
            *args,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if r.returncode != 0 or b"ERROR" in r.stderr:
        # This is our way of bubbling up *some* sort of signal if something seems off.
        # We'll sometimes get here in cases where vsql returns a zero exit code but
        # reports an error via stderr. :/
        # logger.info(r.stdout.decode('utf-8'))
        # logger.info('{}\n{}'.format(r.stderr.decode('utf-8'), sys.stderr))
        logger.info("vsql raised an error")
        logger.info("ERROR: {}".format(r.stderr.decode("utf-8")))
        raise Exception(r.stderr)

    return r

