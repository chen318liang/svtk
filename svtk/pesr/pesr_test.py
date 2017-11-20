#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Matthew Stone <mstone5@mgh.harvard.edu>
# Distributed under terms of the MIT license.

"""

"""

import numpy as np
import scipy.stats as ss
import pandas as pd
import svtk.utils as svu


class PESRTest:
    def __init__(self):
        pass

    def test(self, counts, samples, background):
        """
        Test enrichment of clipped reads in a set of samples at a given coord.

        Arguments
        ---------
        chrom : str
        pos : int
        strand : str
        samples : list of str
            List of called samples to test
        background : list of str
            List of samples to use as background

        Returns
        -------
        called_median : float
        background_median : float
        log_pval : float
            Negative log10 p-value
        """

        # Restrict to called or background samples
        counts = counts.loc[counts['sample'].isin(samples + background)].copy()

        # Return null score if no eligible clipped reads present
        if counts.shape[0] == 0:
            return self.null_score()

        # Add called and background samples with no observed clipped reads
        counts = counts.set_index('sample')['count']\
                       .reindex(samples + background)\
                       .fillna(0).reset_index()

        # Label samples
        counts['is_called'] = counts['sample'].isin(samples)

        # Calculate enrichment
        result = counts.groupby('is_called')['count'].median()

        # Fill 0 if called in all samples
        result = result.reindex([True, False]).fillna(0)
        result.index = ['called', 'background']
        pval = ss.poisson.cdf(result.background, result.called)
        result['log_pval'] = np.abs(np.log10(pval))

        return result

    def null_score(self, null_val=0.0):
        """Null score if no clipped reads observed"""
        score = pd.Series([null_val] * 3,
                          ['background', 'called', 'log_pval']).rename('count')
        score.index.name = 'status'

        return score


class PESRTestRunner:
    def __init__(self, vcf, n_background=160, whitelist=None, blacklist=None):
        self.vcf = vcf

        self.samples = list(vcf.header.samples)
        self.n_background = n_background

        self.whitelist = whitelist if whitelist else self.samples
        self.blacklist = blacklist if blacklist else []

    def run(self):
        for record in self.vcf:
            self.test_record(record)

    def test_record(self, record):
        called, background = self.choose_background(record)

    def choose_background(self, record, whitelist=None, blacklist=None):
        # Select called and background samples
        called = svu.get_called_samples(record)
        background = [s for s in self.samples if s not in called]

        # Permit override of specified white/blacklists
        whitelist = whitelist if whitelist is not None else self.whitelist
        blacklist = blacklist if blacklist is not None else self.blacklist

        def _filter_whitelist(samples):
            return [s for s in samples if s in whitelist]

        def _filter_blacklist(samples):
            return [s for s in samples if s not in blacklist]

        called = _filter_whitelist(called)
        background = _filter_whitelist(background)

        called = _filter_blacklist(called)
        background = _filter_blacklist(background)

        if len(background) >= self.n_background:
            background = np.random.choice(background, self.n_background,
                                          replace=False).tolist()

        return called, background
