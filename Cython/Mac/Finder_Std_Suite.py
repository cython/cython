"""Suite Standard Suite: Common terms for most applications
Level 1, version 1

Generated from Macintosh HD:System 8.0:Finder
AETE/AEUT resource version 0/144, language 0, script 0
"""

import aetools
import MacOS

_code = 'core'

class Finder_Std_Suite:

    _argmap_class_info = {
        '_in' : 'wrcd',
    }

    def class_info(self, _object=None, _attributes={}, **_arguments):
        """class info: Get information about an object class
        Required argument: the object class about which information is requested
        Keyword argument _in: the human language and script system in which to return information
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: a record containing the object's properties and elements
        """
        _code = 'core'
        _subcode = 'qobj'

        aetools.keysubst(_arguments, self._argmap_class_info)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_close = {
        'saving' : 'savo',
        'saving_in' : 'kfil',
    }

    def close(self, _object, _attributes={}, **_arguments):
        """close: Close an object
        Required argument: the object to close
        Keyword argument saving: specifies whether changes should be saved before closing
        Keyword argument saving_in: the file in which to save the object
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'core'
        _subcode = 'clos'

        aetools.keysubst(_arguments, self._argmap_close)
        _arguments['----'] = _object

        aetools.enumsubst(_arguments, 'savo', _Enum_savo)

        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_count = {
        'each' : 'kocl',
    }

    def count(self, _object, _attributes={}, **_arguments):
        """count: Return the number of elements of a particular class within an object
        Required argument: the object whose elements are to be counted
        Keyword argument each: the class of the elements to be counted
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: the number of elements
        """
        _code = 'core'
        _subcode = 'cnte'

        aetools.keysubst(_arguments, self._argmap_count)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_data_size = {
        'as' : 'rtyp',
    }

    def data_size(self, _object, _attributes={}, **_arguments):
        """data size: Return the size in bytes of an object
        Required argument: the object whose data size is to be returned
        Keyword argument as: the data type for which the size is calculated
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: the size of the object in bytes
        """
        _code = 'core'
        _subcode = 'dsiz'

        aetools.keysubst(_arguments, self._argmap_data_size)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    def delete(self, _object, _attributes={}, **_arguments):
        """delete: Delete an element from an object
        Required argument: the element to delete
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'core'
        _subcode = 'delo'

        if _arguments: raise TypeError, 'No optional args expected'
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_duplicate = {
        'to' : 'insh',
        'replacing' : 'alrp',
        'routing_suppressed' : 'rout',
    }

    def duplicate(self, _object, _attributes={}, **_arguments):
        """duplicate: Duplicate object(s)
        Required argument: the object(s) to duplicate
        Keyword argument to: the new location for the object(s)
        Keyword argument replacing: Specifies whether or not to replace items in the destination that have the same name as items being duplicated
        Keyword argument routing_suppressed: Specifies whether or not to autoroute items (default is false). Only applies when copying to the system folder.
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: to the duplicated object(s)
        """
        _code = 'core'
        _subcode = 'clon'

        aetools.keysubst(_arguments, self._argmap_duplicate)
        _arguments['----'] = _object

        aetools.enumsubst(_arguments, 'alrp', _Enum_bool)
        aetools.enumsubst(_arguments, 'rout', _Enum_bool)

        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_event_info = {
        '_in' : 'wrcd',
    }

    def event_info(self, _object, _attributes={}, **_arguments):
        """event info: Get information about the Apple events in a suite
        Required argument: the event class of the Apple events for which to return information
        Keyword argument _in: the human language and script system in which to return information
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: a record containing the events and their parameters
        """
        _code = 'core'
        _subcode = 'gtei'

        aetools.keysubst(_arguments, self._argmap_event_info)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    def exists(self, _object, _attributes={}, **_arguments):
        """exists: Verify if an object exists
        Required argument: the object in question
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: true if it exists, false if not
        """
        _code = 'core'
        _subcode = 'doex'

        if _arguments: raise TypeError, 'No optional args expected'
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_get = {
        'as' : 'rtyp',
    }

    def get(self, _object, _attributes={}, **_arguments):
        """get: Get the data for an object
        Required argument: the object whose data is to be returned
        Keyword argument as: the desired types for the data, in order of preference
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: the data from the object
        """
        _code = 'core'
        _subcode = 'getd'

        aetools.keysubst(_arguments, self._argmap_get)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_make = {
        'new' : 'kocl',
        'at' : 'insh',
        'to' : 'to  ',
        'with_data' : 'data',
        'with_properties' : 'prdt',
    }

    def make(self, _no_object=None, _attributes={}, **_arguments):
        """make: Make a new element
        Keyword argument new: the class of the new element
        Keyword argument at: the location at which to insert the element
        Keyword argument to: when creating an alias file, the original item to create an alias to
        Keyword argument with_data: the initial data for the element
        Keyword argument with_properties: the initial values for the properties of the element
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: to the new object(s)
        """
        _code = 'core'
        _subcode = 'crel'

        aetools.keysubst(_arguments, self._argmap_make)
        if _no_object != None: raise TypeError, 'No direct arg expected'


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_move = {
        'to' : 'insh',
        'replacing' : 'alrp',
        'positioned_at' : 'mvpl',
        'routing_suppressed' : 'rout',
    }

    def move(self, _object, _attributes={}, **_arguments):
        """move: Move object(s) to a new location
        Required argument: the object(s) to move
        Keyword argument to: the new location for the object(s)
        Keyword argument replacing: Specifies whether or not to replace items in the destination that have the same name as items being moved
        Keyword argument positioned_at: Gives a list (in local window coordinates) of positions for the destination items
        Keyword argument routing_suppressed: Specifies whether or not to autoroute items (default is false). Only applies when moving to the system folder.
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: to the object(s) after they have been moved
        """
        _code = 'core'
        _subcode = 'move'

        aetools.keysubst(_arguments, self._argmap_move)
        _arguments['----'] = _object

        aetools.enumsubst(_arguments, 'alrp', _Enum_bool)
        aetools.enumsubst(_arguments, 'mvpl', _Enum_list)
        aetools.enumsubst(_arguments, 'rout', _Enum_bool)

        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_open = {
        'using' : 'usin',
        'with_properties' : 'prdt',
    }

    def open(self, _object, _attributes={}, **_arguments):
        """open: Open the specified object(s)
        Required argument: list of objects to open
        Keyword argument using: the application file to open the object with
        Keyword argument with_properties: the initial values for the properties, to be sent along with the open event sent to the application that opens the direct object
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'aevt'
        _subcode = 'odoc'

        aetools.keysubst(_arguments, self._argmap_open)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    def _print(self, _object, _attributes={}, **_arguments):
        """print: Print the specified object(s)
        Required argument: list of objects to print
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'aevt'
        _subcode = 'pdoc'

        if _arguments: raise TypeError, 'No optional args expected'
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_quit = {
        'saving' : 'savo',
    }

    def quit(self, _no_object=None, _attributes={}, **_arguments):
        """quit: Quit the Finder (direct parameter ignored)
        Keyword argument saving: specifies whether to save currently open documents (not supported by Finder)
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'aevt'
        _subcode = 'quit'

        aetools.keysubst(_arguments, self._argmap_quit)
        if _no_object != None: raise TypeError, 'No direct arg expected'

        aetools.enumsubst(_arguments, 'savo', _Enum_savo)

        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_save = {
        '_in' : 'kfil',
        'as' : 'fltp',
    }

    def save(self, _object, _attributes={}, **_arguments):
        """save: Save an object (Not supported by Finder)
        Required argument: the object to save
        Keyword argument _in: the file in which to save the object (not supported by Finder)
        Keyword argument as: the file type of the document in which to save the data (not supported by Finder)
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'core'
        _subcode = 'save'

        aetools.keysubst(_arguments, self._argmap_save)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_set = {
        'to' : 'data',
    }

    def set(self, _object, _attributes={}, **_arguments):
        """set: Set an object's data
        Required argument: the object to change
        Keyword argument to: the new value
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'core'
        _subcode = 'setd'

        aetools.keysubst(_arguments, self._argmap_set)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']

    _argmap_suite_info = {
        '_in' : 'wrcd',
    }

    def suite_info(self, _object, _attributes={}, **_arguments):
        """suite info: Get information about event suite(s)
        Required argument: the suite for which to return information
        Keyword argument _in: the human language and script system in which to return information
        Keyword argument _attributes: AppleEvent attribute dictionary
        Returns: a record containing the suites and their versions
        """
        _code = 'core'
        _subcode = 'gtsi'

        aetools.keysubst(_arguments, self._argmap_suite_info)
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']


class application(aetools.ComponentItem):
    """application - An application program"""
    want = 'capp'
class about_this_computer(aetools.NProperty):
    """about this computer - the "About this Computer" dialog and the list of running processes displayed in it"""
    which = 'abbx'
    want = 'obj '
class apple_menu_items_folder(aetools.NProperty):
    """apple menu items folder - the special folder named "Apple Menu Items," the contents of which appear in the Apple menu"""
    which = 'amnu'
    want = 'obj '
class clipboard(aetools.NProperty):
    """clipboard - the Finder's clipboard window"""
    which = 'pcli'
    want = 'obj '
class control_panels_folder(aetools.NProperty):
    """control panels folder - the special folder named 'Control Panels'"""
    which = 'ctrl'
    want = 'obj '
class desktop(aetools.NProperty):
    """desktop - the desktop"""
    which = 'desk'
    want = 'obj '
class extensions_folder(aetools.NProperty):
    """extensions folder - the special folder named 'Extensions'"""
    which = 'extn'
    want = 'obj '
class file_sharing(aetools.NProperty):
    """file sharing - Is file sharing on?"""
    which = 'fshr'
    want = 'bool'
class Finder_preferences(aetools.NProperty):
    """Finder preferences - Various preferences that apply to the Finder as a whole"""
    which = 'pfrp'
    want = 'obj '
class fonts_folder(aetools.NProperty):
    """fonts folder - the special folder named 'Fonts'"""
    which = 'ffnt'
    want = 'obj '
class frontmost(aetools.NProperty):
    """frontmost - Is the Finder the frontmost process?"""
    which = 'pisf'
    want = 'bool'
class insertion_location(aetools.NProperty):
    """insertion location - the container in which a new folder would appear if "New Folder" was selected"""
    which = 'pins'
    want = 'obj '
class largest_free_block(aetools.NProperty):
    """largest free block - the largest free block of process memory available to launch an application"""
    which = 'mfre'
    want = 'long'
class preferences_folder(aetools.NProperty):
    """preferences folder - the special folder named 'Preferences'"""
    which = 'pref'
    want = 'obj '
class product_version(aetools.NProperty):
    """product version - the version of the System software running on this computer"""
    which = 'ver2'
    want = 'itxt'
class selection(aetools.NProperty):
    """selection - the selection visible to the user"""
    which = 'sele'
    want = 'obj '
class sharing_starting_up(aetools.NProperty):
    """sharing starting up - Is file sharing in the process of starting up?"""
    which = 'fsup'
    want = 'bool'
class shutdown_items_folder(aetools.NProperty):
    """shutdown items folder - the special folder named 'Shutdown Items'"""
    which = 'shdf'
    want = 'obj '
class startup_items_folder(aetools.NProperty):
    """startup items folder - the special folder named 'Startup Items'"""
    which = 'strt'
    want = 'obj '
class system_folder(aetools.NProperty):
    """system folder - the System folder"""
    which = 'macs'
    want = 'obj '
class temporary_items_folder(aetools.NProperty):
    """temporary items folder - the special folder named "Temporary Items" (invisible)"""
    which = 'temp'
    want = 'obj '
class version(aetools.NProperty):
    """version - the version of the Finder"""
    which = 'vers'
    want = 'itxt'
class view_preferences(aetools.NProperty):
    """view preferences - backwards compatibility with Finder Scripting Extension. DEPRECATED -- not supported after Finder 8.0"""
    which = 'pvwp'
    want = 'obj '
class visible(aetools.NProperty):
    """visible - Is the Finder's layer visible?"""
    which = 'pvis'
    want = 'bool'
#        element 'dsut' as ['indx', 'name']
#        element 'alia' as ['indx', 'name']
#        element 'appf' as ['indx', 'name', 'ID  ']
#        element 'clpf' as ['indx', 'name']
#        element 'lwnd' as ['indx', 'name']
#        element 'ctnr' as ['indx', 'name']
#        element 'cwnd' as ['indx', 'name']
#        element 'dwnd' as ['indx', 'name']
#        element 'ccdv' as ['indx', 'name']
#        element 'dafi' as ['indx', 'name']
#        element 'cdsk' as ['indx', 'name']
#        element 'cdis' as ['indx', 'name', 'ID  ']
#        element 'docf' as ['indx', 'name']
#        element 'file' as ['indx', 'name']
#        element 'cfol' as ['indx', 'name', 'ID  ']
#        element 'fntf' as ['indx', 'name']
#        element 'fsut' as ['indx', 'name']
#        element 'iwnd' as ['indx', 'name']
#        element 'cobj' as ['indx', 'name']
#        element 'sctr' as ['indx', 'name']
#        element 'swnd' as ['indx', 'name']
#        element 'sndf' as ['indx', 'name']
#        element 'qwnd' as ['indx', 'name']
#        element 'stcs' as ['indx', 'name']
#        element 'ctrs' as ['indx', 'name']
#        element 'cwin' as ['indx', 'name']

class file(aetools.ComponentItem):
    """file - A file"""
    want = 'file'
class creator_type(aetools.NProperty):
    """creator type - the OSType identifying the application that created the item"""
    which = 'fcrt'
    want = 'type'
class file_type_obsolete(aetools.NProperty):
    """file type obsolete - the OSType identifying the type of data contained in the item (DEPRECATED - for use with scripts compiled before Finder 8.0. Will be removed in the next release)"""
    which = 'fitp'
    want = 'type'
class file_type(aetools.NProperty):
    """file type - the OSType identifying the type of data contained in the item"""
    which = 'asty'
    want = 'type'
class locked_obsolete(aetools.NProperty):
    """locked obsolete - Is the file locked? (DEPRECATED - for use with scripts compiled before Finder 8.0. Will be removed in the next release)"""
    which = 'islk'
    want = 'bool'
class locked(aetools.NProperty):
    """locked - Is the file locked?"""
    which = 'aslk'
    want = 'bool'
# repeated property product_version the version of the product (visible at the top of the "Get Info" window)
class stationery(aetools.NProperty):
    """stationery - Is the file a stationery pad?"""
    which = 'pspd'
    want = 'bool'
# repeated property version the version of the file (visible at the bottom of the "Get Info" window)

files = file

class window(aetools.ComponentItem):
    """window - A window"""
    want = 'cwin'
class collapsed(aetools.NProperty):
    """collapsed - Is the window collapsed (only applies to non-pop-up windows)?"""
    which = 'wshd'
    want = 'bool'
class popup(aetools.NProperty):
    """popup - Is the window is a pop-up window?"""
    which = 'drwr'
    want = 'bool'
class pulled_open(aetools.NProperty):
    """pulled open - Is the window pulled open (only applies to pop-up windows)?"""
    which = 'pull'
    want = 'bool'
# repeated property visible Is the window visible (always true for Finder windows)?
class zoomed_full_size(aetools.NProperty):
    """zoomed full size - Is the window zoomed to the full size of the screen? (can only be set, not read)"""
    which = 'zumf'
    want = 'bool'

windows = window
# XXXX application element 'dsut' not found!!
# XXXX application element 'alia' not found!!
# XXXX application element 'appf' not found!!
# XXXX application element 'clpf' not found!!
# XXXX application element 'lwnd' not found!!
# XXXX application element 'ctnr' not found!!
# XXXX application element 'cwnd' not found!!
# XXXX application element 'dwnd' not found!!
# XXXX application element 'ccdv' not found!!
# XXXX application element 'dafi' not found!!
# XXXX application element 'cdsk' not found!!
# XXXX application element 'cdis' not found!!
# XXXX application element 'docf' not found!!
# XXXX application element 'cfol' not found!!
# XXXX application element 'fntf' not found!!
# XXXX application element 'fsut' not found!!
# XXXX application element 'iwnd' not found!!
# XXXX application element 'cobj' not found!!
# XXXX application element 'sctr' not found!!
# XXXX application element 'swnd' not found!!
# XXXX application element 'sndf' not found!!
# XXXX application element 'qwnd' not found!!
# XXXX application element 'stcs' not found!!
# XXXX application element 'ctrs' not found!!
application._propdict = {
    'about_this_computer' : about_this_computer,
    'apple_menu_items_folder' : apple_menu_items_folder,
    'clipboard' : clipboard,
    'control_panels_folder' : control_panels_folder,
    'desktop' : desktop,
    'extensions_folder' : extensions_folder,
    'file_sharing' : file_sharing,
    'Finder_preferences' : Finder_preferences,
    'fonts_folder' : fonts_folder,
    'frontmost' : frontmost,
    'insertion_location' : insertion_location,
    'largest_free_block' : largest_free_block,
    'preferences_folder' : preferences_folder,
    'product_version' : product_version,
    'selection' : selection,
    'sharing_starting_up' : sharing_starting_up,
    'shutdown_items_folder' : shutdown_items_folder,
    'startup_items_folder' : startup_items_folder,
    'system_folder' : system_folder,
    'temporary_items_folder' : temporary_items_folder,
    'version' : version,
    'view_preferences' : view_preferences,
    'visible' : visible,
}
application._elemdict = {
    'file' : file,
    'window' : window,
}
file._propdict = {
    'creator_type' : creator_type,
    'file_type_obsolete' : file_type_obsolete,
    'file_type' : file_type,
    'locked_obsolete' : locked_obsolete,
    'locked' : locked,
    'product_version' : product_version,
    'stationery' : stationery,
    'version' : version,
}
file._elemdict = {
}
window._propdict = {
    'collapsed' : collapsed,
    'popup' : popup,
    'pulled_open' : pulled_open,
    'visible' : visible,
    'zoomed_full_size' : zoomed_full_size,
}
window._elemdict = {
}
# XXXX enum list not found!!
# XXXX enum bool not found!!
# XXXX enum savo not found!!

#
# Indices of types declared in this module
#
_classdeclarations = {
    'cwin' : window,
    'file' : file,
    'capp' : application,
}

_propdeclarations = {
    'amnu' : apple_menu_items_folder,
    'pvwp' : view_preferences,
    'extn' : extensions_folder,
    'pins' : insertion_location,
    'fshr' : file_sharing,
    'aslk' : locked,
    'drwr' : popup,
    'fcrt' : creator_type,
    'pcli' : clipboard,
    'asty' : file_type,
    'strt' : startup_items_folder,
    'islk' : locked_obsolete,
    'pvis' : visible,
    'pref' : preferences_folder,
    'pisf' : frontmost,
    'sele' : selection,
    'temp' : temporary_items_folder,
    'pull' : pulled_open,
    'abbx' : about_this_computer,
    'wshd' : collapsed,
    'pspd' : stationery,
    'fitp' : file_type_obsolete,
    'pfrp' : Finder_preferences,
    'desk' : desktop,
    'fsup' : sharing_starting_up,
    'mfre' : largest_free_block,
    'ctrl' : control_panels_folder,
    'zumf' : zoomed_full_size,
    'shdf' : shutdown_items_folder,
    'ffnt' : fonts_folder,
    'macs' : system_folder,
    'ver2' : product_version,
    'vers' : version,
}

_compdeclarations = {
}

_enumdeclarations = {
}
