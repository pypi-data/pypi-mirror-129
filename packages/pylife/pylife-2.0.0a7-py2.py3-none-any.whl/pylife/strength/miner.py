# Copyright (c) 2019-2021 - for information on the respective copyright owner
# see the NOTICE file and/or the repository
# https://github.com/boschresearch/pylife
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

Implementation of the miner rule for fatigue analysis
=====================================================

Currently, the following implementations are part of this module:

* Miner-elementar
* Miner-haibach

The source will be given in the function/class

References
----------
M. Wächter, C. Müller and A. Esderts, "Angewandter Festigkeitsnachweis nach {FKM}-Richtlinie"
Springer Fachmedien Wiesbaden 2017, https://doi.org/10.1007/978-3-658-17459-0

E. Haibach, "Betriebsfestigkeit", Springer-Verlag 2006, https://doi.org/10.1007/3-540-29364-7
"""

__author__ = "Cedric Philip Wagner"
__maintainer__ = "Johannes Mueller"


import numpy as np
import pandas as pd

from pylife.strength.helpers import solidity_haibach
import pylife.materialdata.woehler


def get_accumulated_from_relative_collective(collective):
    """Get collective with accumulated frequencies.

    This function can be used to transform a collective with
    relative frequencies.

    Parameters
    ----------
    collective : np.ndarray
        numpy array of shape (:, 2)
        where ":" depends on the number of classes defined
        for the rainflow counting
        * column: class values in ascending order
        * column: relative number of cycles for each load class
    """
    accumulated = np.stack([
        collective[:, 0],
        np.flipud(np.cumsum(np.flipud(collective[:, 1])))
    ], axis=1)
    return accumulated


class MinerBase:
    """Basic functions related to miner-rule (original)

    Definitions will be based on the given references.
    Therefore, the original names are used so that they can
    be looked up easily.

    Parameters
    ----------
    ND : float
        number of cycles of the fatigue strength of the S/N curve [number of cycles]
    k_1 : float
        slope of the S/N curve [unitless]
    SD : float
        fatigue strength of the S/N curve [MPa]
    """

    collective = None

    def __init__(self, ND, k_1, SD):
        self._woehler_curve = pd.Series({
            'k_1': k_1,
            'SD': SD,
            'ND': ND
        }).woehler

    def setup(self, collective):
        """Calculations independent from the instantation

        Use the setup for functions that might require information that was not
        yet available at runtime during instantation.

        Parameters
        ----------
        collective : np.ndarray
            numpy array of shape (:, 2)
            where ":" depends on the number of classes defined
            for the rainflow counting
            * column: class values in ascending order
            * column: accumulated number of cycles
            first entry is the total number of cycles
            then in a descending manner till the
            number of cycles of the highest stress class
        """
        self._parse_collective(collective)
        self.zeitfestigkeitsfaktor_collective = self.calc_zeitfestigkeitsfaktor(self.H0)

    def _parse_collective(self, collective):
        """Parse collective and structure frequently used features"""
        # first, only select values of the collective with number of cycles >0

        if isinstance(collective, pd.Series) \
                and isinstance(collective.index, pd.IntervalIndex):
            collective = self._transform_pylife_collective(collective)

        N_collective_accumulated = collective[:, 1]

        def get_relative_from_accumulated(accumulated):
            relative = np.append(
                np.abs(np.diff(accumulated)),
                # the last value has to be appended separately since
                # it is the only value that is not obtained as a difference
                accumulated[-1],
            )
            return relative

        hi = get_relative_from_accumulated(N_collective_accumulated)
        self.collective = collective[hi > 0]

        # normalize collective to S_a_max = 1
        self.collective = self.collective / np.array([self.collective[:, 0].max(), 1])

        # the first entry of 2nd column is the sum of all cycles
        self.H0 = self.collective[0, 1]

        self.S_collective = self.collective[:, 0]
        if not np.all(np.diff(self.S_collective) > 0):
            raise ValueError(
                "The load classes of the collective are not in ascending order: "
                "{}".format(self.S_collective)
            )
        self.N_collective_accumulated = self.collective[:, 1]
        # get the number of cycles for each class
        hi = get_relative_from_accumulated(self.N_collective_accumulated)
        self.N_collective_relative = hi
        self.collective_relative = np.stack((self.S_collective,
                                             self.N_collective_relative),
                                            axis=1)

    def _transform_pylife_collective(self, coll):
        """Adjust the mean stress corrected pylife collective for parsing

        Parameters
        ----------
        coll : pandas.Series
            mean stress transformed pylife collective
        index: pandas.IntervalIndex
        """
        load_classes = np.array(coll.index.mid)
        self._original_pylife_frequencies = coll.to_numpy()
        accumulated_frequencies = np.flip(
            np.cumsum(np.flip(self._original_pylife_frequencies))
        )

        return np.stack([load_classes, accumulated_frequencies], axis=1)

    def calc_zeitfestigkeitsfaktor(self, N):
        """Calculate "Zeitfestigkeitsfaktor" according to Waechter2017 (p. 96)"""
        return np.power(self._woehler_curve.ND/N, 1./self._woehler_curve.k_1)

    def calc_A(self, collective):
        """Compute multiple of the lifetime"""
        if collective is None:
            if self.collective is None:
                raise RuntimeError(
                    "The collective has not been specified either "
                    "as input parameter or as attribute during setup."
                )
        else:
            self._parse_collective(collective)

        if self.__class__.__name__ == "MinerBase":
            raise NotImplementedError(
                "Method should be used only by deriving classes."
            )

    def effective_damage_sum(self, A):
        """Compute 'effective damage sum' D_m

        Refers to the formula given in Waechter2017, p. 99

        Parameters
        ----------
        A : float or np.ndarray (with 1 element)
            the multiple of the lifetime
        """

        d_min = 0.3  # minimum as suggested by FKM
        d_max = 1.0

        d_m_no_limits = 2. / (A**(1./4.))
        d_m = min(
            max(d_min, d_m_no_limits),
            d_max
        )

        return d_m

    def N_predict(self, load_level, A=None):
        """The predicted lifetime according to damage sum of the collective

        Parameters
        ----------
        load_level : float
            the maximum (stress) amplitude of the collective
        A : float
            the lifetime multiple A
            BEWARE: this relation is only valid in a specific
            representation of the predicted (Miner) lifetime
            where the sn-curve is expressed via the point
            of the maximum amplitude of the collective:
            N_predicted = N(S = S_max) * A
        """
        n_woehler_load_level = self._woehler_curve.basquin_cycles(load_level)
        if A is None:
            A = self.calc_A(None)
        return n_woehler_load_level * A


class MinerElementar(MinerBase):
    """Implementation of Miner-elementar according to Waechter2017

    """
    # Solidity (Völligkeit) according to Haibach
    V_haibach = None
    # Solidity (Völligkeit) according to FKM guideline
    V_FKM = None

    def setup(self, collective):
        super().setup(collective)
        A = self.calc_A(self.collective)
        # at this point N_expected is equal to H0
        # i.e. the number of cycles for the collective (not N for sample failure)
        self.d_m_collective = self.effective_damage_sum(A)

    def calc_A(self, collective=None):
        """Compute the lifetime multiple according to miner-elementar

        Described in Waechter2017 as "Lebensdauervielfaches, A_ele".

        Parameters
        ----------
        collective : np.ndarray
            numpy array of shape (:, 2)
            where ":" depends on the number of classes defined
            for the rainflow counting
            * column: class values in ascending order
            * column: accumulated number of cycles
            first entry is the total number of cycles
            then in a descending manner till the
            number of cycles of the highest stress class
        """
        super().calc_A(collective)
        V = solidity_haibach(self.collective, self._woehler_curve.k_1)
        self.V_haibach = V
        self.V_FKM = V**(1/self._woehler_curve.k_1)
        A = 1. / V
        self.A = A

        return A


class MinerHaibach(MinerBase):
    """Miner-modified according to Haibach (2006)

    WARNING: Contrary to Miner-elementar, the lifetime multiple A
             is not constant but dependent on the evaluated load level!

    Parameters
    ----------
    see MinerBase

    Attributes
    ----------
    A : dict
        the multiple of the life time initiated as dict
        Since A is different for each load level, the
        load level is taken as dict key (values are rounded to 0 decimals)
    """

    def calc_A(self, load_level, collective=None, ignore_inf_rule=False):
        """Compute the lifetime multiple for Miner-modified according to Haibach

        Refer to Haibach (2006), p. 291 (3.21-61). The lifetime multiple can be
        expressed in respect to the maximum amplitude so that
        N_lifetime = N_Smax * A

        Parameters
        ----------
        load_level : float > 0
            load level in [MPa]
        collective : np.ndarray (optional)
            the collective can optionally be input to this function
            if it is not specified, then the attribute is used.
            If no collective exists as attribute (is set during setup)
            then an error is thrown
        ignore_inf_rule : boolean
            By default, the lifetime is returned as inf when the given load level
            is smaller than the lifetime (see Haibach eq. 3.2-62).
            This rule can be ignored if an estimate for the lifetime in the
            region below the fatigue strength is required for investigation.

        Returns
        -------
        A : float > 0
            lifetime multiple
            return value is 'inf' if load_level < SD
        """
        super().calc_A(collective)

        # this parameter makes each evaluation of A unique

        if load_level < self._woehler_curve.SD:
            return np.inf

        assert self.S_collective.max() == 1

        s_a = self.S_collective * load_level

        i_full_damage = (s_a >= self._woehler_curve.SD)
        i_reduced_damage = (s_a < self._woehler_curve.SD)

        x_D = self._woehler_curve.SD / s_a.max()

        s_full_damage = s_a[i_full_damage]
        s_reduced_damage = s_a[i_reduced_damage]

        n_full_damage = self.N_collective_relative[i_full_damage]
        n_reduced_damage = self.N_collective_relative[i_reduced_damage]

        # first expression of the summation term in the denominator
        sum_1 = np.dot(
            n_full_damage,
            ((s_full_damage / s_a.max())**self._woehler_curve.k_1),
        )
        sum_2 = (x_D**(1 - self._woehler_curve.k_1)) * np.dot(
            n_reduced_damage,
            ((s_reduced_damage / s_a.max())**(2 * self._woehler_curve.k_1 - 1))
        )

        A = self.H0 / (sum_1 + sum_2)

        return A

    def N_predict(self, load_level, A=None, ignore_inf_rule=False):
        """The predicted lifetime according to damage sum of the collective

        Parameters
        ----------
        load_level : float
            the maximum (stress) amplitude of the collective
        A : float
            the lifetime multiple A
            BEWARE: this relation is only valid in a specific
            representation of the predicted (Miner) lifetime
            where the sn-curve is expressed via the point
            of the maximum amplitude of the collective:
            N_predicted = N(S = S_max) * A
        """
        if A is None:
            A = self.calc_A(load_level, ignore_inf_rule=ignore_inf_rule)

        N_pred = super().N_predict(load_level, A)
        return N_pred
