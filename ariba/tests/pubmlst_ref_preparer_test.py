import unittest
import os
import filecmp
import shutil
import pyfastaq
from ariba import mlst_profile, pubmlst_ref_preparer

modules_dir = os.path.dirname(os.path.abspath(pubmlst_ref_preparer.__file__))
data_dir = os.path.join(modules_dir, 'tests', 'data')


class TestPubmlstRefPreparer(unittest.TestCase):
    def test_load_fasta_files_and_write_clusters_file(self):
        '''test _load_fasta_files_and_write_clusters_file'''
        indir = os.path.join(data_dir, 'pubmlst_ref_prepare.test_load_fa_and_clusters.in')
        outdir = 'tmp.test.pubmlst_ref_prepare.test_load_fa_and_clusters'
        os.mkdir(outdir)
        r_prep = pubmlst_ref_preparer.PubmlstRefPreparer('species', outdir)
        profile_file = os.path.join(indir, 'profile.txt')
        r_prep.profile = mlst_profile.MlstProfile(profile_file)
        r_prep._load_fasta_files_and_write_clusters_file(indir)
        expected_cluster_tsv = os.path.join(data_dir, 'pubmlst_ref_prepare.test_load_fa_and_clusters.expect.tsv')
        self.assertTrue(filecmp.cmp(expected_cluster_tsv, r_prep.clusters_file, shallow=False))
        shutil.rmtree(outdir)

        expected_fasta_files = [os.path.join(indir, x) for x in ['gene1.tfa', 'gene2.tfa']]
        self.assertEqual(expected_fasta_files, r_prep.fasta_files)

        expected_seqs = {
            'gene1': {
                'gene1_1': pyfastaq.sequences.Fasta('gene1_1', 'ACGT'),
                'gene1_2': pyfastaq.sequences.Fasta('gene1_2', 'AAAA'),
            },
            'gene2': {
                'gene2_1': pyfastaq.sequences.Fasta('gene2_1', 'GGGG'),
                'gene2_2': pyfastaq.sequences.Fasta('gene2_2', 'TTTT'),
            },
        }
        self.assertEqual(expected_seqs, r_prep.sequences)

