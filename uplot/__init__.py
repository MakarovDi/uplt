import sys
import uplt  # import the actual implementation package

# make 'uplot' a true alias for 'uplt' in the module cache
sys.modules['uplot'] = uplt
