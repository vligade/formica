import json
import yaml
import pytest
from path import Path

from formica import cli


@pytest.fixture
def logger(mocker):
    return mocker.patch('formica.cli.logger')


def test_template_calls_template(tmpdir, logger):
    with Path(tmpdir):
        with open('test.template.json', 'w') as f:
            f.write('{"Description": "{{ \'test\' | title }}"}')
        cli.main(['template'])
        logger.info.assert_called()
        assert {"Description": "Test"} == json.loads(logger.info.call_args[0][0])


def test_template_calls_template_with_yaml(tmpdir, logger):
    with Path(tmpdir):
        with open('test.template.json', 'w') as f:
            f.write('{"Description": "{{ \'test\' | title }}"}')
        cli.main(['template', '--yaml'])
        logger.info.assert_called()
        assert {"Description": "Test"} == yaml.load(logger.info.call_args[0][0])
