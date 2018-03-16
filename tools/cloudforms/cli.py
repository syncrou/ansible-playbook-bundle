""" cli module which handles all of the cloudforms commandline parsing """
import os
import sys
import pdb
import argparse
import pkg_resources

#import cloudforms.engine

SKIP_OPTIONS = ['provision', 'deprovision', 'bind', 'unbind', 'roles']

AVAILABLE_COMMANDS = {
    'help': 'Display this help message',
    'cf': 'Modify the environment for a CloudForms service',
    'version': 'Get current version of CF APB tool'
}

def subcmd_version_parser(subcmd):
    """ version subcommand """
    return


def subcmd_help_parser(subcmd):
    """ help subcommand """
    return


def subcmd_cf_parser(subcmd):
    """ cf subcommand """
    return


def main():
    """ main """
    #pdb.set_trace()
    parser = argparse.ArgumentParser(
        description=u'CF tooling for '
        u'assisting in building and packaging CloudForms APBs.'
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

    #try:
    #    getattr(cloudforms.engine,
    #            u'cmdrun_{}'.format(args.subcommand))(**vars(args))
    #except Exception as e:
    #    print("Exception occurred! %s" % e)
    #    sys.exit(1)

if __name__ == "__main__":
    main()
