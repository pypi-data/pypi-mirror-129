'''
[Mobiles:person.features.specproc]
3039: healer.Healer

[Rooms]
0: Dump

'''

from stuphos.runtime import LookupClassObject
from stuphos.runtime.facilities import Facility
# from mud.tools.logs import logException
from stuphos.etc import splitOne
from stuphos import logException

from stuphos.system.api import syslog, world
BuiltinSpecialProcedure = world.special

#from traceback import print_exc as traceback
from configparser import ConfigParser

# Special Procedures Management.
class SpecprocBitvector(int):
    pass

Room   = SpecprocBitvector(1 << 0)
Mobile = SpecprocBitvector(1 << 1)
Item   = SpecprocBitvector(1 << 2)

Any    = SpecprocBitvector(Room | Mobile | Item)

class Table:
    def __init__(self, parent = None, name = None):
        self.parent = parent
        self.name = name

        # What about by name?
        self.rooms = {}
        self.mobiles = {}
        self.items = {}

        self.subtables = {}
        if parent:
            parent.registerSubtable(self, name)

        # Do this dynamically (shy from direct access without mud api)
        from world import room, mobile, item
        self.RealRoom = room
        self.RealMobile = mobile
        self.RealItem = item

    def assign(self, object, room = None,
               mobile = None, item = None):

        self.assignRoom(room, object)
        self.assignMobile(mobile, object)
        self.assignItem(item, object)

    def register(self, object, room = None,
                 mobile = None, item = None):

        self.registerRoom(room, object)
        self.registerMobile(mobile, object)
        self.registerItem(item, object)

    def registerSubtable(self, table, name):
        if name:
            self.subtables[name] = table

    # Registration: Put procedure into the table, associated with
    # name or Vnum information.
    def registerRoom(self, room, object):
        if type(room) is int:
            self.rooms[room] = object
            return self.RealRoom(room)

        if type(room) is world.room:
            # recognize re-register
            self.rooms[room.vnum] = object
            return room

    def registerMobile(self, mobile, object):
        if type(mobile) is int:
            self.mobiles[mobile] = object
            return self.RealMobile(mobile)

        if type(mobile) is world.mobile:
            # recognize re-register
            self.mobiles[mobile.vnum] = object
            return mobile

    def registerItem(self, item, object):
        if type(item) is int:
            self.items[item] = object
            return self.RealItem(item)

        if type(item) is world.item:
            # recognize re-register
            self.items[item.vnum] = object
            return item

    # Assignment: The interface-with-core operation of
    # procedure installation.
    def assignRoom(self, room, object, **values):
        try: room = self.registerRoom(room, object)
        except ValueError:
            syslog('SYSERR: Assigning %r to unknown room: %s' % (object, room))
        else:
            if room is not None:
                # todo: recognize overwrite
                DoBindSpecial(room, object, **values)

    def assignMobile(self, mobile, object, **values):
        try: mobile = self.registerMobile(mobile, object)
        except ValueError:
            syslog('SYSERR: Assigning %r to unknown mobile: %s' % (object, mobile))
        else:
            if mobile is not None:
                # todo: recognize overwrite
                DoBindSpecial(mobile, object, **values)

    def assignItem(self, item, object, **values):
        try: item = self.registerItem(item, object)
        except ValueError:
            syslog('SYSERR: Assigning %r to unknown item: %s' % (object, item))
        else:
            if item is not None:
                # todo: recognize overwrite
                DoBindSpecial(item, object, **values)

def DoBindSpecial(entity, object, **values):
    special = getBoundSpecial(entity, object, **values)
    if special is not None:
        entity.special = special

    return special

def getBoundSpecial(entity, object, **values):
    try: bind = object.BindSpecial
    except AttributeError: return object

    if not callable(bind):
        # I guess we'll just ignore this attribute.
        return object

    # Do dynamic binding of specproc to entity.
    result = bind(entity, **values)
    if result is not False:
        if callable(result):
            return result

        return object

# Builtin Table.
class SpecialManager(Facility, Table):
    NAME = 'SpecialProcedure::Manager'

    @classmethod
    def create(self):
        table = self(name = '')
        for name in ('assign', 'register', 'assignItem',
                     'assignMobile', 'assignRoom'):

            # Basically provide a recapitalized form of the attribute.
            setattr(self, name[0].upper() + name[1:],
                    staticmethod(getattr(table, name)))

        return table

# Install.
# SpecialManage.manage()
getBuiltinTable = SpecialManager.get
getBuiltinTable(create = True)

# Configuration Layer.
def parseSpecialsConfigSection(section):
    parts = section.split(':', 1)
    if len(parts) == 2:
        return parts
    if len(parts) == 1:
        return (parts[0], None)
    return (None, None)

def LookupSpecialObject(name, namespace = None, spec_type = None):
    if namespace:
        name = '%s.%s' % (namespace, name)
    elif spec_type and '.' not in name:
        try: return BuiltinSpecialProcedure(name, spec_type)
        except NameError:
            return None

    try: return LookupClassObject(name, raise_import_errors = True)
    except (ImportError, AttributeError):
        logException(traceback = True)

    # This raised from LookupObject, which doesn't differentiate
    # types.  So, provide our own type by recognizing this error.
    ##    except AssertionError:
    ##        raise UnknownSpecialObject(name, namespace, spec_type)


def parseSpecialsConfigType(config, special_type):
    results = []
    type = special_type.lower()
    for section in config.sections():
        (type, namespace) = parseSpecialsConfigSection(section)
        if type.lower() == special_type:
            for opt in config.options(section):
                try: vnum = int(opt)
                except ValueError:
                    continue

                values = config.get(section, opt)
                values = values.split('\n')
                name = values[0]

                if len(values) == 1:
                    values = dict()
                else:
                    # Configure binding parameters.
                    from yaml import load
                    values = load('\n'.join(values[1:]))

                results.append((vnum, namespace, name, values))

    return results

def parseSpecialsConfig(config):
    return dict(rooms = parseSpecialsConfigType(config, 'rooms'),
                mobiles = parseSpecialsConfigType(config, 'mobiles'),
                items = parseSpecialsConfigType(config, 'items'))

def parseSpecialsConfigFromFile(config_file):
    config = ConfigParser()
    config.read([config_file])
    return parseSpecialsConfig(config)

def parseSpecialsConfigFromString(string):
    from io import StringIO
    config = ConfigParser()
    config.readfp(StringIO(string)) # , '<init-buf>')
    return parseSpecialsConfig(config)

# Real World Loading.
def loadSpecialsConfig(config):
    # Todo: maybe log more about which specproc this is happening for.
    for (kind, assign) in [('rooms', SpecialManager.AssignRoom),
                           ('mobiles', SpecialManager.AssignMobile),
                           ('items', SpecialManager.AssignItem)]:

        for (entity, ns, name, values) in config[kind]:
            try: object = LookupSpecialObject(name, ns, kind)
            except NameError as e: syslog('SYSERR: %s (%s)' % (e, e.__class__.__name__))
            except Exception: logException(traceback = True)
            else:
                if object is None:
                    syslog('SYSERR: Unknown %s procedure [%s::%s]' % (kind, ns, name))
                else:
                    try: assign(entity, object, **values)
                    except: logException(traceback = True)

def loadSpecialsConfigFromFile(config_file):
    loadSpecialsConfig(parseSpecialsConfigFromFile(config_file))
def loadSpecialsConfigFromString(string):
    loadSpecialsConfig(parseSpecialsConfigFromString(string))

# todo: loadSpecialsConfigFromDatabase, for in-game-managed assignment file.
# see: mud.player.commands.gc.wizard [ControlPoints::assign]

# Object Model.
def isCommandReserved(cmd):
    return cmd is None or cmd.name == 'RESERVED'
def parseSpecialCommand(argstr):
    if argstr is None:
        return ('', '')

    return splitOne(argstr, ' ')


# import standard
