from apps.service_manager.manager import service_manager
from importlib import import_module


def register_service(scope=None):
    """
    decorator to register a service manager.

    :returns: status hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available status hooks.

        :param type cls: status hook class.

        :returns: status hook class.
        :rtype: type
        """

        instance = cls()
        service_manager.set(instance, scope)

        return cls

    return decorator


def use(service_path, scope=None):
    """
    use services with service path and scope.

    :param str service_path:
    :param str scope:
    """

    class __ServiceLazyObject:

        def __init__(self, __service_path, scope=None):
            self.__service_path = __service_path
            self.__scope = scope

        def __getattr__(self, name):
            import_module(self.__service_path)
            service = service_manager.get(self.__service_path, self.__scope)
            if service is None:
                raise Exception('This path is not registered in service.')

            return getattr(service, name)

    return __ServiceLazyObject(service_path, scope)
