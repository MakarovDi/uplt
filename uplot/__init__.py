import sys

# import the actual implementation package
import uplt

# import everything is do nothing really
# only for static type checkers and analysis tools
from uplt import * # type: ignore # noqa: F403

# make 'uplot' a true alias for 'uplt' in the module cache
sys.modules['uplot'] = uplt
