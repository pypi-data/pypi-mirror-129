"""Simple, fast, parallelizable and object-oriented
implementation of Echo State Networks [#]_ [#]_, using offline
learning methods.

References
----------

    .. [#] H. Jaeger, ‘The “echo state” approach to analysing
           and training recurrent neural networks – with an
           Erratum note’, p. 48.
    .. [#] M. Lukoševičius, ‘A Practical Guide to Applying Echo
           State Networks’, Jan. 2012, doi: 10.1007/978-3-642-35289-8_36.

"""
# @author: Xavier HINAUT
# xavier.hinaut@inria.fr
# Copyright Xavier Hinaut 2018
# We would like to thank Mantas Lukosevicius for his code that
# was used as inspiration for this code:
# # http://minds.jacobs-university.de/mantas/code
import time

from typing import Sequence, Callable
from multiprocessing import Manager

import numpy as np

from .utils.parallel import parallelize, get_joblib_backend
from .utils.validation import _check_values, check_input_lists
from .utils.types import Data, Activation
from .regression_models import RidgeRegression, SklearnLinearModel
from ._base import _ESNBase


def _get_offline_model(ridge: float = 0.0,
                       sklearn_model: Callable = None,
                       dtype: np.dtype = np.float64):
    if ridge > 0.0 and sklearn_model is not None:
        raise ValueError("Parameters 'ridge' and 'sklearn_model' can not be "
                         "defined at the same time.")
    elif sklearn_model is not None:
        return SklearnLinearModel(sklearn_model, dtype=dtype)
    else:
        return RidgeRegression(ridge, dtype=dtype)


class ESN(_ESNBase):
    """Base class of Echo State Networks.

    The :py:class:`reservoirpy.ESN` class is the angular stone of ReservoirPy
    offline learning methods using reservoir computing.
    Echo State Network allows one to:
        - quickly build ESNs, using the :py:mod:`reservoirpy.mat_gen` module
          to initialize weights,
        - train and test ESNs on the task of your choice,
        - use the trained ESNs on the task of your choice, either in
          predictive mode or generative mode.

    Parameters
    ----------
        lr: float
            Leaking rate

        W: np.ndarray
            Reservoir weights matrix

        Win: np.ndarray
            Input weights matrix

        input_bias: bool, optional
            If True, will add a constant bias
            to the input vector. By default, True.

        reg_model: Callable, optional
            A scikit-learn linear model function to use for
            regression. Should be None if ridge is used.

        ridge: float, optional
            Ridge regularization coefficient for Tikonov regression.
            Should be None if reg_model is used. By default, pseudo-inversion
            of internal states and teacher signals is used.

        Wfb: np.array, optional
            Feedback weights matrix.

        fbfunc: Callable, optional
            Feedback activation function.

        typefloat: numpy.dtype, optional

    Attributes
    ----------
        Wout: np.ndarray
            Readout matrix
        dim_out: int
            Output dimension
        dim_in: int
            Input dimension
        N: int
            Number of neuronal units

    See also
    --------
        reservoirpy.ESNOnline for ESN with online learning using FORCE.

    """
    def __init__(self,
                 lr: float,
                 W: np.ndarray,
                 Win: np.ndarray,
                 input_bias: bool = True,
                 reg_model: Callable = None,
                 ridge: float = 0.0,
                 Wfb: np.ndarray = None,
                 fbfunc: Callable = lambda x: x,
                 noise_in: float = 0.0,
                 noise_rc: float = 0.0,
                 noise_out: float = 0.0,
                 activation: Activation = np.tanh,
                 seed: int = None,
                 typefloat: np.dtype = np.float64):
        super(ESN, self).__init__(lr,
                                  W,
                                  Win,
                                  input_bias=input_bias,
                                  activation=activation,
                                  Wfb=Wfb,
                                  fbfunc=fbfunc,
                                  Wout=None,
                                  noise_in=noise_in,
                                  noise_rc=noise_rc,
                                  noise_out=noise_out,
                                  seed=seed,
                                  typefloat=typefloat)
        self.model = _get_offline_model(ridge, reg_model, dtype=typefloat)

    @property
    def ridge(self):
        return getattr(self.model, "ridge", None)

    @ridge.setter
    def ridge(self, value):
        if hasattr(self.model, "ridge"):
            self.model.ridge = value

    def fit_readout(self,
                    states: Data,
                    teachers: Data,
                    reg_model: Callable = None,
                    ridge: float = None,
                    force_pinv: bool = False,
                    verbose: bool = False) -> np.ndarray:
        """Compute a readout matrix by fitting the states computed by the ESN
        to the expected values, using the regression model defined
        in the ESN.

        Parameters
        ----------
            states: list of numpy.ndarray
                All states computed.

            teachers: list of numpy.ndarray
                All ground truth vectors.

            reg_model: scikit-learn regression model, optional
                A scikit-learn regression model to use for readout
                weights computation.

            ridge: float, optional
                Use Tikhonov regression for readout weights computation
                and set regularization parameter to the parameter value.

            force_pinv: bool, optional
                Overwrite all previous parameters and
                force computation of readout using pseudo-inversion.

            verbose: bool, optional

        Returns
        -------
            numpy.ndarray
                Readout matrix.
        """
        states, teachers = check_input_lists(states, self.N, teachers, self.dim_out)

        # switch the regression model used at instanciation if needed.
        # WARNING: this change won't be saved by the save function.
        if (ridge is not None) or (reg_model is not None):
            offline_model = _get_offline_model(ridge, reg_model, dtype=self.typefloat)
        elif force_pinv:
            offline_model = _get_offline_model(ridge=0.0)
        else:
            offline_model = self.model

        # check if network responses are valid
        _check_values(array_or_list=states, value=None)

        if verbose:
            tic = time.time()
            print("Linear regression...")

        self.Wout = offline_model.fit(X=states, Y=teachers)

        if verbose:
            toc = time.time()
            print(f"Linear regression done! (in {toc - tic} sec)")

        return self.Wout

    def train(self,
              inputs: Data,
              teachers: Data,
              wash_nr_time_step: int = 0,
              workers: int = -1,
              seed: int = None,
              verbose: bool = False,
              backend=None,
              use_memmap=None,
              return_states: bool = False) -> Sequence[np.ndarray]:
        """Train the ESN model on set of input sequences.

        Parameters
        ----------
            inputs: list of numpy.ndarray
                List of inputs.
                Note that it should always be a list of sequences, i.e. if
                only one sequence (array with rows representing time axis)
                of inputs is used, it should be alone in a list.
            teachers: list of numpy.ndarray
                List of ground truths.
                Note that is should always be a list of
                sequences of the same length than the `inputs`, i.e. if
                only one sequence of inputs is used, it should be alone in a
                list.
            wash_nr_time_step: int
                Number of states to considered as transient when training. Transient
                states will be discarded when computing readout matrix. By default,
                no states are removes.
            workers: int, optional
                If n >= 1, will enable parallelization of states computation with
                n threads/processes, if possible. If n = -1, will use all available
                resources for parallelization. By default, -1.
            return_states: bool, False by default
                If `True`, the function will return all the internal states computed
                during the training. Be warned that this may be too heavy for the
                memory of your computer.
            backend:
                kept for compatibility with previous versions.
            use_memmap:
                kept for compatibility with previous versions.
            verbose: bool, optional

        Returns
        -------
            list of numpy.ndarray
                All states computed, for all inputs.

        Note
        ----
            If only one input sequence is provided ("continuous time" inputs),
            workers should be 1, because parallelization is impossible. In other
            cases, if using large NumPy arrays during computation (which is often
            the case), prefer using `threading` backend to avoid huge overhead.
            Multiprocess is a good idea only in very specific cases, and this code
            is not (yet) well suited for this.
        """
        # autochecks of inputs and outputs
        inputs, teachers = check_input_lists(inputs, self.dim_in,
                                             teachers, self.dim_out)

        self._dim_out = teachers[0].shape[1]
        self.model.initialize(self.N, self.dim_out)

        lengths = [i.shape[0] for i in inputs]
        steps = sum(lengths)

        if verbose:
            print(f"Training on {len(inputs)} inputs ({steps} steps) "
                  f"-- wash: {wash_nr_time_step} steps")

        if workers > 1 and get_joblib_backend() != "sequential":
            lock = Manager().Lock()
        else:
            lock = None

        def train_fn(*, x, y, pbar):
            s = self._compute_states(x, y, seed=seed, pbar=pbar)

            # increment X.X^T and Y.X^T
            if lock is not None:
                with lock:
                    self.model.partial_fit(s[wash_nr_time_step:], y)
            else:
                self.model.partial_fit(s[wash_nr_time_step:], y)

            return s

        if isinstance(self.model, SklearnLinearModel):
            # Force the workers to return all reservoir states
            # to feed the scikit-learn estimator, as most of them do not
            # possess a partial_fit function
            return_states = True

        _, states = parallelize(self, train_fn, workers, lengths, return_states,
                                pbar_text="Train", verbose=verbose,
                                x=inputs, y=teachers)

        if isinstance(self.model, SklearnLinearModel):
            self.Wout = self.model.fit(states, teachers)
        else:
            self.Wout = self.model.fit()  # perform Y.X^T.(X.X^T + ridge)^-1

        return states
