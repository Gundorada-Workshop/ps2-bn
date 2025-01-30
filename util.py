from typing import Any, Callable, Dict, List

class Functor:
    __slots__ = ["__func", "__args", "__kwargs"]
    __func: Callable
    __args: List[Any]
    __kwargs: Dict[str, Any]

    def __init__(self, func, *args, **kwargs):
        # Provided arguments when Functor is instantiated are passed to function first
        self.__func = func
        self.__args = args
        self.__kwargs = kwargs
    
    def __call__(self, *args, **kwargs):
        # Arguments provided in __call__ are positioned after those provided when instantiated
        self.__func(*(self.__args + args), **(self.__kwargs | kwargs))
