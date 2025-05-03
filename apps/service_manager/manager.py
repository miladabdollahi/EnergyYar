from apps.core.structs import Manager


class ServiceManager(Manager):
    services = dict()

    def set(self, manager, scope=None):
        """
        Set a service manager.

        :param ServiceManager manager: service manager instance.
        :param scope:
        """

        if isinstance(manager, Manager):
            if scope is not None and isinstance(scope, str):
                key = manager.__module__[:manager.__module__.rfind(scope) - 1]
                service = self.services.get(key)
                if service is not None:
                    service.update({scope: manager})
                else:
                    self.services.update({
                        key: {scope: manager}
                    })
            else:
                self.services.update({manager.__module__: manager})

    def get(self, name, scope=None):
        """
        Get a service manager.

        :param str name: service manager name.
        :param scope:
        """

        service = self.services.get(name)
        if isinstance(service, Manager):
            return service
        if scope is not None and isinstance(service, dict):
            return service.get(scope)
        else:
            raise Exception('Service [{name}] not registered.'.format(name=f'{name}:{scope}'))


service_manager = ServiceManager()
