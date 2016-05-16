import unittest

from conda.resolve import MatchSpec

from conda_build.metadata import select_lines, handle_config_version


def test_select_lines():
    lines = """
test
test keep-if-true, omit-if-false [abc]
test keep-if-true, omit-if-false # [abc]
test [abc] trailing text hides selector
test foo[:-2] # other brackets are allowed
test foo[:-2] # other brackets are allowed [abc]
"""

    assert select_lines(lines, {'abc': True}) == """
test
test keep-if-true, omit-if-false 
test keep-if-true, omit-if-false # 
test [abc] trailing text hides selector
test foo[:-2] # other brackets are allowed
test foo[:-2] # other brackets are allowed 
"""
    assert select_lines(lines, {'abc': False}) == """
test
test [abc] trailing text hides selector
test foo[:-2] # other brackets are allowed
"""


class HandleConfigVersionTests(unittest.TestCase):

    def test_python(self):
        for spec, ver, res_spec in [
                ('python', '3.4', 'python 3.4*'),
                ('python 2.7.8', '2.7', 'python 2.7.8'),
                ('python 2.7.8', '3.5', 'python 2.7.8'),
                ('python 2.7.8', None, 'python 2.7.8'),
                ('python', None, 'python'),
                ('python x.x', '2.7', 'python 2.7*'),
                ('python', '27', 'python 2.7*'),
                ('python', 27, 'python 2.7*'),
        ]:
            ms = MatchSpec(spec)
            self.assertEqual(handle_config_version(ms, ver),
                             MatchSpec(res_spec))

        self.assertRaises(RuntimeError,
                          handle_config_version,
                          MatchSpec('python x.x'), None)

    def test_numpy(self):
        for spec, ver, res_spec in [
                ('numpy', None, 'numpy'),
                ('numpy', 18, 'numpy'),
                ('numpy', 110, 'numpy'),
                ('numpy x.x', 17, 'numpy 1.7*'),
                ('numpy x.x', 110, 'numpy 1.10*'),
                ('numpy 1.9.1', 18, 'numpy 1.9.1'),
                ('numpy 1.9.0 py27_2', None, 'numpy 1.9.0 py27_2'),
        ]:
            ms = MatchSpec(spec)
            self.assertEqual(handle_config_version(ms, ver),
                             MatchSpec(res_spec))

        self.assertRaises(RuntimeError,
                          handle_config_version,
                          MatchSpec('numpy x.x'), None)

