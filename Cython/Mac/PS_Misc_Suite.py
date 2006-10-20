"Apple Event suite for pyserver."

import aetools
import MacOS

_code = 'misc'

class PS_Misc_Suite:

    def DoScript(self, _object, _attributes={}, **_arguments):
        """DoScript: Execute a Python file, optionally with command line args.
        Required argument: filename.py or [filename.py, arg, ...]
        Keyword argument _attributes: AppleEvent attribute dictionary
        """
        _code = 'misc'
        _subcode = 'dosc'

        if _arguments: raise TypeError, 'No optional args expected'
        _arguments['----'] = _object


        _reply, _arguments, _attributes = self.send(_code, _subcode,
                _arguments, _attributes)
        if _arguments.has_key('errn'):
            raise aetools.Error, aetools.decodeerror(_arguments)
        # XXXX Optionally decode result
        if _arguments.has_key('----'):
            return _arguments['----']


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
