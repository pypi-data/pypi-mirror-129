# Managed File System.
from .. import playerAlert, PlayerAlert

from errno import EEXIST

from os.path import exists, normpath, isdir
from os.path import sep as PATH_SEP, sep as root
from os.path import join as joinpath, split as splitpath
from os import makedirs
# from string import lowercase
from string import ascii_lowercase as lowercase

from stuphos import getConfig
from stuphos.runtime import Component
from stuphos.runtime.registry import setObject as registerObject
from stuphmud.server.player import HandleCommandError

PLAYER_FILE_DIR = getConfig('player-file-dir') or 'plrfiles'
PERSONAL_PLRFILE_DIR = getConfig('personal-file-dir') or 'personal'
PROGRAMS_DIR = getConfig('player-program-dir') or 'programmes'
DATABASE_DIR = getConfig('player-database-dir') or 'db'
LIBRARY_DIR = getConfig('player-library-dir') or 'library'
SECURE_DIR = getConfig('player-secure-dir') or 'secure'
KEYFILE_DIR = joinpath(SECURE_DIR, getConfig('player-keyfile-subdir') or 'keyfiles')

def splitallpath(path):
    # Just split via the PATH_SEP into individual elements, but never
    # empty ones (that is, // is treated as /).
    result = []
    while any(c != PATH_SEP for c in path): # Only works when PATH_SEP is one char.
        (head, tail) = splitpath(path)
        result.insert(0, tail)
        path = head

    return result

def getSecureFilename(filename):
    # XXX Is this platform-compatible?
    # Pretend the filename is in root, then normalize away the
    # relative parts against this path, then strip off the root.
    parts = splitallpath(normpath(joinpath(root, filename)))
    if parts:
        return joinpath(*parts)

    return ''

def getPlayername(player):
    plrname = player.name.lower()
    plrname = ''.join(c for c in plrname if c in lowercase)
    return plrname

def validatePlayername(plrname):
    plrname = plrname.lower()
    plrname = ''.join(c for c in plrname if c in lowercase)
    assert plrname
    return plrname

# What about middle-name stacks?
def getPlayerFilename(plrname, filename, folder):
    plrfile = PLAYER_FILE_DIR
    if not exists(plrfile):
        return

    plrpath = joinpath(plrfile, plrname)
    if folder:
        plrpath = joinpath(plrpath, folder)

    try: makedirs(plrpath)
    except OSError as e:
        if e.errno != EEXIST:
            raise

    if not isdir(plrpath):
        return

    return joinpath(plrpath, filename)

def getCheckedPlayerFilename(peer, filename, folder = None, dirOp = False):
    if not peer.avatar:
        playerAlert('No avatar from which to obtain player name.')

    plrname = getPlayername(peer.avatar)
    if not plrname:
        playerAlert('Could not obtain player name.')

    filename = getSecureFilename(filename)
    if not filename and not dirOp:
        playerAlert('Unable to produce secure filename.')

    plrfile = getPlayerFilename(plrname, filename, folder)
    if not plrfile:
        playerAlert('Could not obtain player filename.')

    return plrfile


# Register API.
from stuphos.runtime.registry import setObject

# API
def apply(function, *args, **kwd):
    return function(*args, **kwd)

@apply
class API:
    NAME = 'Player::DB::ManagedFS::API'
    VALID_FOLDERS = ['PLAYER_FILE_DIR', 'PERSONAL_PLRFILE_DIR',
                     'PROGRAMS_DIR', 'DATABASE_DIR', 'LIBRARY_DIR']

    getSecureFilename = staticmethod(getSecureFilename)
    getPlayername = staticmethod(getPlayername)
    getPlayerFilename = staticmethod(getPlayerFilename)
    getCheckedPlayerFilename = staticmethod(getCheckedPlayerFilename)

    def getFolder(self, kind):
        if kind in self.VALID_FOLDERS:
            return globals()[kind]

registerObject(API.NAME, API)

# todo: Web-Extended Properties?
# todo: This should be a part of mud.player.interpret, but this doesn't
#       always occur as a bridge event.  Copyover calls interpret directly.
#       also, programmes are player parts (not peer).
#
# also, since the mud.player.enterGame handler relies on programs installed via
# this managed fs, this functionality should probably be moved into the core.
#
# also, onNewConnection can't do it because player isn't there yet.
#
from shelve import open as openShelf
# import pdb; pdb.set_trace()
class PlayerFileManager(Component):
    def onPlayerActivation(self, cltr, peer, player):
        installPlayerFileStructure(peer, player)
        installPlayerPrograms(peer, player)
        if installPlayerProperties:
            # todo: disable
            installPlayerProperties(peer, player)

class PlayerFileStructure(object):
    def __init__(self, player, pathObjectClass):
        self.player = player
        self.pathObjectClass = pathObjectClass

    def getPlayername(self):
        return getPlayername(self.player)
    def __getitem__(self, name):
        return self.pathObjectClass(getPlayerFilename(self.getPlayername(), name, None))
    def __getattr__(self, name):
        try: return self[API.getFolder(self.FolderNames[name])]
        except KeyError:
            return object.__getattribute__(self, name)

    FolderNames = dict(personal = 'PERSONAL_PLRFILE_DIR',
                       programs = 'PROGRAMS_DIR',
                       database = 'DATABASE_DIR',
                       library = 'LIBRARY_DIR')

def installPlayerFileStructure(peer, player):
    try: from path import path as pathObjectClass
    except ImportError:
        try: from common.platform.path import path as pathObjectClass
        except ImportError: return

    player.plrfiles = PlayerFileStructure(player, pathObjectClass)

def installPlayerPrograms(peer, player):
    if 0:
        # File Model.
        try:
            filename = getCheckedPlayerFilename(peer, 'python.db',
                                                folder = PROGRAMS_DIR)
        except PlayerAlert as e:
            e.deliver(peer)
        except:
            HandleCommandError(peer)
        else:
            # Plop her in.
            player.programs = openShelf(filename)

    else:
        from stuphmud.server.player.notebook import Notebook
        player.programs = Notebook.Model.OpenForPlayer(player.name).shelf

# SQLObject Extended Properties.
try:
    from sqlobject import connectionForURI, SQLObject, StringCol, PickleCol
    from sqlobject import classregistry
except ImportError:
    from warnings import warn
    warn('SQLObject not installed -- Extended Properties not available!')
    installPlayerProperties = False
else:
    from os.path import abspath

    class SqlProperties(object):
        # Don't really need separate registry, because this isn't going to change much.
        try: StoredValue = classregistry.findClass('StoredValue')
        except KeyError:
            class StoredValue(SQLObject):
                name = StringCol()
                value = PickleCol() # pickleProtocol = 0) # nonstrict?

                # todo: Stored properties for all players in a single connection.
                # player = IntegerCol() # idnum

                _connection = None

        # Table Construction.
        def __init__(self, filename): # , player_idnum
            # Hmm, new db file connection for each player?
            conn = connectionForURI('sqlite:' + abspath(filename))
            self.__dict__['_%s__connection' % self.__class__.__name__] = conn

            if not SqlProperties.StoredValue.tableExists(connection = conn):
                SqlProperties.StoredValue.createTable(connection = conn)

        # Methods.
        def loadProperty(self, name):
            try: return object.__getattribute__(self, name)
            except AttributeError:
                pass

            for sv in SqlProperties.StoredValue.selectBy(connection = self.__connection,
                                                         name = name):
                return sv.value

            raise AttributeError(name)

        def storeProperty(self, name, value):
            if name.startswith('_'):
                # Do not allow storing anything else on this class.
                raise AttributeError(name)

            conn = self.__connection
            for sv in SqlProperties.StoredValue.selectBy(connection = conn, name = name):
                sv.value = value
                break
            else:
                sv = SqlProperties.StoredValue(connection = conn, name = name, value = value)

            sv._connection = conn
            sv.sync()

        def deleteProperty(self, name):
            if not name.startswith('_'):
                conn = self.__connection
                for sv in SqlProperties.StoredValue.selectBy(connection = conn, name = name):
                    sv._connection = conn
                    sv.destroySelf()
                    return

            raise AttributeError(name)

        def enumerateProperties(self):
            return (sv.name for sv in SqlProperties.StoredValue.select(connection = self.__connection))
        def numberOfProperties(self):
            return len(list(self.enumerateProperties()))
            # return SqlProperties.StoredValue.tableSize(connection = self.__connection))

        __getattr__ = loadProperty
        __setattr__ = storeProperty
        __delattr__ = deleteProperty
        __getitem__ = loadProperty
        __setitem__ = storeProperty
        __delitem__ = deleteProperty
        __iter__    = enumerateProperties
        __len__     = numberOfProperties

    def installPlayerProperties(peer, player):
        # todo: Connect properties view to existing shared database.
        try:
            filename = getCheckedPlayerFilename(peer, 'properties.sqlite',
                                                folder = DATABASE_DIR)
        except PlayerAlert as e:
            e.deliver(peer)
        except:
            HandleCommandError(peer)
        else:
            # Plop her in.
            player.properties = SqlProperties(filename)
