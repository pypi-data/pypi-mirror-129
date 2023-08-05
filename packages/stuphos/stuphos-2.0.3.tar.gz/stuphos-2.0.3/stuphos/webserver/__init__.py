# StuphMUD Compartmentalized Django WSGI Development/Production Server
#   for Django-1.2.1

# This contains a django framework and a bit of an application framework
# for using as a component to building applications.  But, the applications
# are specific to embedding contexts (usually), or, just other purposes
# that are fulfilled by the role of this software package.  However, these
# things are more network specific (external interfaces like the web).

# It is necessary to first import this module to setup the django settings
# module before using the server in this package.  Fortunately, this happens
# automatically.


from django.core.servers.basehttp import run, WSGIRequestHandler, WSGIServer, ServerHandler
#from django.core.servers.basehttp import WSGIServerException
#from django.core.servers.basehttp import AdminMediaHandler
#from django.core.management.validation import get_validation_errors
from django.core.handlers.wsgi import WSGIHandler
from django.conf import settings
from django.utils import translation

from stuphos.runtime.facilities import Facility
from stuphos.runtime.registry import getObject
from stuphos.runtime import newComponent

from io import StringIO
from _thread import start_new_thread as nth
from select import error as select_error
from errno import EINTR
from contextlib import contextmanager

import os
import sys
import imp


# Make Django project and webapps visible.
#

_settings_module = '%s.project.settings' % __name__
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ['DJANGO_SETTINGS_MODULE'] = _settings_module

def importDjango(*submodules):
    import django
    return django


# Server Model Validation.
class ValidationError(Exception):
    pass

def ValidactivateOnce(app = None):
    if not getattr(sys, '__django_validactivated', False):
        ##    s = StringIO()
        ##    num_errors = get_validation_errors(s, app)
        ##    if num_errors:
        ##        raise ValidationError("One or more models did not validate:\n%s" % s.getvalue())

        #translation.activate(settings.LANGUAGE_CODE)
        sys.__django_validactivated = True

def getWSGIServerExceptionMessage(e):
    # Use helpful error messages instead of ugly tracebacks.
    ERRORS = {
        13: "You don't have permission to access that port.",
        98: "That port is already in use.",
        99: "That IP address can't be assigned-to.",
    }
    try: return ERRORS[e.args[0].args[0]]
    except (AttributeError, KeyError):
        return str(e)

try: from fcntl import fcntl, F_SETFD, F_GETFD, FD_CLOEXEC
except ImportError: CloseOnExec = False
else:
    def CloseOnExec(fd):
        # My Impl:
        ##    'This is broken because ~1 returns -2!  Fortunately, sockets seem to be !FD_CLOEXEC initially.'
        ##    oldbits=fcntl(fd, F_GETFD)
        ##    newbits=oldbits & ~FD_CLOEXEC
        ##
        ##    #print oldbits, '&', '~%d' % FD_CLOEXEC, '(%d)' % ~FD_CLOEXEC, '=', newbits
        ##
        ##    ##fcntl(fd, F_SETFD, newbits)
        ##    return fd

        # Basically, from solution addressing [Bug #1222790]:
        flags = fcntl(fd, F_GETFD)
        flags |= FD_CLOEXEC
        fcntl(fd, F_SETFD, flags)

# Service.
from socketserver import ThreadingMixIn as ServerCompartment
class ServerControl(ServerCompartment):
    def set_running(self, value = True):
        self.__running = value
    def is_running(self):
        try: return (self.__running)
        except AttributeError:
            return False

    ##    def process_request_thread(self, *args, **kwd):
    ##        import pdb; pdb.set_trace()
    ##        return ThreadingMixin.process_request_thread(self, *args, **kwd)

    def server_start(self):
        def serve_loop():
            # import pdb; pdb.set_trace()

            while self.is_running():
                #import pdb; pdb.set_trace()

                # print('handling django request...')
                # debugOn()

                try: self.handle_request()
                except select_error as e:
                    if e.args[0] is EINTR:
                        # A process signal was sent, ignore and continue.
                        continue

                    (etype, value, tb) = sys.exc_info()
                    raise etype(value).with_traceback(tb)
                # I don't know where WSGIServerException is defined in django lib.
                # except WSGIServerException, e:
                #     self.log(getWSGIServerExceptionMessage(e))
                except KeyboardInterrupt:
                    self.server_stop()

        self.set_running(True)
        nth(serve_loop, ())

    def server_stop(self):
        self.set_running(False)
    def server_shutdown(self):
        # XXX!
        self.server_stop()
        self.server_close()

    def runningState(self):
        return self.is_running() and 'RUNNING' or 'STOPPED'

    def handle_error(self, request, client_address):
        from stuphos.system.api import syslog
        from stuphos import logException, getConfig

        from sys import exc_info
        from socket import error
        from errno import EPIPE
        (etype, value, tb) = exc_info()

        def log():
            syslog('[HTTP %s] %s: %s [%s]' % ('%s:%s' % client_address, etype.__name__, value, request))

            if isinstance(value, error):
                if value.errno == EPIPE:
                    return

            logException(traceback = True, header = False)

        method = getConfig('process-error') # XXX currently disabled because invocation not called right, 'core/system/httpError')
        if method:
            from stuphos.kernel import invokeLibraryMethod as i
            task = i(method, etype, value, tb,
                     request, client_address)

            @nth
            def async():
                # Why does this need to be off-thread again??
                # I ask because handle_error should already be parallel to VM thread.

                # XXX This is also wrong because the task variable is actually bound
                #   to a result object from a task that has run.

                task = task()

                @task.onComplete
                def completion(task, exception = None):
                    log()

        else:
            log()


class Instrument:
    # These models are not currently available as named:
    ##    from .tracking import onSendMail
    ##    from .tracking import onMovement
    ##    from .tracking import onDealDamage
    ##    from .tracking import onSlayMobile
    ##    from .tracking import onDeathTrap
    ##    from .tracking import onPasswordChange
    ##    from .tracking import onPlayerSavePoint
    pass

class EmbeddedRequestHandler(WSGIRequestHandler):
    # Provide configurable ServerHandler.server_software
    # (Probably a better way to do this is to set Server header)

    class ServerHandler(ServerHandler):
        def __init__(self, stdin, stdout, stderr, environ, software, **kwd):
                     # multithread = True, multiprocess = False):
            ServerHandler.__init__(self, stdin, stdout, stderr, environ, software, **kwd)
            self.server_software = software

    def handle(self):
        """Copy of WSGIRequestHandler, but with different ServerHandler"""

        # [HTTP 192.168.43.1:52786] ConnectionResetError: [Errno 104] Connection reset by peer [<ssl.SSLSocket fd=15, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('192.168.43.192', 2180)>]
        #   [socketserver.py:654] process_request_thread
        #     self.finish_request(request, client_address)
        #   [socketserver.py:364] finish_request
        #     self.RequestHandlerClass(request, client_address, self)
        #   [socketserver.py:724] __init__
        #     self.handle()
        #   [stuphos/webserver/__init__.py:211] handle
        #     self.raw_requestline = self.rfile.readline(65537)
        #   [socket.py:586] readinto
        #     return self._sock.recv_into(b)
        #   [ssl.py:971] recv_into
        #     return self.read(nbytes, buffer)
        #   [ssl.py:833] read
        #     return self._sslobj.read(len, buffer)
        #   [ssl.py:590] read
        #     v = self._sslobj.read(len, buffer)

        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return

        if not self.parse_request():  # An error code has been sent, just exit
            return

        handler = self.ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ(),
            self.server.software
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())

class LoggingWSGIRequestHandler(EmbeddedRequestHandler):
    'Disables logging of WSGI messages.'

    def log_message(self, format, *args):
        from stuphos import getConfig
        from stuphos.etc import isYesValue

        # import pdb; pdb.set_trace()
        if isYesValue(getConfig('log-request', 'DjangoService')):
            message = '%s - - [%s] %s' % \
                         (self.client_address[0],
                          self.log_date_time_string(),
                          format)

            EmbeddedRequestHandler.log_message(self, message, *args)

from django.utils.deprecation import MiddlewareMixin

class Key:
    public = ''
    private = ''

    def __init__(self, request = None):
        if request:
            try:
                # (Never encrypt)
                self.private = request.session.get('retention_token_secret', self.private)
                self.public = request.session.get('retention_token_public', self.public)
 
            except KeyError:
                pass

            else:
                return

        # pair = providerGenerate()
        # self.private = pair.private
        # self.public = pair.public

    def __call__(self, data):
        return data # encrypt(data, self.public)


class LoggingMiddleware(MiddlewareMixin):
    @runtime.available(runtime.System.Journal)
    # Note the argument positioning.
    def process_view(log, self, request, callback, callback_args, callback_kwargs):
        from stuphos.etc.tools.timing import date as now
        import json

        # todo: debug this api:
        # @runtime.System.Engine # (accessorOf.contextObject.task)
        # def task(vm):
        #     return vm.contextObject.task

        task = None

        source = task.taskName if task is not None else 'web-request'
        meta = request.META.get

        content = json.dumps(dict(remoteAddress = meta('REMOTE_ADDR'),
                                  userAgent = meta('HTTP_USER_AGENT'),
                                  method = meta('REQUEST_METHOD'),
                                  path = meta('PATH_INFO'),
                                  queryString = meta('QUERY_STRING')),
                             indent = 1)

        key = Key() # (request)
        content = json.dumps(dict(content = key(content), user = request.user.id))

        request.session['retention_token_secret'] = key.private
        request.session['retention_token_public'] = key.public

        # :system-journal:
        log += dict(source = source, type = 'web-request/json',
                    content = content, timestamp = now())


@runtime.available(runtime.System.Journal)
def retentionView(log, request, key = False, delete = False):
    # io.user.data.jsonOf.write(host['/data/retention'].value)
    # host['/data/retention?delete=true'].value 
    # io.user.secret.keyOf.write(host['/data/retention?key=true'].value)
    # host['/data/retention?key=true&delete=true'].value

    key = request.GET.get('key', key)

    def records(self):
        for e in log.select():
            # todo: configure task context in middleware
            if e['source'] != 'web-request':
                continue

            o = json.loads(e.content)

            if o['user'] == request.user.id:
                yield (e, o['content'])

                if delete:
                    e.delete()

    # todo: assert SSL, overlock
    if key:
        if key not in ['yes', 'true', '1', 'on', 'no', 'false', '0', 'off']:
            # Set key.
            assert not any(records())

            del request.session['retention_token_public']
            request.session['retention_token_secret'] = key

            key = False

        else:
            key = isYesValue(key)

            if key:
                o = request.session['retention_token_secret']
                response = http.DjangoResponse(o, content_type = 'text/plain') # application/octet

    delete = isYesValue(request.GET.get('delete', delete) or 'no')

    if key:
        # Transactionally return key on confirmation of exported records.

        if delete:
            del request.session['retention_token_secret']
            del request.session['retention_token_public']

        return response

    return http.DjangoResponse(json.dumps(list(records()), indent = 1),
                               content_type = 'application/json')


class DjangoService(Facility, ServerControl, WSGIServer, Instrument):
    NAME = 'Django::Service'

    # Configuration.
    HOSTNAME = '0.0.0.0' # 'localhost'
    PORT = 8000
    ADMIN_MEDIA_PATH = ''
    DEBUG = False # Production

    @classmethod
    def GetConfig(self):
        try:
            from stuphos import getConfig
            from stuphos.etc import isYesValue

        except ImportError:
            hostname = self.HOSTNAME
            port = self.PORT
            admin_media_path = self.ADMIN_MEDIA_PATH
            debug = self.DEBUG

            certfile = None
            software = ServerHandler.server_software

            urlConf = 'phsite.network.urls' # XXX default this better

        else:
            hostname = getConfig('hostname', 'DjangoService') or self.HOSTNAME
            port = int(getConfig('port', 'DjangoService') or self.PORT)
            admin_media_path = getConfig('admin-media-path', 'DjangoService') or self.ADMIN_MEDIA_PATH
            debug = self.DEBUG # isYesValue(getConfig('show-debug-page', 'DjangoService') or (self.DEBUG and 'yes' or 'no'))

            certfile = getConfig('certificate-path', 'DjangoService')
            software = getConfig('software', 'DjangoService')

            urlConf = getConfig('sitemap', 'DjangoService')

        return (hostname, port, admin_media_path, debug, certfile, software, urlConf)

    class Manager(Facility.Manager):
        VERB_NAME = 'dj*ango-service'
        MINIMUM_LEVEL = Facility.Manager.IMPLEMENTOR

        def do_reload(self, peer, parentCommand, args):
            with ReloadEmbeddedUrlConf():
                for moduleName in args:
                    try: module = importModule(moduleName)
                    except ImportError as e: print('%s: %s' % (moduleName, str(e)), file=peer)
                    else: print('Reloaded: %s' % getattr(imp.reload(module), '__name__', moduleName), file=peer)

            print('Reloaded Django URLConf.', file=peer)

        def do_toggle_debug(self, peer, command, args):
            from django.conf import settings
            settings.DEBUG = not settings.DEBUG

    # Uncomment this to debug individual incoming requests:
    # finish_request = breakOn(WSGIServer.finish_request)

    def server_bind(self, *args, **kwd):
        # Ideally, this would go on ServerControl, if WSGIServer/BaseHTTPServer actually implemented it.
        result = WSGIServer.server_bind(self, *args, **kwd)
        if CloseOnExec:
            CloseOnExec(self.fileno())

        return result

    @classmethod
    def create(self):
        from phsite.network.embedded import install, uninstall
        install()

        import logging, logging.handlers
        logger = logging.getLogger('django.server')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.INFO)

        try:
            ValidactivateOnce()
            (hostname, port, admin_media_path, debug, certfile, software, urlConf) = \
                self.GetConfig()

            from django.conf import settings
            # Doesn't affect the construction of the middleware.
            # Q: What about getting the config before activation, and setting then?
            # settings.DEBUG = debug

            # Moved out of constructor because handler relies on it being configured sooner.
            from django.apps import apps
            apps.populate(settings.INSTALLED_APPS)

            #wsgi_handler = AdminMediaHandler(WSGIHandler(), admin_media_path)
            wsgi_handler = WSGIHandler()

            server = newComponent(self) # todo: ditch instrument, use Module component.
            self.__init__(server, (hostname, port), wsgi_handler,
                          urlConf, certfile, software)
        except:
            uninstall()
            raise

        return server

    def __init__(self, server_address, wsgi_handler, urlConf, certfile, software):
        WSGIServer.__init__(self, server_address, LoggingWSGIRequestHandler)
        self.software = software

        if certfile is not None:
            import ssl
            self.socket = ssl.wrap_socket (self.socket, certfile = certfile, server_side = True)

        self.set_app(wsgi_handler)

        # Start Immediately.
        self.server_start()

        # Force load the sitemap. XXX Hack
        ##    from django.core.urlresolvers import get_urlconf, get_resolver
        ##    urlconf = get_urlconf()
        ##    resolver = get_resolver(urlconf)
        ##    resolver._populate()


        # Configuration specific for the development shell.
        # Note:
        # django\core\urlresolvers.py(107) #get_resolver = memoize(get_resolver, _resolver_cache, 1)

        ##    DATABASE_PATH = str(io.here.web.olc.dbOf)
        ##    DATABASE = dict(ENGINE = 'django.db.backends.sqlite3',
        ##                    NAME = DATABASE_PATH,
        ##                    USER = '',
        ##                    PASSWORD = '')

        #settings._wrapped = None # This seems to work, although it's hardcore.
        #settings.configure(DATABASES = dict(default = DATABASE))

        # settings.DATABASES = dict(default = DATABASE)

        # Do this.. the problem is that the settings are already all
        # configured way before, and when the database modules are
        # initialized, because django is imported initially by pywin
        # shell.  So... for the purposes of this testing, we'd need
        # to reload alot of the components that require 'connections'
        # OR, find a way to configure the database manually within
        # pywin.
        #import django
        #reload(django.db)

        # OR, figure out a way to host multiple databases/settings.

        # This was moved to before server/handler construction (create()).
        ##    from django.apps import apps
        ##    from django.conf import settings
        ##    apps.populate(settings.INSTALLED_APPS)

        with ReloadEmbeddedUrlConf(urlConf):
            pass

    def __registry_delete__(self):
        self.server_shutdown()

        from phsite.network.embedded import uninstall
        uninstall()

    def getStatus(self):
        return '{%s: %s}\n%s' % (self.__class__.__name__, self.runningState(),
                                 GetURLConf(indent = '  '))

@contextmanager
def ReloadEmbeddedUrlConf(urlConf = None):
    from django.core.urlresolvers import clear_url_caches
    clear_url_caches()

    # Hack in the settings file, because this service doesn't compartmentalize
    # the project right in embedded mode.
    #template_dir = system.modulePath(system.lookup(__name__))
    #template_dir = template_dir.folder.folder.templates
    #template_dir = str(template_dir)

    from os.path import dirname, join as joinpath
    template_dir = dirname(dirname(__file__))
    template_dir = joinpath(template_dir, 'templates')

    if template_dir not in settings.TEMPLATE_DIRS:
        settings.TEMPLATE_DIRS += (template_dir,)


    # XXX obseleted reference:
    # if 'web.application' not in settings.INSTALLED_APPS:
    #     settings.INSTALLED_APPS += ('web.application',)


    # Note: this has become necessary because the settings is abstracted
    # into the application configuration.
    if urlConf is not None:
        settings.ROOT_URLCONF = urlConf


    try: yield
    finally:
        # from web.stuph.embedded import urls
        #from web.stuph import urls
        #reload(urls)

        # todo: put them back into global_settings.ROOT_URLCONF,
        # wrap them in a hashable entity so that the object caching
        # internals work properly (urls.urlpatterns is a list).
        #from django.core import urlresolvers
        # First, dereference the previous '^/'-wrapped resolver object from the memory
        #settings.ROOT_URLCONF = urlresolvers.RegexURLResolver('', urls.urlpatterns)
        #settings.ROOT_URLCONF = tuple(urls.urlpatterns) # tuple(...)?

        pass


def GetURLConf(indent = ''):
    from django.core.urlresolvers import get_resolver, get_urlconf, RegexURLResolver, RegexURLPattern
    def formatResolver(r, indent):
        result = ['[module:%s (%s:%s)] %s' % (r.urlconf_name, r.app_name,
                                     r.namespace, r.regex.pattern)]

        indent2 = indent + '  '
        for url in r.url_patterns:
            if isinstance(url, RegexURLResolver):
                result.append(formatResolver(url, indent2))
            elif isinstance(url, RegexURLPattern):
                if url.name:
                    result.append('%s: %s' % (url.name, url.regex.pattern))
                else:
                    result.append(url.regex.pattern)

        tab = '\n' + indent
        return tab.join(result)

    return formatResolver(get_resolver(get_urlconf()), indent)

def importModule(name):
    return __import__(name, locals(), globals(), [''])

# Install Front End.
DjangoService.manage()
