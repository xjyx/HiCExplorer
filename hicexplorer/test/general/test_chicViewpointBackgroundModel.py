import warnings
warnings.simplefilter(action="ignore", category=RuntimeWarning)
warnings.simplefilter(action="ignore", category=PendingDeprecationWarning)
import pytest
import os
from tempfile import NamedTemporaryFile
from sys import platform

import numpy as np
from hicexplorer import chicViewpointBackgroundModel

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data/cHi-C/")


def are_files_equal(file1, file2, delta=1, skip=0):

    lines_file1_dict = {}
    mismatches = 0
    matches = 0
    line_count_file1 = 0
    with open(file1, 'r') as textfile1:
        file_content = textfile1.readlines()

        for i, line in enumerate(file_content):
            if i < skip:
                continue
            lines_file1_dict[line] = True
            line_count_file1 += 1
    with open(file2, 'r') as textfile2:

        file_content = textfile2.readlines()
        for i, line in enumerate(file_content):
            if i < skip:
                continue
            if line in lines_file1_dict:
                matches += 1
            else:
                mismatches += 1
    if mismatches < delta and line_count_file1 - delta <= matches:
        return True
    else:
        return False


def test_compute_background():
    outfile = NamedTemporaryFile(suffix='.bed', delete=False)
    outfile.close()
    args = "--matrices {} {} --referencePoints {} -o {}".format(ROOT + 'FL-E13-5_chr1.cool', ROOT + 'MB-E10-5_chr1.cool',
                                                                ROOT + 'referencePoints.bed', outfile.name).split()
    chicViewpointBackgroundModel.main(args)
    if platform == 'darwin':
        length_background = 0
        length_background_outfile = 0

        with open(ROOT + 'background.bed') as textfile:
            file_content = textfile.readlines()
            length_background = len(file_content)
        with open(outfile.name) as textfile:
            file_content = textfile.readlines()
            length_background_outfile = len(file_content)

        assert np.abs(length_background - length_background_outfile) < 1
        # print('length_background {}'.format(length_background))
        # print('length_background_outfile {}'.format(length_background_outfile))
        # assert are_files_equal(ROOT + 'background.bed', outfile.name, delta=100, skip=0)
    else:
        assert are_files_equal(ROOT + 'background.bed', outfile.name, delta=1, skip=0)
