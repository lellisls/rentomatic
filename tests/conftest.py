import os
import tempfile

import pytest
import yaml

from rentomatic.app import create_app
from rentomatic.flask_settings import TestConfig


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )


@pytest.yield_fixture(scope='function')
def app():
    return create_app(TestConfig)


@pytest.fixture(scope='session')
def docker_setup(docker_ip):
    return {
        'postgres': {
            'dbname': 'rentomaticdb',
            'user': 'postgres',
            'password': 'rentomaticdb',
            'port': 15432,
            'host': docker_ip
        }
    }


@pytest.fixture(scope='session')
def docker_tmpfile():
    f = tempfile.mkstemp()
    yield f
    os.remove(f[1])


@pytest.fixture(scope='session')
def docker_compose_file(docker_tmpfile, docker_setup):
    content = {
        'version': '3.1',
        'services': {
            'postgresql': {
                'restart': 'always',
                'image': 'postgres',
                'ports': [f'{docker_setup["postgres"]["port"]}:5432'],
                'environment': [
                    f'POSTGRES_PASSWORD={docker_setup["postgres"]["password"]}'
                ]
            }
        }
    }
    f = os.fdopen(docker_tmpfile[0], 'w')
    f.write(yaml.dump(content))
    f.close()
    return docker_tmpfile[1]


def pytest_addoption(parser):
    parser.addoption("--integration", action="store_true",
                     help="run integration tests")


def pytest_runtest_setup(item):
    if 'integration' in item.keywords and not item.config.getvalue("integration"):
        pytest.skip("need --integration option to run")
