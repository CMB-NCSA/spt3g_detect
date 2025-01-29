#!/usr/bin/env python
import spt3g_detect.dtools as du
import argparse
import time


def cmdline():

    parser = argparse.ArgumentParser(description="spt3g transient detection")
    parser.add_argument("files", nargs='+',
                        help="Filename(s) to ingest")
    parser.add_argument("--outdir", type=str, action='store', default=None,
                        required=True, help="Location for output files")
    parser.add_argument("--clobber", action='store_true', default=False,
                        help="Clobber output files")

    parser.add_argument("--field", type=str, action='store', default=None,
                        help="Field name (i.e. SourceName) for automatically determining point source file to use.")
    # Logging options (loglevel/log_format/log_format_date)
    default_log_format = '[%(asctime)s.%(msecs)03d][%(levelname)s][%(name)s][%(funcName)s] %(message)s'
    default_log_format_date = '%Y-%m-%d %H:%M:%S'
    parser.add_argument("--loglevel", action="store", default='INFO', type=str.upper,
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging Level [DEBUG/INFO/WARNING/ERROR/CRITICAL]")
    parser.add_argument("--log_format", action="store", type=str, default=default_log_format,
                        help="Format for logging")
    parser.add_argument("--log_format_date", action="store", type=str, default=default_log_format_date,
                        help="Format for date section of logging")

    # Detection options
    parser.add_argument("--rms2D", action='store_true', default=False,
                        help="Perform 2D map of the rms using photutils Background2D StdBackgroundRMS")
    parser.add_argument("--rms2D_box", action='store', type=int, default=60,
                        help="Size of box using photutils Background2D StdBackgroundRMS")
    parser.add_argument("--npixels", action='store', type=int, default=20,
                        help="Compress output files with astropy.io.fits.CompImageHDU")
    parser.add_argument("--nsigma_thresh", action='store', type=float, default=5.0,
                        help="Number of sigmas use to compute the detection threshold")
    parser.add_argument("--max_sep", action='store', type=float, default=35.0,
                        help="Maximum angular separation to match sources in arcsec")
    parser.add_argument("--plot", action='store_true', default=False,
                        help="Plot detection diagnostics?")

    # Use multiprocessing
    parser.add_argument("--np", action="store", default=1, type=int,
                        help="Run using multi-process, 0=automatic, 1=single-process [default]")
    parser.add_argument("--ntheads", action="store", default=1, type=int,
                        help="The number of threads used by numexpr 0=automatic, 1=single [default]")

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    # Keep time
    t0 = time.time()
    args = cmdline()
    d3w = du.detect_3gworker(**args.__dict__)
    t0 = time.time()
    d3w.run_detection_files()
    # d3w.run_detection_serial()
    # d3w.run_detection_mp()
    print(f"Total time: {du.elapsed_time(t0)} for [run_detection_files]")
    # Example 2, find repeating soueces
    table_centroids = du.find_repeating_sources(d3w.cat, separation=args.max_sep, plot=args.plot, outdir=args.outdir)
    stacked_centroids = du.find_unique_centroids(table_centroids, separation=args.max_sep, plot=args.plot)
    print("stacked_centroids:")
    print(stacked_centroids)
    print(f"Total time: {du.elapsed_time(t0)}")
