from importlib import import_module
# from zemailer.settings import configuration


def get_module_by_name(path: str):
    try:
        module = import_module(path)
    except ModuleNotFoundError:
        raise
    return module



# def get_backend(path: str):
#     module = get_module_by_name('zemailer.core.backends')
#     for backend in configuration.BACKENDS:
#         path, backend = path.split('.', maxsplit=1)
#         i = getattr(module, backend)
#         if i:
#             break
#     return i
