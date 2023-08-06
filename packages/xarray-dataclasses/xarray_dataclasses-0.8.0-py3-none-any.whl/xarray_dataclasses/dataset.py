__all__ = ["AsDataset", "asdataset"]


# standard library
from dataclasses import Field
from functools import wraps
from types import MethodType
from typing import Any, Callable, Dict, Optional, Type, TypeVar, overload


# dependencies
import numpy as np
import xarray as xr
from morecopy import copy
from typing_extensions import ParamSpec, Protocol


# submodules
from .datamodel import DataModel
from .dataoptions import DataOptions
from .typing import DataType, Order, Sizes


# constants
DEFAULT_OPTIONS = DataOptions(xr.Dataset)


# type hints
P = ParamSpec("P")
TDataset = TypeVar("TDataset", bound=xr.Dataset)
TDataset_ = TypeVar("TDataset_", bound=xr.Dataset, contravariant=True)


class DataClass(Protocol[P]):
    """Type hint for a dataclass object."""

    __init__: Callable[P, None]
    __dataclass_fields__: Dict[str, Field[Any]]


class DatasetClass(Protocol[P, TDataset_]):
    """Type hint for a dataclass object with a Dataset factory."""

    __init__: Callable[P, None]
    __dataclass_fields__: Dict[str, Field[Any]]
    __dataoptions__: DataOptions[TDataset_]


# custom classproperty
class classproperty:
    """Class property only for AsDataset.new().

    As a classmethod and a property can be chained together since Python 3.9,
    this class will be removed when the support for Python 3.7 and 3.8 ends.

    """

    def __init__(self, func: Callable[..., Callable[P, TDataset]]) -> None:
        self.__func__ = func

    def __get__(
        self,
        obj: Any,
        cls: Type[DatasetClass[P, TDataset]],
    ) -> Callable[P, TDataset]:
        return self.__func__(cls)


# runtime functions and classes
@overload
def asdataset(
    dataclass: DatasetClass[Any, TDataset],
    reference: Optional[DataType] = None,
    dataoptions: Any = DEFAULT_OPTIONS,
) -> TDataset:
    ...


@overload
def asdataset(
    dataclass: DataClass[Any],
    reference: Optional[DataType] = None,
    dataoptions: DataOptions[TDataset] = DEFAULT_OPTIONS,
) -> TDataset:
    ...


def asdataset(
    dataclass: Any,
    reference: Any = None,
    dataoptions: Any = DEFAULT_OPTIONS,
) -> Any:
    """Create a Dataset object from a dataclass object.

    Args:
        dataclass: Dataclass object that defines typed Dataset.
        reference: DataArray or Dataset object as a reference of shape.
        dataoptions: Options for Dataset creation.

    Returns:
        Dataset object created from the dataclass object.

    """
    try:
        # for backward compatibility (deprecated in v1.0.0)
        dataoptions = DataOptions(dataclass.__dataset_factory__)
    except AttributeError:
        pass

    try:
        dataoptions = dataclass.__dataoptions__
    except AttributeError:
        pass

    model = DataModel.from_dataclass(dataclass)
    dataset = dataoptions.factory()

    for data in model.data:
        dataset.update({data.name: data(reference)})

    for coord in model.coord:
        dataset.coords.update({coord.name: coord(dataset)})

    for attr in model.attr:
        dataset.attrs.update({attr.name: attr()})

    return dataset


class AsDataset:
    """Mix-in class that provides shorthand methods."""

    __dataoptions__ = DEFAULT_OPTIONS

    @classproperty
    def new(cls: Type[DatasetClass[P, TDataset]]) -> Callable[P, TDataset]:
        """Create a Dataset object from dataclass parameters."""

        init = copy(cls.__init__)
        init.__annotations__["return"] = TDataset
        init.__doc__ = cls.__init__.__doc__

        @wraps(init)
        def new(
            cls: Type[DatasetClass[P, TDataset]],
            *args: P.args,
            **kwargs: P.kwargs,
        ) -> TDataset:
            return asdataset(cls(*args, **kwargs))

        return MethodType(new, cls)

    @classmethod
    def empty(
        cls: Type[DatasetClass[P, TDataset]],
        sizes: Sizes,
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataset:
        """Create a Dataset object without initializing data vars.

        Args:
            sizes: Sizes of the new Dataset object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the Dataset class except for data vars.

        Returns:
            Dataset object without initializing data vars.

        """
        model = DataModel.from_dataclass(cls)
        data_vars: Dict[str, Any] = {}

        for data in model.data:
            shape = tuple(sizes[dim] for dim in data.type["dims"])
            data_vars[data.name] = np.empty(shape, order=order)

        return asdataset(cls(**data_vars, **kwargs))

    @classmethod
    def zeros(
        cls: Type[DatasetClass[P, TDataset]],
        sizes: Sizes,
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataset:
        """Create a Dataset object whose data vars are filled with zeros.

        Args:
            sizes: Sizes of the new Dataset object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the Dataset class except for data vars.

        Returns:
            Dataset object whose data vars are filled with zeros.

        """
        model = DataModel.from_dataclass(cls)
        data_vars: Dict[str, Any] = {}

        for data in model.data:
            shape = tuple(sizes[dim] for dim in data.type["dims"])
            data_vars[data.name] = np.zeros(shape, order=order)

        return asdataset(cls(**data_vars, **kwargs))

    @classmethod
    def ones(
        cls: Type[DatasetClass[P, TDataset]],
        sizes: Sizes,
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataset:
        """Create a Dataset object whose data vars are filled with ones.

        Args:
            sizes: Sizes of the new Dataset object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the Dataset class except for data vars.

        Returns:
            Dataset object whose data vars are filled with ones.

        """
        model = DataModel.from_dataclass(cls)
        data_vars: Dict[str, Any] = {}

        for data in model.data:
            shape = tuple(sizes[dim] for dim in data.type["dims"])
            data_vars[data.name] = np.ones(shape, order=order)

        return asdataset(cls(**data_vars, **kwargs))

    @classmethod
    def full(
        cls: Type[DatasetClass[P, TDataset]],
        sizes: Sizes,
        fill_value: Any,
        order: Order = "C",
        **kwargs: Any,
    ) -> TDataset:
        """Create a Dataset object whose data vars are filled with given value.

        Args:
            sizes: Sizes of the new Dataset object.
            fill_value: Value for data vars of the new Dataset object.
            order: Whether to store data in row-major (C-style)
                or column-major (Fortran-style) order in memory.
            kwargs: Args of the Dataset class except for data vars.

        Returns:
            Dataset object whose data vars are filled with given value.

        """
        model = DataModel.from_dataclass(cls)
        data_vars: Dict[str, Any] = {}

        for data in model.data:
            shape = tuple(sizes[dim] for dim in data.type["dims"])
            data_vars[data.name] = np.full(shape, fill_value, order=order)

        return asdataset(cls(**data_vars, **kwargs))
