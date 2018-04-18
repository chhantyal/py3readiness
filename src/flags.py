"""
It contains all the projects that can be ignored in graph. For example, there
are many Mozilla libs with large download stat which are not really used by
community. See issue #22
"""

FLAGS = {
    "rackspace-novaclient":
        "https://github.com/rackerlabs/rackspace-novaclient",
    "manifestparser": "https://pypi.org/project/manifestparser",
    "mozrunner": "https://pypi.org/project/mozrunner",
    "moznetwork": "https://pypi.org/project/moznetwork",
    "mozdevice": "https://pypi.org/project/mozdevice",
    "mozprofile": "https://pypi.org/project/mozprofile",
    "mozprocess": "https://pypi.org/project/mozprocess",
    "mozfile": "https://pypi.org/project/mozfile",
    "mozinfo": "https://pypi.org/project/mozinfo",
    "mozlog": "https://pypi.org/project/mozlog",
    "mozcrash": "https://pypi.org/project/mozcrash",
    "mozhttpd": "https://pypi.org/project/mozhttpd",
    "moztest": "https://pypi.org/project/moztest",
    "mozversion": "https://pypi.org/project/mozversion",
    "marionette_client": "https://pypi.org/project/marionette_client",
    "marionette-transport": "https://pypi.org/project/marionette-transport",
}
