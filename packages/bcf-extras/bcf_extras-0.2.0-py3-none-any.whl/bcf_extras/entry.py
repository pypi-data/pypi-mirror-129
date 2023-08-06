#!/usr/bin/env python

# bcf_extras is a set of variant file helper utilities built on top of bcftools and htslib.
# Copyright (C) 2021  David Lougheed
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import sys

from typing import List, Optional

from .add_header_lines import add_header_lines
from .copy_compress_index import copy_compress_index
from .parallel_mergestr import parallel_mergestr
from .filter_gff3 import filter_gff3

__all__ = [
    "main",
]


ACTION_ADD_HEADER_LINES = "add-header-lines"
ACTION_ARG_JOIN = "arg-join"
ACTION_COPY_COMPRESS_INDEX = "copy-compress-index"
ACTION_PARALLEL_MERGESTR = "parallel-mergeSTR"
ACTION_FILTER_GFF3 = "filter-gff3"
ACTION_REFORMAT_VCF_CONTIGS = "reformat-vcf-contigs"


def _add_cci_parser(subparsers):
    cci_parser = subparsers.add_parser(
        ACTION_COPY_COMPRESS_INDEX,
        help="Compresses a VCF to a bgzipped copy with a tabix index, leaving the original intact.")
    cci_parser.add_argument("vcfs", nargs="+", type=str, help="The VCF(s) to process.")


def _add_ahl_parser(subparsers):
    ahl_parser = subparsers.add_parser(
        ACTION_ADD_HEADER_LINES,
        help="Inserts new VCF header lines from stdin to either the end of the header (default) or to a specified "
             "position in a VCF file, in-place. Ignores the first and last header lines (fileformat/#CHROM.)")
    ahl_parser.add_argument("vcf", type=str, help="The VCF to process.")
    ahl_parser.add_argument("lines", type=str, help="The text file with header lines to insert.")
    ahl_parser.add_argument(
        "--tmp-dir",
        type=str,
        default=None,
        help="Temporary directory path for VCF header artifacts.")
    ahl_parser.add_argument(
        "--start",
        type=int,
        default=None,
        help="0-indexed offset from the start of the header, excluding fileformat line (e.g. --start 0 will insert "
             "right after ##fileformat.)")
    ahl_parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="0-indexed offset from the start of the header, excluding #CHROM line (e.g. --end 0 will insert "
             "right before #CHROM.)")
    ahl_parser.add_argument(
        "--delete-old",
        action="store_true",
        help="Whether to delete the original file instead of keeping it (as {filename}.old) post-header-change. "
             "Off by default.")


def _add_aj_parser(subparsers):
    aj_parser = subparsers.add_parser(
        ACTION_ARG_JOIN,
        help="Joins arguments by a specified string, for pipelining into other utilities.")
    aj_parser.add_argument("--sep", type=str, default=",", help="The string to join arguments by.")
    aj_parser.add_argument("args", nargs="*", help="Arguments to join together.")


def _add_pms_parser(subparsers):
    pms_parser = subparsers.add_parser(
        ACTION_PARALLEL_MERGESTR,
        help="Runs the TRTools mergeSTR command in parallel, with a specified number of processes.")
    pms_parser.add_argument("--out", type=str, required=True, help="Output VCF name for final merge result.")
    pms_parser.add_argument(
        "--vcftype",
        type=str,
        default="auto",
        help="The type of VCFs being processed (see mergeSTR docs for more info.)")
    pms_parser.add_argument("--ntasks", type=int, default=2, help="The number of processes to use.")
    pms_parser.add_argument("--step1-only", action="store_true", help="Whether to only run the first step.")
    pms_parser.add_argument("--step2-only", action="store_true", help="Whether to only run the second step.")
    pms_parser.add_argument("vcfs", nargs="+", type=str, help="The VCF(s) to merge.")


def _add_fg3_parser(subparsers):
    fg3_parser = subparsers.add_parser(
        ACTION_FILTER_GFF3,
        help="Filters by column on a GFF3 input file (from stdin) based on provided regular expressions.")
    fg3_parser.add_argument("--seqid", type=str, help="seqid filter")
    fg3_parser.add_argument("--source", type=str, help="source filter")
    fg3_parser.add_argument("--type", type=str, help="type filter")
    fg3_parser.add_argument("--strand", type=str, help="strand filter")
    fg3_parser.add_argument("--phase", type=str, help="phase filter")
    fg3_parser.add_argument("--no-body-comments", action="store_true",
                            help="Whether to remove comments that are interspersed with records.")
    fg3_parser.add_argument("file", type=str, help="GFF3 file path to process.")


def _add_rvc_parser(subparsers):
    rvc_parser = subparsers.add_parser(
        ACTION_REFORMAT_VCF_CONTIGS,
        help="Standardizes common VCF contig names (either removes or adds chr prefix.)")
    rvc_parser.add_argument("--with-chr", action="store_true", help="Whether to include or remove the chr prefix.")
    rvc_parser.add_argument("vcfs", nargs="+", type=str, help="The VCF(s) to reformat.")


def main(args: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        description="A set of variant file helper utilities built on top of bcftools and htslib.")
    subparsers = parser.add_subparsers(
        dest="action",
        title="action",
        help="The action to run. Each action has its own set of arguments.",
        required=True)

    _add_cci_parser(subparsers)
    _add_ahl_parser(subparsers)
    _add_aj_parser(subparsers)
    _add_pms_parser(subparsers)
    _add_fg3_parser(subparsers)

    p_args = parser.parse_args(args or sys.argv[1:])

    # TODO: py3.10: match
    if p_args.action == ACTION_COPY_COMPRESS_INDEX:
        copy_compress_index(p_args.vcfs)
    elif p_args.action == ACTION_ADD_HEADER_LINES:
        add_header_lines(p_args.vcf, p_args.lines, p_args.start, p_args.end, p_args.delete_old)
    elif p_args.action == ACTION_ARG_JOIN:
        print(p_args.sep.join(p_args.args), end="")
    elif p_args.action == ACTION_PARALLEL_MERGESTR:
        # leave intermediate_prefix default
        parallel_mergestr(
            p_args.vcfs,
            p_args.out,
            p_args.vcftype,
            p_args.ntasks,
            p_args.step1_only,
            p_args.step2_only,
        )
    elif p_args.action == ACTION_FILTER_GFF3:
        filter_gff3(
            p_args.file,
            getattr(p_args, "seqid", None),
            getattr(p_args, "source", None),
            getattr(p_args, "type", None),
            getattr(p_args, "strand", None),
            getattr(p_args, "phase", None),
            no_body_comments=p_args.no_body_comments,
        )
    elif p_args.action == ACTION_REFORMAT_VCF_CONTIGS:
        pass  # TODO


if __name__ == "__main__":
    main(sys.argv[1:])
