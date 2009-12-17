
__all__ = ["Provider", "find_provider"]

import logging
from pluto.base import Fail
from pluto.environment import env

class Provider(object):
    def __init__(self, resource):
        self.log = logging.getLogger("pluto.provider")
        self.resource = resource

    def action_nothing(self):
        pass

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return u"%s[%s]" % (self.__class__.__name__, self.resource)

PROVIDERS = dict(
    debian = dict(
        Package = "pluto.providers.package.apt.DebianAptProvider",
        Service = "pluto.providers.service.debian.DebianServiceProvider",
    ),
    ubuntu = dict(
        Package = "pluto.providers.package.apt.DebianAptProvider",
        Service = "pluto.providers.service.debian.DebianServiceProvider",
    ),
    default = dict(
        File = "pluto.providers.system.FileProvider",
        Directory = "pluto.providers.system.DirectoryProvider",
        Link = "pluto.providers.system.LinkProvider",
        Execute = "pluto.providers.system.ExecuteProvider",
        Script = "pluto.providers.system.ScriptProvider",
        Mount = "pluto.providers.mount.MountProvider",
    ),
)

def find_provider(resource, class_path=None):
    if not class_path:
        try:
            class_path = PROVIDERS[env.system.platform][resource]
        except KeyError:
            class_path = PROVIDERS["default"][resource]

    # elif '.' not in class_path:
    #     return env.extra_providers[class_path]

    try:
        mod_path, class_name = class_path.rsplit('.', 1)
    except ValueError:
        raise Fail("Unable to find provider for %s as %s" % (resource, class_path))
    mod = __import__(mod_path, {}, {}, [class_name])
    return getattr(mod, class_name)

