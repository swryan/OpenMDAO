"""
Latin Hypercube generator for Analysis Driver.
"""
import numpy as np

import random

from ..analysis_generator import AnalysisGenerator

# please implement a latin hypercube design of experiments using a python generator

# GitHub Copilot
# Here is a Latin Hypercube Sampling (LHS) generator in Python that yields each sample (row)
# one by one, without building the full matrix in memory. This is the classic LHS variant,
# which is the only variant that can be efficiently generated row-by-row.
#
# This generator is memory efficient and suitable for large sample sizes.
# If you need a generator for the "centered" variant, let me know!

# Classic Latin Hypercube Sampling (LHS) generator
# This generator yields samples from a Latin Hypercube Sampling design.
# It generates samples in a way that ensures each factor is sampled uniformly
# across its range, while maintaining the LHS properties.

class LHSGenerator(AnalysisGenerator):
    """
    DOE case generator implementing the classic Latin Hypercube Sampling method.

    Parameters
    ----------
    var_dict : dict
        A dictionary whose keys are promoted paths of variables to be set, and whose
        values are the arguments to `set_val`.
    samples : int, optional
        The number of samples to generate for each factor (Defaults to n).
    criterion : str, optional
        Allowable values are "center" or "c", "maximin" or "m",
        "centermaximin" or "cm", and "correlation" or "corr". If no value
        given, the design is simply randomized.
    iterations : int, optional
        The number of iterations in the maximin and correlations algorithms
        (Defaults to 5).
    seed : int, optional
        Random seed to use if design is randomized. Defaults to None.

    Attributes
    ----------
    _samples : int
        The number of evenly spaced levels between each factor
        lower and upper bound.
    _criterion : str
        the pyDOE criterion to use.
    _iterations : int
        The number of iterations to use for maximin and correlations algorithms.
    _seed : int or None
        Random seed.
    """

    # supported pyDOE criterion names.
    _supported_criterion = [
        # "center", "c",
        # "maximin", "m",
        # "centermaximin", "cm",
        # "correlation", "corr",
        None
    ]

    def __init__(self, var_dict, samples=None, criterion=None, iterations=5, seed=None):
        """
        Initialize the LHSGenerator.

        See : https://pythonhosted.org/pyDOE/randomized.html
        """
        if criterion not in self._supported_criterion:
            raise ValueError("Invalid criterion '%s' specified for %s. "
                             "Must be one of %s." %
                             (criterion, self.__class__.__name__,
                              self._supported_criterion))

        print(f"{self.__class__.__name__}.__init__()")
        self._samples = samples
        self._criterion = criterion
        self._iterations = iterations
        self._seed = seed

        super().__init__(var_dict)

        # self._run_count = 0
        # self._var_dict = var_dict
        # self._iter = None

        print(f"{self.__class__.__name__} initialized with var_dict:", self._var_dict)
        # self.mysetup()
        # print(f"{self.__class__.__name__} called _setup()")

        # super().__init__(var_dict)

    def _setup(self):
        """
        Generate the DOE and instantiate the internal Iterator.
        """
        print(f"{self.__class__.__name__}._setup()", flush=True)

        # Initialize the random number generator
        if self._seed is not None:
            rng = np.random.default_rng(self._seed)
        else:
            rng = np.random.default_rng()

        factors = self._var_dict

        size = sum([_get_size(name, meta) for name, meta in factors.items()])

        samples = self._samples if self._samples is not None else size

        # Generate the intervals
        cut = np.linspace(0, 1, samples + 1)
        a = cut[:samples]
        b = cut[1 : samples + 1]

        # For each column, generate random points in intervals and permute
        columns = []
        for j in range(size):
            u = rng.random(samples)
            col = u * (b - a) + a
            order = rng.permutation(samples)
            columns.append(col[order])

        self.columns = columns


        print("-----------------------------", flush=True)
        from pprint import pprint
        pprint(columns)
        print("-----------------------------", flush=True)


        1/0

        self._iter = iter(range(samples))

        # # Yield each row as a 1D array
        # for i in range(samples):
        #     yield np.array([columns[j][i] for j in range(size)])

        super()._setup()

    def _get_sampled_vars(self):
        """
        Return the set of variable names whose value are provided by this generator.
        """
        return self._var_dict.keys()

    def __next__(self):
        """
        Provide a dictionary of the next point to be analyzed.

        The key of each entry is the promoted path of var whose values are to be set.
        The associated value is the values to set (required), units (options),
        and indices (optional).

        Raises
        ------
        StopIteration
            When all analysis var_dict have been exhausted.

        Returns
        -------
        dict
            A dictionary containing the promoted paths of variables to
            be set by the AnalysisDriver
        """
        # vals = next(self._iter)

        raise StopIteration



    # Example usage:
    # for row in lhs_generator(3, samples=5, random_state=42):
    #     print(row)














class ProhgressiveLHSGenerator(AnalysisGenerator):
    """
    DOE case generator implementing the Progressive Latin Hypercube Sampling method.

    Parameters
    ----------
    var_dict : dict
        A dictionary whose keys are promoted paths of variables to be set, and whose
        values are the arguments to `set_val`.
    samples : int, optional
        The number of samples to generate for each factor (Defaults to n).
    iterations : int, optional
        The number of iterations in the maximin and correlations algorithms (Defaults to 5).
    seed : int, optional
        Random seed to use if design is randomized. Defaults to None.
    """

    def __init__(self, var_dict, samples=None, iterations=5, seed=None):
        """
        Initialize the ProhgressiveLHSGenerator.
        """
        self._samples = samples
        self._iterations = iterations
        self._seed = seed

        super().__init__(var_dict)

    def generate_lhs_samples(self, num_samples, num_variables):
        samples = []
        for i in range(num_samples):
            sample = [(j + random.random()) / num_samples for j in range(num_variables)]
            random.shuffle(sample)
            samples.append(sample)
        return samples

    def progressive_lhs(self, num_samples, num_variables, num_iterations):
        samples = self.generate_lhs_samples(num_samples, num_variables)
        for _ in range(num_iterations - 1):
            new_samples = []
            num_new_samples = num_samples // (2 * (_ + 2))
            for i in range(num_new_samples):
                selected_samples = random.sample(samples, 2)
                new_sample = [(s1 + s2) / 2 for s1, s2 in zip(selected_samples[0], selected_samples[1])]
                new_samples.append(new_sample)
            samples += new_samples
        return samples[:num_samples]

    # # Example usage
    # num_samples = 10
    # num_variables = 3
    # num_iterations = 3
    # lhs_samples = progressive_lhs(num_samples, num_variables, num_iterations)
    # print(lhs_samples)


def _get_size(name, dct):
    """
    Get the size of a variable from its metadata dictionary.

    Parameters
    ----------
    name : str
        The name of the variable for which to determine the size.
    dct : dict
        Dictionary containing metadata for the variable, must include 'upper', and 'lower' keys.

    Returns
    -------
    int
        The size of the variable as determined from the lower and upper bounds of the range.
        Note that both 'lower' and 'upper' must be present in the dictionary and have the same size.

    Raises
    ------
    ValueError
        The size of the specified lower bound does not match the size of the upper bound.
    RuntimeError
        The required metadata was not found in the dictionary to determine the size.
    """
    try:
        lower_size = np.size(dct['lower'])
        upper_size = np.size(dct['upper'])
        if lower_size != upper_size:
            raise ValueError(f"Size mismatch for factor '{name}': 'lower' bound size "
                             f"({lower_size}) does not match 'upper' bound size ({upper_size}).")
        return lower_size
    except KeyError:
        raise RuntimeError(f"Unable to determine levels for factor '{name}'. "
                           "Factors dictionary must contain both 'lower' and 'upper' keys.")
