# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Tests that our test infrastructure is really working!"""

import datetime
import os
import re
import sys
import warnings

import pytest

import coverage
from coverage import tomlconfig
from coverage.exceptions import CoverageWarning
from coverage.files import actual_path

from tests.coveragetest import CoverageTest
from tests.helpers import (
    arcs_to_arcz_repr, arcz_to_arcs, assert_count_equal, assert_coverage_warnings,
    CheckUniqueFilenames, re_lines, re_lines_text, re_line, without_module,
)


def test_xdist_sys_path_nuttiness_is_fixed():
    # See conftest.py:fix_xdist_sys_path
    assert sys.path[1] != ''
    assert os.environ.get('PYTHONPATH') is None


def test_assert_count_equal():
    assert_count_equal(set(), set())
    assert_count_equal({"a": 1, "b": 2}, ["b", "a"])
    with pytest.raises(AssertionError):
        assert_count_equal({1,2,3}, set())
    with pytest.raises(AssertionError):
        assert_count_equal({1,2,3}, {4,5,6})


class CoverageTestTest(CoverageTest):
    """Test the methods in `CoverageTest`."""

    def test_file_exists(self):
        self.make_file("whoville.txt", "We are here!")
        self.assert_exists("whoville.txt")
        self.assert_doesnt_exist("shadow.txt")
        msg = "File 'whoville.txt' shouldn't exist"
        with pytest.raises(AssertionError, match=msg):
            self.assert_doesnt_exist("whoville.txt")
        msg = "File 'shadow.txt' should exist"
        with pytest.raises(AssertionError, match=msg):
            self.assert_exists("shadow.txt")

    def test_file_count(self):
        self.make_file("abcde.txt", "abcde")
        self.make_file("axczz.txt", "axczz")
        self.make_file("afile.txt", "afile")
        self.assert_file_count("a*.txt", 3)
        self.assert_file_count("*c*.txt", 2)
        self.assert_file_count("afile.*", 1)
        self.assert_file_count("*.q", 0)
        msg = re.escape(
            "There should be 13 files matching 'a*.txt', but there are these: " +
            "['abcde.txt', 'afile.txt', 'axczz.txt']"
        )
        with pytest.raises(AssertionError, match=msg):
            self.assert_file_count("a*.txt", 13)
        msg = re.escape(
            "There should be 12 files matching '*c*.txt', but there are these: " +
            "['abcde.txt', 'axczz.txt']"
        )
        with pytest.raises(AssertionError, match=msg):
            self.assert_file_count("*c*.txt", 12)
        msg = re.escape(
            "There should be 11 files matching 'afile.*', but there are these: ['afile.txt']"
        )
        with pytest.raises(AssertionError, match=msg):
            self.assert_file_count("afile.*", 11)
        msg = re.escape(
            "There should be 10 files matching '*.q', but there are these: []"
        )
        with pytest.raises(AssertionError, match=msg):
            self.assert_file_count("*.q", 10)

    def test_assert_recent_datetime(self):
        def now_delta(seconds):
            """Make a datetime `seconds` seconds from now."""
            return datetime.datetime.now() + datetime.timedelta(seconds=seconds)

        # Default delta is 10 seconds.
        self.assert_recent_datetime(now_delta(0))
        self.assert_recent_datetime(now_delta(-9))
        with pytest.raises(AssertionError):
            self.assert_recent_datetime(now_delta(-11))
        with pytest.raises(AssertionError):
            self.assert_recent_datetime(now_delta(1))

        # Delta is settable.
        self.assert_recent_datetime(now_delta(0), seconds=120)
        self.assert_recent_datetime(now_delta(-100), seconds=120)
        with pytest.raises(AssertionError):
            self.assert_recent_datetime(now_delta(-1000), seconds=120)
        with pytest.raises(AssertionError):
            self.assert_recent_datetime(now_delta(1), seconds=120)

    def test_assert_warnings(self):
        cov = coverage.Coverage()

        # Make a warning, it should catch it properly.
        with self.assert_warnings(cov, ["Hello there!"]):
            cov._warn("Hello there!")

        # The expected warnings are regexes.
        with self.assert_warnings(cov, ["Hello.*!"]):
            cov._warn("Hello there!")

        # There can be a bunch of actual warnings.
        with self.assert_warnings(cov, ["Hello.*!"]):
            cov._warn("You there?")
            cov._warn("Hello there!")

        # There can be a bunch of expected warnings.
        with self.assert_warnings(cov, ["Hello.*!", "You"]):
            cov._warn("You there?")
            cov._warn("Hello there!")

        # But if there are a bunch of expected warnings, they have to all happen.
        warn_regex = r"Didn't find warning 'You' in \['Hello there!'\]"
        with pytest.raises(AssertionError, match=warn_regex):
            with self.assert_warnings(cov, ["Hello.*!", "You"]):
                cov._warn("Hello there!")

        # Make a different warning than expected, it should raise an assertion.
        warn_regex = r"Didn't find warning 'Not me' in \['Hello there!'\]"
        with pytest.raises(AssertionError, match=warn_regex):
            with self.assert_warnings(cov, ["Not me"]):
                cov._warn("Hello there!")

        # Try checking a warning that shouldn't appear: happy case.
        with self.assert_warnings(cov, ["Hi"], not_warnings=["Bye"]):
            cov._warn("Hi")

        # But it should fail if the unexpected warning does appear.
        warn_regex = r"Found warning 'Bye' in \['Hi', 'Bye'\]"
        with pytest.raises(AssertionError, match=warn_regex):
            with self.assert_warnings(cov, ["Hi"], not_warnings=["Bye"]):
                cov._warn("Hi")
                cov._warn("Bye")

        # assert_warnings shouldn't hide a real exception.
        with pytest.raises(ZeroDivisionError, match="oops"):
            with self.assert_warnings(cov, ["Hello there!"]):
                raise ZeroDivisionError("oops")

    def test_assert_no_warnings(self):
        cov = coverage.Coverage()

        # Happy path: no warnings.
        with self.assert_warnings(cov, []):
            pass

        # If you said there would be no warnings, and there were, fail!
        warn_regex = r"Unexpected warnings: \['Watch out!'\]"
        with pytest.raises(AssertionError, match=warn_regex):
            with self.assert_warnings(cov, []):
                cov._warn("Watch out!")

    def test_sub_python_is_this_python(self):
        # Try it with a Python command.
        self.set_environ('COV_FOOBAR', 'XYZZY')
        self.make_file("showme.py", """\
            import os, sys
            print(sys.executable)
            print(os.__file__)
            print(os.environ['COV_FOOBAR'])
            """)
        out = self.run_command("python showme.py").splitlines()
        assert actual_path(out[0]) == actual_path(sys.executable)
        assert out[1] == os.__file__
        assert out[2] == 'XYZZY'

        # Try it with a "coverage debug sys" command.
        out = self.run_command("coverage debug sys")

        executable = re_line("executable:", out)
        executable = executable.split(":", 1)[1].strip()
        assert _same_python_executable(executable, sys.executable)

        # "environment: COV_FOOBAR = XYZZY" or "COV_FOOBAR = XYZZY"
        environ = re_line("COV_FOOBAR", out)
        _, _, environ = environ.rpartition(":")
        assert environ.strip() == "COV_FOOBAR = XYZZY"

    def test_run_command_stdout_stderr(self):
        # run_command should give us both stdout and stderr.
        self.make_file("outputs.py", """\
            import sys
            sys.stderr.write("StdErr\\n")
            print("StdOut")
            """)
        out = self.run_command("python outputs.py")
        assert "StdOut\n" in out
        assert "StdErr\n" in out

    def test_stdout(self):
        # stdout is captured.
        print("This is stdout")
        print("Line 2")
        assert self.stdout() == "This is stdout\nLine 2\n"
        # When we grab stdout(), it's reset.
        print("Some more")
        assert self.stdout() == "Some more\n"


class CheckUniqueFilenamesTest(CoverageTest):
    """Tests of CheckUniqueFilenames."""

    run_in_temp_dir = False

    class Stub:
        """A stand-in for the class we're checking."""
        def __init__(self, x):
            self.x = x

        def method(self, filename, a=17, b="hello"):
            """The method we'll wrap, with args to be sure args work."""
            return (self.x, filename, a, b)

    def test_detect_duplicate(self):
        stub = self.Stub(23)
        CheckUniqueFilenames.hook(stub, "method")

        # Two method calls with different names are fine.
        assert stub.method("file1") == (23, "file1", 17, "hello")
        assert stub.method("file2", 1723, b="what") == (23, "file2", 1723, "what")

        # A duplicate file name trips an assertion.
        with pytest.raises(AssertionError):
            stub.method("file1")


class CheckCoverageTest(CoverageTest):
    """Tests of the failure assertions in check_coverage."""

    CODE = """\
        a, b = 1, 1
        def oops(x):
            if x % 2:
                raise Exception("odd")
        try:
            a = 6
            oops(1)
            a = 8
        except:
            b = 10
        assert a == 6 and b == 10
        """
    ARCZ = ".1 12 -23 34 3-2 4-2 25 56 67 78 8B 9A AB B."
    ARCZ_MISSING = "3-2 78 8B"
    ARCZ_UNPREDICTED = "79"

    def test_check_coverage_possible(self):
        msg = r"(?s)Possible arcs differ: .*- \(6, 3\).*\+ \(6, 7\)"
        with pytest.raises(AssertionError, match=msg):
            self.check_coverage(
                self.CODE,
                arcz=self.ARCZ.replace("7", "3"),
                arcz_missing=self.ARCZ_MISSING,
                arcz_unpredicted=self.ARCZ_UNPREDICTED,
            )

    def test_check_coverage_missing(self):
        msg = r"(?s)Missing arcs differ: .*- \(3, 8\).*\+ \(7, 8\)"
        with pytest.raises(AssertionError, match=msg):
            self.check_coverage(
                self.CODE,
                arcz=self.ARCZ,
                arcz_missing=self.ARCZ_MISSING.replace("7", "3"),
                arcz_unpredicted=self.ARCZ_UNPREDICTED,
            )

    def test_check_coverage_unpredicted(self):
        msg = r"(?s)Unpredicted arcs differ: .*- \(3, 9\).*\+ \(7, 9\)"
        with pytest.raises(AssertionError, match=msg):
            self.check_coverage(
                self.CODE,
                arcz=self.ARCZ,
                arcz_missing=self.ARCZ_MISSING,
                arcz_unpredicted=self.ARCZ_UNPREDICTED.replace("7", "3")
            )


class ReLinesTest(CoverageTest):
    """Tests of `re_lines`."""

    run_in_temp_dir = False

    @pytest.mark.parametrize("pat, text, result", [
        ("line", "line1\nline2\nline3\n", "line1\nline2\nline3\n"),
        ("[13]", "line1\nline2\nline3\n", "line1\nline3\n"),
        ("X", "line1\nline2\nline3\n", ""),
    ])
    def test_re_lines(self, pat, text, result):
        assert re_lines_text(pat, text) == result
        assert re_lines(pat, text) == result.splitlines()

    @pytest.mark.parametrize("pat, text, result", [
        ("line", "line1\nline2\nline3\n", ""),
        ("[13]", "line1\nline2\nline3\n", "line2\n"),
        ("X", "line1\nline2\nline3\n", "line1\nline2\nline3\n"),
    ])
    def test_re_lines_inverted(self, pat, text, result):
        assert re_lines_text(pat, text, match=False) == result
        assert re_lines(pat, text, match=False) == result.splitlines()

    @pytest.mark.parametrize("pat, text, result", [
        ("2", "line1\nline2\nline3\n", "line2"),
    ])
    def test_re_line(self, pat, text, result):
        assert re_line(pat, text) == result

    @pytest.mark.parametrize("pat, text", [
        ("line", "line1\nline2\nline3\n"),      # too many matches
        ("X", "line1\nline2\nline3\n"),         # no matches
    ])
    def test_re_line_bad(self, pat, text):
        with pytest.raises(AssertionError):
            re_line(pat, text)


def _same_python_executable(e1, e2):
    """Determine if `e1` and `e2` refer to the same Python executable.

    Either path could include symbolic links.  The two paths might not refer
    to the exact same file, but if they are in the same directory and their
    numeric suffixes aren't different, they are the same executable.

    """
    e1 = os.path.abspath(os.path.realpath(e1))
    e2 = os.path.abspath(os.path.realpath(e2))

    if os.path.dirname(e1) != os.path.dirname(e2):
        return False                                    # pragma: only failure

    e1 = os.path.basename(e1)
    e2 = os.path.basename(e2)

    if e1 == "python" or e2 == "python" or e1 == e2:
        # Python and Python2.3: OK
        # Python2.3 and Python: OK
        # Python and Python: OK
        # Python2.3 and Python2.3: OK
        return True

    return False                                        # pragma: only failure


def test_without_module():
    toml1 = tomlconfig.tomli
    with without_module(tomlconfig, 'tomli'):
        toml2 = tomlconfig.tomli
    toml3 = tomlconfig.tomli

    assert toml1 is toml3 is not None
    assert toml2 is None


class ArczTest(CoverageTest):
    """Tests of arcz/arcs helpers."""

    run_in_temp_dir = False

    @pytest.mark.parametrize("arcz, arcs", [
        (".1 12 2.", [(-1, 1), (1, 2), (2, -1)]),
        ("-11 12 2-5", [(-1, 1), (1, 2), (2, -5)]),
        ("-QA CB IT Z-A", [(-26, 10), (12, 11), (18, 29), (35, -10)]),
    ])
    def test_arcz_to_arcs(self, arcz, arcs):
        assert arcz_to_arcs(arcz) == arcs

    @pytest.mark.parametrize("arcs, arcz_repr", [
        ([(-1, 1), (1, 2), (2, -1)], "(-1, 1) # .1\n(1, 2) # 12\n(2, -1) # 2.\n"),
        ([(-1, 1), (1, 2), (2, -5)], "(-1, 1) # .1\n(1, 2) # 12\n(2, -5) # 2-5\n"),
        ([(-26, 10), (12, 11), (18, 29), (35, -10), (1, 33), (100, 7)],
            (
            "(-26, 10) # -QA\n" +
            "(12, 11) # CB\n" +
            "(18, 29) # IT\n" +
            "(35, -10) # Z-A\n" +
            "(1, 33) # 1X\n" +
            "(100, 7) # ?7\n"
            )
        ),
    ])
    def test_arcs_to_arcz_repr(self, arcs, arcz_repr):
        assert arcs_to_arcz_repr(arcs) == arcz_repr


class AssertCoverageWarningsTest(CoverageTest):
    """Tests of assert_coverage_warnings"""

    def test_one_warning(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("Hello there", category=CoverageWarning)
        assert_coverage_warnings(warns, "Hello there")

    def test_many_warnings(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("The first", category=CoverageWarning)
            warnings.warn("The second", category=CoverageWarning)
            warnings.warn("The third", category=CoverageWarning)
        assert_coverage_warnings(warns, "The first", "The second", "The third")

    def test_wrong_type(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("Not ours", category=Warning)
        with pytest.raises(AssertionError):
            assert_coverage_warnings(warns, "Not ours")

    def test_wrong_message(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("Goodbye", category=CoverageWarning)
        with pytest.raises(AssertionError):
            assert_coverage_warnings(warns, "Hello there")

    def test_wrong_number_too_many(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("The first", category=CoverageWarning)
            warnings.warn("The second", category=CoverageWarning)
        with pytest.raises(AssertionError):
            assert_coverage_warnings(warns, "The first", "The second", "The third")

    def test_wrong_number_too_few(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("The first", category=CoverageWarning)
            warnings.warn("The second", category=CoverageWarning)
            warnings.warn("The third", category=CoverageWarning)
        with pytest.raises(AssertionError):
            assert_coverage_warnings(warns, "The first", "The second")

    def test_regex_matches(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("The first", category=CoverageWarning)
        assert_coverage_warnings(warns, re.compile("f?rst"))

    def test_regex_doesnt_match(self):
        with pytest.warns(Warning) as warns:
            warnings.warn("The first", category=CoverageWarning)
        with pytest.raises(AssertionError):
            assert_coverage_warnings(warns, re.compile("second"))
