from crequest.middleware import CrequestMiddleware


def get_user():
    request = CrequestMiddleware.get_request()
    return request.user
