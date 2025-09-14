import copy
import functools
import six
from prototypeclient import exc
from oslo_utils import encodeutils
from oslo_utils import strutils
from prototypeclient.i18n import _

from prototypeclient.common import utils

_bool_strict = functools.partial(strutils.bool_from_string, strict=True)


def do_service_list(client, args):
    """List all services."""
    services = client.services.list()
    fields = ['id', 'host', 'type', 'topic', 'disabled']
    utils.print_list(services, fields)


@utils.arg('service',
           metavar='<service>',
           help='ID of service to show')
def do_service_show(client, args):
    """Show details of a service."""
    service = client.services.get(args.service)
    utils.print_dict(service._info)


@utils.arg('--host',
           metavar='<host>',
           required=True,
           help='Service host')
@utils.arg('--type',
           metavar='<type>',
           required=True,
           help='Service type')
@utils.arg('--topic',
           metavar='<topic>',
           required=True,
           help='Service topic')
def do_service_create(client, args):
    """Create a service."""
    service = client.services.create(args.host, args.type, args.topic)
    utils.print_dict(service._info)


@utils.arg('service',
           metavar='<service>',
           help='ID of service to delete')
def do_service_delete(client, args):
    """Delete a service."""
    client.services.delete(args.service)
    print("Request to delete service %s has been accepted." % args.service)


@utils.arg('service',
           metavar='<service>',
           help='ID of service to update')
@utils.arg('--disabled',
           metavar='<disabled>',
           help='Disable service (true/false)')
@utils.arg('--disabled-reason',
           metavar='<disabled-reason>',
           help='Reason for disabling service')
def do_service_update(client, args):
    """Update a service."""
    kwargs = {}

    if args.disabled:
        try:
            kwargs['disabled'] = strutils.bool_from_string(args.disabled, strict=True)
        except ValueError:
            raise exc.CommandError("Disabled must be 'true' or 'false'")

    if args.disabled_reason is not None:
        kwargs['disabled_reason'] = args.disabled_reason

    service = client.services.update(args.service, **kwargs)
    print("Service %s has been updated." % args.service)
    utils.print_dict(service._info)
