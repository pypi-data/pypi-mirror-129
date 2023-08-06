__all__ = ["AsDataArray", "asdataarray"]


# standard library
from dataclasses import Field
from functools import wraps
from types import MethodType
from typing import Any, Callable, Dict, Optional, Type, TypeVar, Union, overload


# dependencies
import numpy as np
import xarray as xr
from morecopy import copy
from typing_extensions import ParamSpec, Protocol


# submodules
from .datamodel import DataModel
from .dataoptions import DataOptions
from .typing import DataType, Order, Shape, Sizes


# constants
DEFAULT_OPTIONS = DataOptions(xr.DataArray)


# type hints
P = ParamSpec("P")
TDataArray = TypeVar("TDataArray", bound=xr.DataArray)
TDataArray_ = TypeVar("TDataArray_", bound=xr.DataArray, contravariant=True)


class DataClass(Protocol[P]):
    """Type hint for a dataclass object."""

    __init__: Callable[P, None]
    __dataclass_fields__: Dict[str, Field[Any]]


class DataArrayClass(Protocol[P, TDataArray_]):
    """Type hint for a dataclass object with a DataArray factory."""

    __init__: Callable[P, None]
    __dataclass_fields__: Dict[str, Field[Any]]
    __dataoptions__: DataOptions[TDataArray_]


# custom classproperty
class classproperty:
    """Class property only for AsDataArray.new().

    As a classmethod and a property can be chained together since Python 3.9,
    this class will be removed when the support for Python 3.7 and 3.8 ends.

    """

    def __init__(self, func: Callable[..., Callable[P, TDataArray]]) -> None:
        self.__func__ = func

    def __get__(
        self,
        obj: Any,
        cls: Type[DataArrayClass[P, TDataArray]],
    ) -> Callable[P, TDataArray]:
        return self.__func__(cls)


# runtime functions and classes
@overload
def asdataarray(
    dataclass: DataArrayClass[Any, TDataArray],
    reference: Optional[DataType] = None,
    dataoptions: Any = DEFAULT_OPTIONS,
) -> TDataArray:
    ...


@overload
def asdataarray(
    dataclass: DataClass[Any],
    reference: Optional[DataType] = None,
    dataoptions: DataOptions[TDataArray] = DEFAULT_OPTIONS,
) -> TDataArray:
    ...


def asdataarray(
    dataclass: Any,
    reference: Any = None,
    dataoptions: Any = DEFAULT_OPTIONS,
) -> Any:
    """Create a DataArray object from a dataclass object.

    Args:
        dataclass: Dataclass object that defines typed DataArray.
        reference: DataArray or Dataset object as a reference of shape.
        dataoptions: Options for DataArray creation.

    Returns:
        DataArray object created from the dataclass object.

    """
    try:
        # for backward compatibility (deprecated in v1.0.0)
        dataoptions = DataOptions(dataclass.__dataarray_factory__)
    except AttributeError:
        pass

    try:
        dataoptions = dataclass.__dataoptions__
    except AttributeError:
        pass

    model = DataModel.from_dataclass(dataclass)
    dataarray = dataoptions.factory(model.data[0](reference))

    for coord in model.coord:
        dataarray.coords.update({coord.name: coord(dataarray)})

    for attr in model.attr:
        dataarray.attrs.update({attr.name: attr()})

    for name in model.name:
        dataarray.name = name()

    return dataarray


class AsDataArray:
    """Mix-in class that provides shorthand methods."""

    __dataoptions__ = DEFAULT_OPTIONS

    @classproperty
    def new(cls: Type[DataArrayClass[P, TDataArray]]) -> Callable[P, TDataArray]:
        """Create a DataArray object from dataclass parameters."""

        init = copy(cls.__init__)
        init.__annotations__["return"] = TDataArray
        init.__doc__ = cls.__init__.__doc__

        @wraps(init)
        def new(
            cls: Type[DataArrayClass[P, TDataArray]],
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> TDataArray:
            return asdataarray(cls(*args, **kwargs))

        return MethodType(new, cls)

    @classmethod
    def empty(
        cls: Type[DataArrayClass[P, TDataArray]],
        shape: Union[Shape, Sizes],
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataArray:
        """Create a DataArray object without initializing data.

        Args:
            shape: Shape or sizes of the new DataArray object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the DataArray class except for data.

        Returns:
            DataArray object without initializing data.

        """
        model = DataModel.from_dataclass(cls)
        name = model.data[0].name
        dims = model.data[0].type["dims"]

        if isinstance(shape, dict):
            shape = tuple(shape[dim] for dim in dims)

        data = np.empty(shape, order=order)
        return asdataarray(cls(**{name: data}, **kwargs))

    @classmethod
    def zeros(
        cls: Type[DataArrayClass[P, TDataArray]],
        shape: Union[Shape, Sizes],
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataArray:
        """Create a DataArray object filled with zeros.

        Args:
            shape: Shape or sizes of the new DataArray object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the DataArray class except for data.

        Returns:
            DataArray object filled with zeros.

        """
        model = DataModel.from_dataclass(cls)
        name = model.data[0].name
        dims = model.data[0].type["dims"]

        if isinstance(shape, dict):
            shape = tuple(shape[dim] for dim in dims)

        data = np.zeros(shape, order=order)
        return asdataarray(cls(**{name: data}, **kwargs))

    @classmethod
    def ones(
        cls: Type[DataArrayClass[P, TDataArray]],
        shape: Union[Shape, Sizes],
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataArray:
        """Create a DataArray object filled with ones.

        Args:
            shape: Shape or sizes of the new DataArray object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the DataArray class except for data.

        Returns:
            DataArray object filled with ones.

        """
        model = DataModel.from_dataclass(cls)
        name = model.data[0].name
        dims = model.data[0].type["dims"]

        if isinstance(shape, dict):
            shape = tuple(shape[dim] for dim in dims)

        data = np.ones(shape, order=order)
        return asdataarray(cls(**{name: data}, **kwargs))

    @classmethod
    def full(
        cls: Type[DataArrayClass[P, TDataArray]],
        shape: Union[Shape, Sizes],
        fill_value: Any,
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataArray:
        """Create a DataArray object filled with given value.

        Args:
            shape: Shape or sizes of the new DataArray object.
            fill_value: Value for the new DataArray object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the DataArray class except for data.

        Returns:
            DataArray object filled with given value.

        """
        model = DataModel.from_dataclass(cls)
        name = model.data[0].name
        dims = model.data[0].type["dims"]

        if isinstance(shape, dict):
            shape = tuple(shape[dim] for dim in dims)

        data = np.full(shape, fill_value, order=order)
        return asdataarray(cls(**{name: data}, **kwargs))
