import pkgutil
import modules
import importlib
from .generic import cms_metaclass


class Controller(object):
    modules = []
    path = None

    def __init__(self):
        self.try_modules()

    def try_modules(self):
        for _, modname, _ in pkgutil.walk_packages(path=modules.__path__,
                                                      prefix=modules.__name__ + '.'):
            importlib.import_module(modname)

        cms_metaclass.menu.finalize()
        self.modules = cms_metaclass.registry

    def get_modules(self):
        return self.modules

    def get_urls(self):
        return cms_metaclass.urlpatterns

controller = Controller()
