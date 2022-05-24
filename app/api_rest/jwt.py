from api_rest.serializer import AccountSerializer


def get_permissions(user):
    permissions = {}
    for permission in user.get_all_permissions():
        module_permission = permission.split(".")
        data = module_permission[1].split("_")
        resource = data[1]
        if resource not in permissions:
            permi = [data[0]]
            permissions[resource] = permi
        else:
            permissions[resource].append(data[0])

    return permissions


def get_modules(user):
    modules = {}
    for permission in user.get_all_permissions():
        module_permission = permission.split(".")
        module = module_permission[0]
        resource = module_permission[1].split("_")[1]

        if module not in modules:
            modules[module] = set([resource])
        else:
            modules[module].add(resource)

    return modules


def jwt_response_payload_handler(token, user=None, request=None, algo=None):
    return {
        "token": token,
        "user": AccountSerializer(user, context={"request": request}).data,
        "permissions": get_permissions(user),
        "modules": get_modules(user),
    }
