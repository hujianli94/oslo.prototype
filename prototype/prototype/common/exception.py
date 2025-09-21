import functools
import sys

from oslo_log import log as logging
from prototype.conf import CONF
from prototype.common.i18n import _, _LE

LOG = logging.getLogger(__name__)


class PrototypeException(Exception):
    """Base Prototype Exception

    To correctly use this class, inherit from it and define
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """
    msg_fmt = _("An unknown exception occurred.")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                pass

        if not message:
            try:
                message = self.msg_fmt % kwargs

            except Exception:
                exc_info = sys.exc_info()
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                LOG.exception(_LE('Exception in string format operation'))
                for name, value in kwargs.iteritems():
                    LOG.error("%s: %s" % (name, value))  # noqa

                if CONF.fatal_exception_format_errors:
                    raise exc_info[0], exc_info[1], exc_info[2]
                else:
                    # at least get the core message out if something happened
                    message = self.msg_fmt

        super(PrototypeException, self).__init__(message)

    def format_message(self):
        # NOTE(mrodden): use the first argument to the python Exception object
        # which should be our full PrototypeException message, (see __init__)
        return self.args[0]


class ProgrammingError(PrototypeException):
    message = _('Programming error in Prototype: %(reason)s')


class NotAuthorized(PrototypeException):
    message = _("Not authorized.")
    code = 403


class AdminRequired(NotAuthorized):
    message = _("User does not have admin privileges")


class PolicyNotAuthorized(NotAuthorized):
    message = _("Policy doesn't allow %(action)s to be performed.")


class Invalid(PrototypeException):
    message = _("Unacceptable parameters.")
    code = 400


class InvalidResults(Invalid):
    message = _("The results are invalid.")


class InvalidInput(Invalid):
    message = _("Invalid input received: %(reason)s")


class InvalidContentType(Invalid):
    message = _("Invalid content type %(content_type)s.")


class InvalidHost(Invalid):
    message = _("Invalid host: %(reason)s")


class InvalidParameterValue(Invalid):
    message = "%(err)s"


class InvalidConfigurationValue(Invalid):
    message = _('Value "%(value)s" is not valid for '
                'configuration option "%(option)s"')


class ServiceUnavailable(Invalid):
    message = _("Service is unavailable at this time.")


class InvalidAPIVersionString(Invalid):
    message = _("API Version String %(version)s is of invalid format. Must "
                "be of format MajorNum.MinorNum.")


class VersionNotFoundForAPIMethod(Invalid):
    message = _("API version %(version)s is not supported on this method.")


class ValidationError(Invalid):
    message = "%(detail)s"

    safe = True


class Invalid(PrototypeException):
    msg_fmt = _("Bad Request - Invalid Parameters")
    code = 400


class InvalidInput(Invalid):
    msg_fmt = _("Invalid input received: %(reason)s")


class NotFound(PrototypeException):
    message = _("Resource could not be found.")
    code = 404


class MessageNotFound(NotFound):
    message = _("Message %(message_id)s could not be found.")


class ServerNotFound(NotFound):
    message = _("Instance %(uuid)s could not be found.")


class ServiceNotFound(NotFound):

    def __init__(self, message=None, **kwargs):
        if not message:
            if kwargs.get('host', None):
                self.message = _("Service %(service_id)s could not be "
                                 "found on host %(host)s.")
            else:
                self.message = _("Service %(service_id)s could not be found.")
        super(ServiceNotFound, self).__init__(message, **kwargs)


class WorkerNodeNotFound(NotFound):
    message = _("Worker with %s could not be found.")

    def __init__(self, message=None, **kwargs):
        keys_list = ('{0}=%({0})s'.format(key) for key in kwargs)
        placeholder = ', '.join(keys_list)
        self.message = self.message % placeholder
        super(WorkerNodeNotFound, self).__init__(message, **kwargs)


class HostNotFound(NotFound):
    message = _("Host %(host)s could not be found.")


class HostBinaryNotFound(NotFound):
    message = _("Could not find binary %(binary)s on host %(host)s.")


class PrototypeHostNotFound(NotFound):
    message = _("Prototype host %(host)s could not be found.")


class PrototypeServiceNotFound(NotFound):
    message = _("Prototype service %(service)s could not be found.")


class SchedulerHostFilterNotFound(NotFound):
    message = _("Scheduler Host Filter %(filter_name)s could not be found.")


class SchedulerHostWeigherNotFound(NotFound):
    message = _("Scheduler Host Weigher %(weigher_name)s could not be found.")


class FileNotFound(NotFound):
    message = _("File %(file_path)s could not be found.")


class InvalidName(Invalid):
    message = _("An invalid 'name' value was provided. %(reason)s")


class InvalidGlobalAPIVersion(Invalid):
    message = _("Invalid global API version %(version)s.")


class SSHInjectionThreat(PrototypeException):
    message = _("SSH command injection detected: %(command)s")


class PasteAppNotFound(NotFound):
    message = _("Paste app %(app_name)s could not be found.")


class ConfigNotFound(NotFound):
    message = _("Could not find config at %(path)s")


class Duplicate(PrototypeException):
    message = _("Resource already exists.")


class WorkerExists(Duplicate):
    message = _("Worker for %(type)s %(id)s already exists.")


class APIException(PrototypeException):
    message = _("Error while requesting %(service)s API.")

    def __init__(self, message=None, **kwargs):
        if 'service' not in kwargs:
            kwargs['service'] = 'unknown'
        super(APIException, self).__init__(message, **kwargs)


class APITimeout(APIException):
    message = _("Timeout while requesting %(service)s API.")


class MalformedRequestBody(PrototypeException):
    message = _("Malformed message body: %(reason)s")


class RPCTimeout(PrototypeException):
    message = _("Timeout while requesting capabilities from backend "
                "%(service)s.")
    code = 502
