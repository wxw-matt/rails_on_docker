class GlobalArgs(object):
    pass

_args = GlobalArgs()

def get_global_args():
    global _args
    return _args

def set_global_arg(arg, value):
    _args.__setattr__(arg,value)

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
