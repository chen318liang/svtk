# SVTools

Utilities for manipulating structural variation calls.

## Installation

```
$ git clone https://github.com/talkowski-lab/svtools.git
$ cd svtools
$ pip install -e .
```

## Available commands

```
SVTools: Utilities for manipulating structural variation

usage: svtools [-h] <subcommand> [options]

[ Preprocessing ]
    standardize    Convert SV calls to a standardized format.
    rdtest2vcf     Convert an RdTest-formatted bed to a standardized VCF.

[ Algorithm integration ]
    vcfcluster     Cluster SV calls from a list of VCFs. (Generally PE/SR.)
    bedcluster     Cluster SV calls from a BED. (Generally depth.)

[ Statistics ]
    count-svtypes  Count instances of each svtype in each sample in a VCF

[ Read-depth analysis ]
    bincov         Calculate normalized genome-wide depth of coverage.
    rdtest*        Calculate comparative coverage statistics at CNV sites.

[ PE/SR analysis ]
    collect-pesr   Count clipped reads and extract discordant pairs genomewide.
    sr-test        Calculate enrichment of clipped reads at SV breakpoints.
    pe-test        Calculate enrichment of discordant pairs at SV breakpoints.

[ Variant analysis ]
    link-cpx       Resolve complex variants from VCF of breakpoints.
    annotate       Annotate genic effects and ovelrap with noncoding elements.

* Not yet implemented

optional arguments:
  -h, --help  show this help message and exit
```
