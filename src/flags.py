"""
It contains all the projects that can be ignored in graph. For example, there
are many Mozilla libs with large download stat which are not really used by
community. See issue #22
"""

FLAGS = {
    "rackspace-novaclient": "https://github.com/rackerlabs/rackspace-novaclient",
    "manifestparser": "https://pypi.python.org/pypi/manifestparser",
    "mozrunner": "https://pypi.python.org/pypi/mozrunner",
    "moznetwork": "https://pypi.python.org/pypi/moznetwork",
    "mozdevice": "https://pypi.python.org/pypi/mozdevice",
    "mozprofile": "https://pypi.python.org/pypi/mozprofile",
    "mozprocess": "https://pypi.python.org/pypi/mozprocess",
    "mozfile": "https://pypi.python.org/pypi/mozfile",
    "mozinfo": "https://pypi.python.org/pypi/mozinfo",
    "mozlog": "https://pypi.python.org/pypi/mozlog",
    "mozcrash": "https://pypi.python.org/pypi/mozcrash",
    "mozhttpd": "https://pypi.python.org/pypi/mozhttpd",
    "moztest": "https://pypi.python.org/pypi/moztest",
    "mozversion": "https://pypi.python.org/pypi/mozversion",
    "marionette_client": "https://pypi.python.org/pypi/marionette_client",
    "marionette-transport": "https://pypi.python.org/pypi/marionette-transport",
}
