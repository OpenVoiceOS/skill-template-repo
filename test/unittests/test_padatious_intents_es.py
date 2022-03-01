# write your first unittest!
import unittest
from os.path import join, dirname
import os
from ovos_utils.bracket_expansion import expand_parentheses, expand_options


def read_samples(path):
    samples = []
    with open(path) as fi:
        for _ in fi.read().split("\n"):
            if _ and not _.strip().startswith("#"):
                samples += expand_options(_)
    return samples


class TestPadaos(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        from padaos import IntentContainer
        res_folder = join(dirname(dirname(dirname(__file__))), "locale", "es-es")
        engine = IntentContainer()
        for root, folders, files in os.walk(res_folder):
            for f in files:
                samples = read_samples(join(root, f))
                if f.endswith(".intent"):
                    engine.add_intent(f.replace(".intent", ""), samples)
                if f.endswith(".entity"):
                    engine.add_entity(f.replace(".entity", ""), samples)
        self.engine = engine
        self.res_folder = res_folder

    def test_padaos(self):
        for root, folders, files in os.walk(self.res_folder):
            for f in files:
                if f.endswith(".intent"):
                    samples = read_samples(join(root, f))
                    for s in samples:
                        self.assertEqual(self.engine.calc_intent(s),
                                         {'entities': {}, 'name': f.replace(".intent", "")})


class TestPadatious(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        from padatious import IntentContainer
        res_folder = join(dirname(dirname(dirname(__file__))), "locale", "es-es")
        engine = IntentContainer(cache_dir="/tmp/padatious_cache")
        for root, folders, files in os.walk(res_folder):
            for f in files:
                samples = read_samples(join(root, f))
                if f.endswith(".intent"):
                    engine.add_intent(f.replace(".intent", ""), samples)
                if f.endswith(".entity"):
                    engine.add_entity(f.replace(".entity", ""), samples)
        engine.train(force=True)
        self.engine = engine
        self.res_folder = res_folder

    def test_padatious(self):
        for root, folders, files in os.walk(self.res_folder):
            for f in files:
                if f.endswith(".intent"):
                    samples = read_samples(join(root, f))
                    for s in samples:
                        self.assertEqual(self.engine.calc_intent(s).name,
                                         f.replace(".intent", ""))

