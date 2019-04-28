"""
Wrapper over `pyxdg` (in Ubuntu 16.04), or `xdg` (can be installed in some later versions).
"""

import xdg


is_package_xdg   = 'XDG_CACHE_HOME' in xdg.__all__
is_package_pyxdg = 'BaseDirectory'  in xdg.__all__

if is_package_pyxdg:
    from xdg.BaseDirectory import xdg_data_home, xdg_config_home, xdg_cache_home
    XDG_DATA_HOME   = xdg.BaseDirectory.xdg_data_home
    XDG_CONFIG_HOME = xdg.BaseDirectory.xdg_config_home
    XDG_CACHE_HOME  = xdg.BaseDirectory.xdg_cache_home
elif is_package_xdg:
    from xdg import XDG_DATA_HOME, XDG_CONFIG_HOME, XDG_CACHE_HOME
else:
    raise ImportError('Unsupported xdg package installed.')
