# Error and Informational Logging Routines.
# These are loaded into runtime.core module.
from . import getSystemException, getModuleFileBasename
from traceback import extract_tb

__all__ = ['log', 'logWarning', 'logError', 'logException', 'logWizards']

def log(*args, **kwd):
    global log
    from stuphos.system.api import syslog
    log = syslog # Rewrite.

    # runtime.call.System.Bridge.logSystem(*args, **kwd)
    # logJournal(*args, **kwd)

    return syslog(*args, **kwd)

def logJournal(*args, **kwd):
    log = runtime[runtime.System.Journal]
    if log is not None:
        from stuphos.etc.tools.timing import date as now
        import json

        # @runtime.on.System.Bridge.logSystem
        # :system-journal:
        log += ('system', 'log', json.dumps((args, kwd)), now())

def logWarning(message):
    log('Warning: %s' % message)
def logError(message):
    log('Error: %s' % message)

DEFAULT_LOGINDENT = 27
PADINDENT = ' ' * 2

def tracebackString(tb = None, indent = None):
    if indent is None:
        indent = DEFAULT_LOGINDENT

    def _():
        logindent = indent * ' '
        logindent += PADINDENT
        logindent2 = logindent + PADINDENT

        for (file, lineno, name, source) in extract_tb(tb):
            file = getModuleFileBasename(file)
            yield '%s[%s:%d] %s' % (logindent, file, lineno, name)
            if source:
                yield '%s%s' % (logindent2, source.strip())

    return '\n'.join(_())

def exceptionHeader(etype = None, value = None, tb = None):
    return '%s: %s' % (etype.__name__, value)

def logException(etype = None, value = None, tb = None,
                 traceback = False, header = None,
                 indent = 'auto'):

    # Construct a traceback suitable for logging to syslog file.
    # Todo: serialize the exception data to another file.
    if etype is None and value is None and tb is None:
        (etype, value, tb) = getSystemException()

    if header is None:
        header = exceptionHeader(etype, value, tb)

    if traceback:
        if indent == 'auto':
            from stuphos import getConfig

            indent = getConfig('logindent')
            if indent is not None:
                indent = int(indent)


        tb = tracebackString(tb, indent = indent)

        if header:
            log('%s\n%s' % (header, tb))
        else:
            log(tb)
    else:
        log(header)

DEFAULT_WIZLOG_LEVEL = 115
DEFAULT_WIZLOG_TYPE = 'Complete'

def logWizards(message, level = None, type = DEFAULT_WIZLOG_TYPE, tofile = False):
    if level is None:
        level = DEFAULT_WIZLOG_LEVEL

    elif not isinstance(level, int):
        from world import mobile
        if isinstance(level, mobile):
            level = mobile.level
        else:
            raise TypeError(type(level).__name__)

    from stuphos.system.api import mudlog, syslog
    mudlog(message, level, type)

    if tofile:
        syslog(message)

wizlog = logWizards
