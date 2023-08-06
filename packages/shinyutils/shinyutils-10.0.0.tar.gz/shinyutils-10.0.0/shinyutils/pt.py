"""Utilities for pytorch."""

try:
    import torch
except ImportError:
    raise ImportError("shinyutils.pt needs `pytorch`") from None

import inspect
import logging
from argparse import _ArgumentGroup, Action, ArgumentParser, ArgumentTypeError
from typing import (
    Annotated,
    Callable,
    Iterable,
    Optional,
    overload,
    Sequence,
    Tuple,
    TYPE_CHECKING,
    Union,
)
from unittest.mock import Mock

import torch.nn.functional as F
from corgy import Corgy, corgyparser
from corgy.types import KeyValueType, SubClassType
from torch import nn
from torch.optim import Adam
from torch.optim.lr_scheduler import _LRScheduler
from torch.optim.optimizer import Optimizer
from torch.utils.data import DataLoader, Dataset, TensorDataset

try:
    from tqdm import trange
except ImportError:
    logging.info("progress bar disabled: could not import `tqdm`")

    def trange(n, *args, **kwargs):
        return range(n)


if TYPE_CHECKING:
    import numpy as np

__all__ = ("DEFAULT_DEVICE", "PTOpt", "FCNet", "NNTrainer", "TBLogs")

DEFAULT_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class PTOpt(Corgy):
    """Wrapper around PyTorch optimizer and learning rate scheduler.

    Usage::

        >>> opt = PTOpt(Adam, {"lr": 0.001})
        >>> net = nn.Module(...)  # some network
        >>> opt.set_weights(net.parameters())
        >>> opt.zero_grad()
        >>> opt.step()
    """

    def _t_param(s: str) -> Union[int, float, str]:  # pylint: disable=no-self-argument
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                pass
        return s

    _OptimizerSubClassType = SubClassType(Optimizer)
    _LRSchedulerSubClassType = SubClassType(_LRScheduler)
    _KVType = KeyValueType(str, _t_param)
    __slots__ = (
        "optimizer",
        "lr_scheduler",
        "_optim_params_dict",
        "_lr_sched_params_dict",
    )

    _OptimizerSubClassType.__choices__ = [
        _c
        for _c in _OptimizerSubClassType.__choices__
        if _c.__module__ != "torch.optim._multi_tensor"
    ]

    optim_cls: Annotated[  # type: ignore
        _OptimizerSubClassType, "optimizer class"
    ] = Adam
    optim_params: Annotated[  # type: ignore
        Sequence[_KVType], "arguments for the optimizer"
    ] = []
    lr_sched_cls: Annotated[  # type: ignore
        Optional[_LRSchedulerSubClassType], "learning rate scheduler class"
    ] = None
    lr_sched_params: Annotated[  # type: ignore
        Sequence[_KVType], "arguments for the learning rate scheduler"
    ] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.optimizer = None
        self.lr_scheduler = None
        self._optim_params_dict = dict(self.optim_params)
        self._lr_sched_params_dict = dict(self.lr_sched_params)

    def set_weights(self, weights: Iterable[torch.Tensor]):
        """Set weights of underlying optimizer."""
        self.optimizer = self.optim_cls(  # type: ignore
            weights, **self._optim_params_dict
        )
        if self.lr_sched_cls is not None:
            self.lr_scheduler = (
                self.lr_sched_cls(  # type: ignore  # pylint: disable=not-callable
                    self.optimizer, **self._lr_sched_params_dict
                )
            )

    @staticmethod
    def _better_lr_sched_repr(lr_sched: _LRScheduler) -> str:
        return (
            lr_sched.__class__.__name__
            + "(\n    "
            + "\n    ".join(
                f"{k}: {v}"
                for k, v in lr_sched.state_dict().items()
                if not k.startswith("_")
            )
            + "\n)"
        )

    def __repr__(self) -> str:
        if self.optimizer is None:
            return super().__repr__()
        r = repr(self.optimizer)
        if self.lr_scheduler is not None:  # type: ignore
            r += f"\n{self._better_lr_sched_repr(self.lr_scheduler)}"  # type: ignore
        return r

    def _ensure_initialized(self):
        if self.optimizer is None:
            raise TypeError("no weights set: call `PTOpt.set_weights` first")

    def zero_grad(self):
        """Call `zero_grad` on underlying optimizer."""
        self._ensure_initialized()
        self.optimizer.zero_grad()

    def step(self):
        """Call `step` on underlying optimizer, and lr scheduler (if present)."""
        self._ensure_initialized()
        self.optimizer.step()
        if self.lr_scheduler is not None:
            self.lr_scheduler.step()

    @staticmethod
    def add_help_args_to_parser(
        base_parser: Union[ArgumentParser, _ArgumentGroup],
        group_title: Optional[str] = "pytorch help",
    ):
        """Add parser arguments for help on PyTorch optimizers and lr schedulers.

        Example::

            >>> arg_parser = ArgumentParser(
                    add_help=False, formatter_class=corgy.CorgyHelpFormatter
            )
            >>> PTOpt.add_help(arg_parser)
            >>> arg_parser.print_help()
            pytorch help:
              --explain-optimizer cls  describe arguments of a torch optimizer
                                       (optional)
              --explain-lr-sched cls   describe arguments of a torch lr scheduler
                                       (optional)
            >>> arg_parser.parse_args(["--explain-optimizer", "Adamax"])
            Adamax(params, lr=0.002, betas=(0.9, 0.999), eps=1e-08, weight_decay=0)
        """

        class _ShowHelp(Action):
            def __call__(self, parser, namespace, values, option_string=None):
                cls_name = values.__name__
                cls_sig = inspect.signature(values)
                cls_doc = inspect.getdoc(values)
                print(f"{cls_name}{cls_sig}\n\n{cls_doc}")
                parser.exit()

        if group_title is not None:
            base_parser = base_parser.add_argument_group(group_title)

        base_parser.add_argument(
            "--explain-optimizer",
            type=PTOpt._OptimizerSubClassType,
            action=_ShowHelp,
            help="describe arguments of a torch optimizer",
            choices=PTOpt._OptimizerSubClassType.__choices__,
        )
        base_parser.add_argument(
            "--explain-lr-sched",
            type=PTOpt._LRSchedulerSubClassType,
            action=_ShowHelp,
            help="describe arguments of a torch lr scheduler",
            choices=PTOpt._LRSchedulerSubClassType.__choices__,
        )


class FCNet(Corgy, nn.Module):
    """Fully connected network."""

    _ActType = Callable[..., torch.Tensor]
    _ActType.__metavar__ = "fun"  # type: ignore

    __slots__ = ("__dict__",)

    in_dim: Annotated[int, "number of input features"]
    out_dim: Annotated[int, "number of output features"]
    hidden_dims: Annotated[Sequence[int], "hidden layer dimensions"]
    hidden_act: Annotated[_ActType, "activation function for hidden layers"] = F.relu
    out_act: Annotated[
        Optional[_ActType], "activation function for output layer"
    ] = None

    @corgyparser("hidden_act")
    @corgyparser("out_act")
    @staticmethod
    def _activation_function(s: str) -> _ActType:
        try:
            return getattr(F, s)
        except AttributeError:
            raise ArgumentTypeError(
                f"`torch.nn.functional` has no attribute `{s}`"
            ) from None

    def __init__(self, *args, **kwargs):
        nn.Module.__init__(self)
        Corgy.__init__(self, *args, **kwargs)
        layer_sizes = [self.in_dim] + self.hidden_dims + [self.out_dim]
        self.layers = nn.ModuleList(
            [nn.Linear(ls, ls_n) for ls, ls_n in zip(layer_sizes, layer_sizes[1:])]
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward a tensor through the network, and return the result.

        Args:
            x: Input tensor of shape `(batch_size, in_dim)`.
        """
        for layer in self.layers[:-1]:
            x = self.hidden_act(layer(x))
        x = self.layers[-1](x)
        if self.out_act is not None:
            x = self.out_act(x)  # pylint: disable=not-callable
        return x


class NNTrainer(Corgy):
    """Helper class for training a model on a dataset."""

    __slots__ = ("_dataset", "_data_loader")

    train_iters: Annotated[int, "number of training iterations"]
    ptopt: Annotated[PTOpt, "optimizer"]
    batch_size: Annotated[int, "batch size for training"] = 8
    data_load_workers: Annotated[int, "number of workers for loading data"] = 0
    shuffle: Annotated[bool, "whether to shuffle the dataset"] = True
    pin_memory: Annotated[bool, "whether to pin data to CUDA memory"] = True
    drop_last: Annotated[bool, "whether to drop the last incomplete batch"] = True
    pbar_desc: Annotated[str, "description for training progress bar"] = "Training"

    @overload
    def set_dataset(self, value: Dataset):
        ...

    @overload
    def set_dataset(self, value: Tuple[torch.Tensor, ...]):
        ...

    @overload
    def set_dataset(self, value: Tuple["np.ndarray", ...]):
        ...

    def set_dataset(self, value):
        """Set the training data.

        Args:
            value: `torch.utils.data.Dataset` instance, or tuple of `torch.Tensor` or
                `np.ndarray` objects.
        """
        if isinstance(value, Dataset):
            self._dataset = value
        elif isinstance(value, tuple):
            if not isinstance(value[0], torch.Tensor):
                value = [torch.from_numpy(val_i) for val_i in value]
            self._dataset = TensorDataset(*value)
        else:
            raise ValueError(f"can't set dataset from type `{type(value)}`")

        self._data_loader = DataLoader(
            self._dataset,
            batch_size=self.batch_size,
            num_workers=self.data_load_workers,
            shuffle=self.shuffle,
            pin_memory=self.pin_memory,
            drop_last=self.drop_last,
        )

    def train(
        self,
        model: nn.Module,
        loss_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
        post_iter_hook: Optional[
            Callable[
                [int, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor], None
            ]
        ] = None,
    ):
        """Train a model.

        Args:
            model: Model (`nn.Module` instance) to train.
            loss_fn: Loss function mapping input tensors to a loss tensor.
            post_iter_hook: Optional callback function to call after each iteration.
                The function will be called with arguments
                `(iteration, x_batch, y_batch, yhat_batch, loss)`.
        """
        if self._dataset is None:
            raise RuntimeError("dataset not set: call `set_dataset` before `train`")
        bat_iter = iter(self._data_loader)

        logging.info("moving model to %s", DEFAULT_DEVICE)
        model = model.to(DEFAULT_DEVICE)

        logging.info("setting optimizer weights")
        self.ptopt.set_weights(model.parameters())

        with trange(self.train_iters, desc=self.pbar_desc) as pbar:
            for _iter in pbar:
                try:
                    x_bat, y_bat = next(bat_iter)
                except StopIteration:
                    bat_iter = iter(self._data_loader)
                    x_bat, y_bat = next(bat_iter)
                x_bat, y_bat = x_bat.to(DEFAULT_DEVICE), y_bat.to(DEFAULT_DEVICE)

                yhat_bat = model(x_bat)
                loss = loss_fn(yhat_bat, y_bat)
                pbar.set_postfix(loss=float(loss))

                self.ptopt.zero_grad()
                loss.backward()
                self.ptopt.step()

                if post_iter_hook is not None:
                    post_iter_hook(_iter, x_bat, y_bat, yhat_bat, loss)


class TBLogs:
    """TensorBoard logs type.

    Args:
        path: Path to log directory. If `None` (default), a mock instance is
            returned.

    Usage::

        tb_logs = TBLogs("tmp/tb")
        tb_logs.writer  # `SummaryWriter` instance
        TBLogs.mock  # mock instance
    """

    __metavar__ = "dir"
    _mock = None

    def __init__(self, path: Optional[str] = None):
        if path is not None:
            try:
                from torch.utils.tensorboard import SummaryWriter
            except ImportError:
                raise RuntimeError("tensorboard not installed") from None
            self.writer = SummaryWriter(path)
        else:
            self.writer = Mock()

    @classmethod
    @property
    def mock(cls):
        """Mock instace that no-ops for every call."""
        if cls._mock is None:
            cls._mock = cls()
        return cls._mock

    def __repr__(self) -> str:
        if isinstance(self.writer, Mock):
            return "<TBLogs object with mock writer>"
        return f"<TBLogs object with writer logging to '{self.writer.log_dir}'>"
