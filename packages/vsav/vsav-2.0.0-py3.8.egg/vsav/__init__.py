""" Save, restore, and diff versions of files.
"""
import argparse
import glob
import os
import sys

__version__ = '2.0.0'


class VersionUtil:
    """
    version suffixes: .v.nnn
    """
    encoding = 'utf-8'

    @classmethod
    def diff(cls, fname, *diff_options):
        """ diff `fname` `*diff_options`
        """
        (specific, current) = cls.get_names(fname)
        if specific is None:
            return
        if not os.access(specific, os.R_OK):
            sys.stderr.write(f'cannot read {specific}\n')
            return
        os.system(f'diff {" ".join(diff_options)} {specific} {current}')

    @staticmethod
    def get_highest_version(fname):
        """
        return an int: the highest version of `fname`
        or -1 if no version is found.
        """
        highest_version = -1
        prefix = f'{fname}.v.'
        prefix_len = len(prefix)
        for fpath in glob.glob(f'{prefix}*'):
            suffix = fpath[prefix_len:]
            if suffix.isdigit() and len(suffix) >= 3:
                version = int(suffix)
                highest_version = max(version, highest_version)
        return highest_version

    @classmethod
    def get_names(cls, fname):
        """
        Returns tuple (specific, current)
        `specific` has a version suffix, `current` does not.
        `specific` is `None` when no backup version of `current` exists.
        """
        specific = fname
        flist = fname.split('.')
        if (len(flist) > 2
                and flist[-2] == 'v'
                and flist[-1].isdigit()
                and len(flist[-1]) >= 3):
            current = '.'.join(flist[0 : -2])
        else:
            current = fname
            version = cls.get_highest_version(fname)
            if version == -1:
                sys.stderr.write(f'cannot find backup version of {current}\n')
                specific = None
            else:
                specific = f'{fname}.v.{version:03d}'
        return (specific, current)

    @classmethod
    def restore(cls, fname):
        """
        Restore file from specific version or latest version.
        """
        (specific, current) = cls.get_names(fname)
        if specific is None:
            return
        if not os.access(specific, os.R_OK):
            sys.stderr.write(f'cannot read {specific}\n')
            return
        with open(specific, 'r', encoding=cls.encoding) as inf:
            with open(current, 'w', encoding=cls.encoding) as ouf:
                ouf.write(inf.read())
        os.utime(current, os.stat(specific)[7:9])
        sys.stderr.write(f'{current} restored from {specific}\n')

    @classmethod
    def save(cls, fname):
        """
        Save `fname` in highest version + 1.
        """
        if not os.access(fname, os.R_OK):
            sys.stderr.write(f'cannot read {fname}\n')
            return
        version = cls.get_highest_version(fname) + 1
        latest = f'{fname}.v.{version:03d}'
        with open(fname, 'r', encoding=cls.encoding) as inf:
            with open(latest, 'w', encoding=cls.encoding) as ouf:
                ouf.write(inf.read())
        os.utime(latest, os.stat(fname)[7:9])
        sys.stderr.write(f'{fname} saved in {latest}\n')


def vdif():
    """
    Compare highest version or specific version to current version.
    """
    parser = argparse.ArgumentParser(description=vdif.__doc__)
    parser.add_argument(
            'fname',
            help='The file (or file.v.nnn) to compare)')
    parser.add_argument(
            'diff_options',
            nargs='*',
            help='options for diff')
    args = parser.parse_args()
    VersionUtil.diff(args.fname, *args.diff_options)

def vres():
    """
    Restore current version from highest version or specific version.
    """
    parser = argparse.ArgumentParser(description=vres.__doc__)
    parser.add_argument(
            'fname',
            nargs='+',
            help='The file to restore.')
    args = parser.parse_args()
    for fname in args.fname:
        VersionUtil.restore(fname)

def vsav():
    """
    Save current version.
    """
    parser = argparse.ArgumentParser(description=vsav.__doc__)
    parser.add_argument(
            'fname',
            nargs='+',
            help='The file to save.')
    args = parser.parse_args()
    for fname in args.fname:
        VersionUtil.save(fname)
