"""
Main application entry point / runner for RPyMostat Engine.

The latest version of this package is available at:
<http://github.com/jantman/RPyMostat>

##################################################################################
Copyright 2016 Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>

    This file is part of RPyMostat, also known as RPyMostat.

    RPyMostat is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    RPyMostat is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with RPyMostat.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
##################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/RPyMostat> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
##################################################################################

AUTHORS:
Jason Antman <jason@jasonantman.com> <http://www.jasonantman.com>
##################################################################################
"""

import os


class Config(object):
    """
    RPyMostat configuration. Reads configuration from environmnet variables,
    sets defaults for anything missing.
    """

    # dict describing valid configuration variables
    # Keys are setting names, values are dicts with elements:
    #
    # - ``env_var_name`` - environment variable name for this setting
    # - ``description`` - description of this variable
    # - ``is_int`` - boolean, whether the value should be an int or a str
    # - ``default_value`` - default value if not present in os.environ
    #
    _config_vars = {
        'api_port': {
            'env_var_name': 'API_PORT',
            'description': 'port number to run API server on',
            'is_int': True,
            'default_value': 8088
        }
    }

    def __init__(self):
        """
        Initialize ``self._config`` with defaults, replace any settings that
        have the appropriate env vars set.
        """
        self._config = self._get_from_env()

    def get(self, setting_name):
        """
        Return the effective value for the configuration option ``setting_name``

        :param setting_name: the config setting to get
        :type setting_name: str
        :return: str or int configuration value
        """
        return self._config[setting_name]

    @property
    def as_dict(self):
        """
        Return the full configuration dictionary, setting names to values.

        :return: configuration dict
        :rtype: dict
        """
        return self._config

    def _get_from_env(self):
        """
        Build ``self._config`` from env vars and defaults
        (``self._config_vars``).

        :return: effective configuration dict
        """
        res = {}
        for name, info in self._config_vars.items():
            res[name] = info['default_value']
            if info['env_var_name'] in os.environ:
                res[name] = os.environ.get(info['env_var_name'])
                if info['is_int']:
                    res[name] = int(res[name])
        return res

    def get_var_info(self):
        """
        Return information about configuration variables. Returns a dict keyed
        by setting name. Values are dicts with keys:

        - ``env_var_name`` - environment variable name for this setting
        - ``description`` - description of this variable
        - ``is_int`` - boolean, whether the value should be an int or a str
        - ``default_value`` - default value if not present in os.environ

        :return: dict describing configuration variables
        :rtype: dict
        """
        return self._config_vars
