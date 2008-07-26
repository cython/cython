"""Suite Misc Suite: Suite that adds additional features to the Application.
Level 1, version 1

Generated from Macintosh HD:Desktop Folder:ToolServer 3.4.1:ToolServer
AETE/AEUT resource version 1/0, language 0, script 0
"""

import aetools
import MacOS

_code = 'misc'

class TS_Misc_Suite:

    def DoScript(self, _object, _attributes={}, **_arguments):
        """DoScript: Execute an MPW command, any command that could be executed from the command line can be sent as a script.
        Required argument: The script to execute
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'misc'
        _subcode = 'dosc'

        if _arguments: raise TypeError, 'No optional args expected'
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        #if _arguments.has_key('errn'):
        #	raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        #if _arguments.has_key('----'):
        #	return _arguments['----']
        errn = 0
        stat = 0
        stdout = ""
        stderr = ""
        if _arguments.has_key('errn'):
            errn = _arguments['errn']
            if errn:
                errn = aetools.decodeerror(_arguments)
        if _arguments.has_key('stat'):
            stat = _arguments['stat']
        if _arguments.has_key('----'):
            stdout = _arguments['----']
        if _arguments.has_key('diag'):
            stderr = _arguments['diag']
        return (errn, stat, stdout, stderr)


#
# Indices of types declared in this module
#
_classdeclarations = {
}

_propdeclarations = {
}

_compdeclarations = {
}

_enumdeclarations = {
}
