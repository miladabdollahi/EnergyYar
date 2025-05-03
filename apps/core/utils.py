def make_iterable(values, collection=None):
    """
    converts the provided values to iterable.

    it returns a collection of values using the given collection type.

    :param object | list[object] | tuple[object] | set[object] values: value or values to make
                                                                       iterable. if the values
                                                                       are iterable, it just
                                                                       converts the collection
                                                                       to given type.

    :param type[list | tuple | set] collection: collection type to use.
                                                defaults to list if not provided.

    :rtype: list | tuple | set
    """

    if collection is None:
        collection = list

    if values is None:
        return collection()

    if not isinstance(values, (list, tuple, set)):
        values = (values,)

    return collection(values)
