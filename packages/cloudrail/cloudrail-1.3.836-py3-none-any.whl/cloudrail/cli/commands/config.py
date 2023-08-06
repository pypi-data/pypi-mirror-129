import os

import click

from cloudrail.cli.cli_configuration import CliConfiguration
from cloudrail.cli.commands_utils import safe_invoke, echo_error, exit_with_code
from cloudrail.cli.exit_codes import ExitCode


@click.group(short_help='Review or clear the Cloudrail configuration stored locally on this machine.',
             help='Review or clear the Cloudrail configuration stored locally on this machine.')
def config():
    check_indeni_mount()


@click.command(name='set',
               short_help='Persist a setting, such as API key or API endpoint, to be used in future executions.',
               help='Persist a setting, such as API key or API endpoint, to be used in future executions.')
@click.argument('pair')
def set_command(pair: str):
    pair = pair.strip()
    cloudrail_cli_config = CliConfiguration()
    config_key, config_value = _extract_config_pair(pair)
    safe_invoke(cloudrail_cli_config.set, config_key, config_value)


@click.command(help='Remove a persisted setting.')
@click.argument('config_key')
def unset(config_key: str):
    config_key = config_key.strip()
    cloudrail_cli_config = CliConfiguration()
    safe_invoke(cloudrail_cli_config.unset, config_key)


@click.command(help='Clear all persisted settings.')
def clear():
    cloudrail_cli_config = CliConfiguration()
    safe_invoke(cloudrail_cli_config.clear_all)
    click.echo('All persisted settings cleared successfully.')


@click.command(help='List the currently persisted settings.')
def info():
    cloudrail_cli_config = CliConfiguration()
    result = safe_invoke(cloudrail_cli_config.get_all)
    # TODO: is there a better option to loop?
    if result:
        for item, doc in result.items():
            click.echo('{0}: {1}'.format(item, doc))
    else:
        click.echo('No configuration contents saved at /indeni/.cloudrail/config')


config.add_command(clear)
config.add_command(info)
config.add_command(set_command)
config.add_command(unset)


def check_indeni_mount():
    cloudrail_volume = os.environ.get('CLOUDRAIL_VOLUME', None)
    if cloudrail_volume and not os.path.ismount(cloudrail_volume):
        echo_error('In order to persist the API key, '
                   'this container must have a /indeni mount point tied to a persistent docker volume.'
                   '\nPlease add \'-v cloudrail:/indeni\' to the command used to run this container.')
        exit_with_code(ExitCode.INVALID_INPUT)


def _extract_config_pair(pair: str) -> tuple:
    pair_as_list = pair.split('=')
    key = None
    value = None
    if len(pair_as_list) == 2:
        key = pair_as_list[0]
        value = pair_as_list[1]
    elif len(pair_as_list) == 1:
        key = pair_as_list[0]
        value = click.prompt(f'Please enter a value for {pair_as_list[0]}')
    else:
        echo_error('This command receives one argument, in the format of \'<name>=<value>\'.')
        exit_with_code(ExitCode.INVALID_INPUT)
    return key, value
