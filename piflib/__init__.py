import pkg_resources

from piflib.pif_calculator import compute_cigs, compute_weighted_cigs, compute_csfs

try:
    __version__ = pkg_resources.get_distribution('clkhash').version
except pkg_resources.DistributionNotFound:
    __version__ = "development"

__author__ = "Data61"
