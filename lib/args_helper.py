class CustomArgs(object):
    pass

_args = CustomArgs()

def get_global_args():
    global _args
    return _args

def set_global_arg(arg, value):
    global _args
    setattr(_args, arg,value)

def set_global_args(args):
    for k,v in args.items():
        set_global_arg(k, v)

def set_dry_run():
    set_global_arg('dry_run', True)

def is_dry_run():
    global _args
    return hasattr(_args, 'dry_run') and _args.dry_run

def set_production():
    set_global_arg('production', True)

def is_production():
    global _args
    return hasattr(_args, 'production') and _args.production
