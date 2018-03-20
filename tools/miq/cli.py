""" cli module which handles all of the miq commandline parsing """
import os
import sys
import pdb
import argparse
import pkg_resources
import traceback

import engine

SKIP_OPTIONS = ['provision', 'deprovision', 'bind', 'unbind', 'roles']

AVAILABLE_COMMANDS = {
    'help': 'Display this help message',
    'add': 'Add new MIQ specific apb information',
    'version': 'Get current version of MIQ APB tool'
}

def subcmd_add_parser(subcmd):
    """ add subcommand """
    subcmd.add_argument(
        '--server',
        action='store',
        dest='server',
        help=u'Ip or Hostname to connect to',
    )

    subcmd.add_argument(
        '--service',
        action='store',
        dest='service',
        help=u'HREF slug endpoint to connect to',
    )

    subcmd.add_argument(
        '--username',
        action='store',
        dest='username',
        help=u'The username to connect to MIQ with',
        default='admin'
    )

    subcmd.add_argument(
        '--password',
        action='store',
        dest='password',
        help=u'The password to connect to MIQ with',
        default='smartvm'
    )

    subcmd.add_argument(
        '--validate-certs',
        action='store',
        dest='validate-certs',
        help=u'Validate the certificate used with SSL for the MIQ API connection',
        default=False
    )
    return


def subcmd_version_parser(subcmd):
    """ version subcommand """
    return


def subcmd_help_parser(subcmd):
    """ help subcommand """
    return


def main():
    """ main """
    #pdb.set_trace()
    parser = argparse.ArgumentParser(
        description=u'MIQ tooling for '
        u'assisting in building and packaging MIQ APBs.'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        dest='debug',
        help=u'Enable debug output',
        default=False
    )

    subparsers = parser.add_subparsers(title='subcommand', dest='subcommand')
    subparsers.required = True

    for subcommand in AVAILABLE_COMMANDS:
        subparser = subparsers.add_parser(
            subcommand, help=AVAILABLE_COMMANDS[subcommand]
        )
        globals()['subcmd_%s_parser' % subcommand](subparser)

    args = parser.parse_args()

    if args.subcommand == 'help':
        parser.print_help()
        sys.exit(0)

    if args.subcommand == 'version':
        #version = pkg_resources.require("apb")[0].version
        version = 0.001
        print("Version: cf-cli-apb-%s" % version)
        sys.exit(0)

    try:
        getattr(engine,
                u'cmdrun_{}'.format(args.subcommand))(**vars(args))
    except Exception as error:
        print "Exception occurred! %s" % error
        if args.debug:
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
