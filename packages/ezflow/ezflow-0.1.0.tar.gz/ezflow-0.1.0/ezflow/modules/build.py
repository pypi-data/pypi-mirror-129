from ..utils import Registry

MODULE_REGISTRY = Registry("MODULE")


def build_module(cfg_grp=None, name=None, instantiate=True, **kwargs):

    """
    Build a module from a registered module name.

    Parameters
    ----------
    name : str
        Name of the registered module.
    cfg : CfgNode
        Config to pass to the module.

    Returns
    -------
    module : object
        The module object.
    """

    if cfg_grp is None:
        assert name is not None, "Must provide name or cfg_grp"
        assert dict(**kwargs) is not None, "Must provide either cfg_grp or kwargs"

    if name is None:
        name = cfg_grp.NAME

    module = MODULE_REGISTRY.get(name)

    if not instantiate:
        return module

    if cfg_grp is None:
        return module(**kwargs)

    return module(cfg_grp, **kwargs)
