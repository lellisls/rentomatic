import os
import tempfile

import pytest
import yaml


@pytest.fixture(scope='session')
def docker_setup(docker_ip):
    return {
        'mongo': {
            'dbname': 'rentomaticdb',
            'user': 'root',
            'password': 'rentomaticdb',
            'host': docker_ip
        },
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
            },
            'mongo': {
                'restart': 'always',
                'image': 'mongo',
                'ports': ["27017:27017"],
                'environment': [
                    f'MONGO_INITDB_ROOT_USERNAME={docker_setup["mongo"]["user"]}',
                    f'MONGO_INITDB_ROOT_PASSWORD={docker_setup["mongo"]["password"]}'
                ]
            }
        }
    }
    f = os.fdopen(docker_tmpfile[0], 'w')
    f.write(yaml.dump(content))
    f.close()

    return docker_tmpfile[1]
