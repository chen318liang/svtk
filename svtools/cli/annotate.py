#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Matthew Stone <mstone5@mgh.harvard.edu>
# Distributed under terms of the MIT license.

"""
Annotate resolved SV with genic effects and noncoding hits.

The following classes of genic effects are annotated if the SV meets the
defined criteria:
    1) LOF - Loss of function.
        * Deletions are annotated LOF if they overlap any exon.
        * Duplications are annotated LOF if they reside entirely within
        a gene boundary and overlap any exon.
        * Inversions are annotated LOF if reside entirely within an exon, if
        one breakpoint falls within an exon, if they reside entirely within a
        gene boundary and overlap an exon, or if only one breakpoint falls
        within a gene boundary.
        * Translocations are annotated LOF If they fall within a gene boundary.
    2) COPY_GAIN
        * Duplications are annotated COPY_GAIN if they span the entirety of a
        gene boundary.
    3) INTRONIC
        * Deletions, duplications, and inversions are annotated INTRONIC if
        they are localized to an intron.
    4) DUP_PARTIAL
        * Duplications are annotated DUP_PARTIAL if they overlap the start or
        end of a gene boundary but not its entirety, such that a whole copy of
        the gene is preserved.
    5) INV_SPAN
        * Inversions are annotated INV_SPAN if they overlap the entirety of a
        gene boundary without disrupting it.
    6) NEAREST_TSS
        * Intragenic events are annotated with the nearest transcription start
        site.
"""

import argparse
import sys
import pysam
import pybedtools as pbt
import svtools.annotation as anno


def main(argv):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('vcf', help='Structural variants.')
    parser.add_argument('--gencode', help='Gencode gene annotations (GTF).')
    parser.add_argument('--noncoding', help='Noncoding elements (bed). '
                        'Columns = chr,start,end,element_class,element_name')
    parser.add_argument('annotated_vcf', help='Annotated variants.')

    # Print help if no arguments specified
    if len(argv) == 0:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args(argv)

    if args.gencode is None and args.noncoding is None:
        sys.stderr.write('ERROR: Neither Gencode annotations nor noncoding '
                         'elements provided. Must specify at least one to '
                         'annotate.\n\n')
        parser.print_help()
        sys.exit(1)

    vcf = pysam.VariantFile(args.vcf)

    if args.gencode is not None:
        gencode = pbt.BedTool(args.gencode)
    else:
        gencode = None
    if args.noncoding is not None:
        noncoding = pbt.BedTool(args.noncoding)
    else:
        noncoding = None

    anno.annotate_vcf(vcf, gencode, noncoding, args.annotated_vcf)


if __name__ == '__main__':
    main(sys.argv[1:])
