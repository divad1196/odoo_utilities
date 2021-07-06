import inspect
import logging
_logger = logging.getLogger(__name__)


#==========================
# analyse the process of a function in a model, example:
# write = func_code_analyse(env, 'sale.order', 'write')
# it = iter(write)
# printn(it) # call this up an error occurs -> you've reached the end

def get_model(env, model_name):
    return type(env[model_name])

def source(f):
    return inspect.getsource(f)


def func_code_analyse(env, model, function):
    """get a list with the source code of the function through all inheritance """
    m = get_model(env, model)
    return ["""model: {model}\nmodule: {module}\n\n{source}""".format(
        model=cls,
        module=cls.__module__,
        source=source(getattr(cls,function)))
        for cls in m.__mro__
        if function in cls.__dict__
    ]


def func_like_code_analyse(env, model, function):
    """has func_code_analyse but permissive about the function name (name.lower().find(function.lower()))"""
    m = get_model(env, model)
    functions = {}
    for cls in m.__mro__:
        for name, attr in inspect.getmembers(cls, inspect.isfunction):
            if name.lower().find(function.lower()) != -1:
                if name in functions:
                    functions[name].append({
                        'model': cls,
                        'source': attr,
                    })
                else:
                    functions[name] = [({
                        'model': cls,
                        'source': attr,
                    })]
    results = {f: ["""
    model: {model}
    module: {module}

    {source}

    """.format(model=s['model'],module=s['model'].__module__,source=source(s['source'])) for s in sources
    ]
    for f, sources in functions.items()
    }
    return results



def get_attr(m, attr):
    el = inspect.getmembers(m)
    return [e for e in el if e[0].find(attr) != -1]


def print_func_code(env, model, function):
    """ Use func_code_analyse and print it with START and STOP clearly writen and separator between functions """
    print("\n\u001b[32mSTART\u001b[0m\n")
    for e in func_code_analyse(env, model, function):
        print(e)
        print("\n\u001b[31m" + ("-"*30) + "\u001b[0m\n")
    print("\n\n\u001b[32mDONE\u001b[0m\n")


def print_field(env, model, field):
    """ Print all attributes that define the field such as string or compute """
    m = get_model(env, model)
    f = getattr(m, field)
    for k, v in sorted(f._slots.items()):
        attr = str(k).ljust(20)
        if v is False:
            print(attr, "\u001b[31m" + str(v) + "\u001b[0m")
        elif not v:
            print(attr, v)
        else:
            print(attr, "\u001b[32m" + str(v) + "\u001b[0m")


#############################################################################################################################################################


def getParents():
    return inspect.getouterframes(inspect.currentframe())


def extract_frameinfo(frameinfo):
    self = frameinfo.frame.f_locals.get("self")
    _name = self and getattr(type(self), "_name", None)
    return (frameinfo.function, _name, frameinfo.filename)

def get_odoo_stack():
    return [
        extract_frameinfo(x)
        for x in reversed(getParents())
    ]

def printTraceBack(printer=print):
    """ Print the Traceback of the function call """
    for function, model, filename in get_odoo_stack()[:-3]:
        printer(
            "{:<30}\t{:<30}\t{}".format(function, model or "unkown", filename)
        )

# NB:
# getParents()[2:] retire les 2 premiers enfants de la list, à savoir la fonction getParents et print*Traceback
# dans le shell Odoo, il est mieux utiliser getParents()[2:-10] car il y a des appels de fonctions pour lancer le shell

#############################################################################################################################################################
# ANALYSER LES DEPENDS ET ONCHANGE

def _get_onchange_methods(env, model):
        return inspect.getmembers(get_model(env, model), lambda cls : hasattr(cls, '_onchange'))

def _get_depends_methods(env, model):
        return inspect.getmembers(get_model(env, model), lambda cls : hasattr(cls, '_depends'))

def get_onchange_methods(env, model):
    functions = _get_onchange_methods(env, model)
    return [{
        "keys" : f[1]._onchange,
        "name" : f[0],
        "code" : f[1],
    } for f in functions]

def get_depends_methods(env, model):
    functions = _get_depends_methods(env, model)
    return [{
        "keys" : f[1]._depends,
        "name" : f[0],
        "code" : f[1],
    } for f in functions]

def analyse_onchange(env, model):
    for name, func in _get_onchange_methods(env, model):
        print_func_code(env, model, name)
        print("\n\n\u001b[34m" + ("=" * 30) + "\n" + ("=" * 30) + "\u001b[0m\n\n")

def analyse_depends(env, model):
    for name, func in _get_depends_methods(env, model):
        print_func_code(env, model, name)
        print("\n\n\u001b[34m" + ("=" * 30) + "\n" + ("=" * 30) + "\u001b[0m\n\n")
