# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/nedbat/coveragepy/blob/master/NOTICE.txt

"""Core control stuff for coverage.py."""

import atexit
import collections
import contextlib
import os
import os.path
import platform
import sys
import time
import warnings

from coverage import env
from coverage.annotate import AnnotateReporter
from coverage.collector import Collector, CTracer
from coverage.config import read_coverage_config
from coverage.context import should_start_context_test_function, combine_context_switchers
from coverage.data import CoverageData, combine_parallel_data
from coverage.debug import DebugControl, short_stack, write_formatted_info
from coverage.disposition import disposition_debug_msg
from coverage.exceptions import ConfigError, CoverageException, CoverageWarning, PluginError
from coverage.files import PathAliases, abs_file, relative_filename, set_relative_directory
from coverage.html import HtmlReporter
from coverage.inorout import InOrOut
from coverage.jsonreport import JsonReporter
from coverage.misc import bool_or_none, join_regex, human_sorted, human_sorted_items
from coverage.misc import DefaultValue, ensure_dir_for_file, isolate_module
from coverage.plugin import FileReporter
from coverage.plugin_support import Plugins
from coverage.python import PythonFileReporter
from coverage.report import render_report
from coverage.results import Analysis
from coverage.summary import SummaryReporter
from coverage.xmlreport import XmlReporter

try:
    from coverage.multiproc import patch_multiprocessing
except ImportError:                                         # pragma: only jython
    # Jython has no multiprocessing module.
    patch_multiprocessing = None

os = isolate_module(os)

@contextlib.contextmanager
def override_config(cov, **kwargs):
    """Temporarily tweak the configuration of `cov`.

    The arguments are applied to `cov.config` with the `from_args` method.
    At the end of the with-statement, the old configuration is restored.
    """
    original_config = cov.config
    cov.config = cov.config.copy()
    try:
        cov.config.from_args(**kwargs)
        yield
    finally:
        cov.config = original_config


_DEFAULT_DATAFILE = DefaultValue("MISSING")

class Coverage:
    """Programmatic access to coverage.py.

    To use::

        from coverage import Coverage

        cov = Coverage()
        cov.start()
        #.. call your code ..
        cov.stop()
        cov.html_report(directory='covhtml')

    Note: in keeping with Python custom, names starting with underscore are
    not part of the public API. They might stop working at any point.  Please
    limit yourself to documented methods to avoid problems.

    Methods can raise any of the exceptions described in :ref:`api_exceptions`.

    """

    # The stack of started Coverage instances.
    _instances = []

    @classmethod
    def current(cls):
        """Get the latest started `Coverage` instance, if any.

        Returns: a `Coverage` instance, or None.

        .. versionadded:: 5.0

        """
        if cls._instances:
            return cls._instances[-1]
        else:
            return None

    def __init__(
        self, data_file=_DEFAULT_DATAFILE, data_suffix=None, cover_pylib=None,
        auto_data=False, timid=None, branch=None, config_file=True,
        source=None, source_pkgs=None, omit=None, include=None, debug=None,
        concurrency=None, check_preimported=False, context=None,
        messages=False,
    ):  # pylint: disable=too-many-arguments
        """
        Many of these arguments duplicate and override values that can be
        provided in a configuration file.  Parameters that are missing here
        will use values from the config file.

        `data_file` is the base name of the data file to use. The config value
        defaults to ".coverage".  None can be provided to prevent writing a data
        file.  `data_suffix` is appended (with a dot) to `data_file` to create
        the final file name.  If `data_suffix` is simply True, then a suffix is
        created with the machine and process identity included.

        `cover_pylib` is a boolean determining whether Python code installed
        with the Python interpreter is measured.  This includes the Python
        standard library and any packages installed with the interpreter.

        If `auto_data` is true, then any existing data file will be read when
        coverage measurement starts, and data will be saved automatically when
        measurement stops.

        If `timid` is true, then a slower and simpler trace function will be
        used.  This is important for some environments where manipulation of
        tracing functions breaks the faster trace function.

        If `branch` is true, then branch coverage will be measured in addition
        to the usual statement coverage.

        `config_file` determines what configuration file to read:

            * If it is ".coveragerc", it is interpreted as if it were True,
              for backward compatibility.

            * If it is a string, it is the name of the file to read.  If the
              file can't be read, it is an error.

            * If it is True, then a few standard files names are tried
              (".coveragerc", "setup.cfg", "tox.ini").  It is not an error for
              these files to not be found.

            * If it is False, then no configuration file is read.

        `source` is a list of file paths or package names.  Only code located
        in the trees indicated by the file paths or package names will be
        measured.

        `source_pkgs` is a list of package names. It works the same as
        `source`, but can be used to name packages where the name can also be
        interpreted as a file path.

        `include` and `omit` are lists of file name patterns. Files that match
        `include` will be measured, files that match `omit` will not.  Each
        will also accept a single string argument.

        `debug` is a list of strings indicating what debugging information is
        desired.

        `concurrency` is a string indicating the concurrency library being used
        in the measured code.  Without this, coverage.py will get incorrect
        results if these libraries are in use.  Valid strings are "greenlet",
        "eventlet", "gevent", "multiprocessing", or "thread" (the default).
        This can also be a list of these strings.

        If `check_preimported` is true, then when coverage is started, the
        already-imported files will be checked to see if they should be
        measured by coverage.  Importing measured files before coverage is
        started can mean that code is missed.

        `context` is a string to use as the :ref:`static context
        <static_contexts>` label for collected data.

        If `messages` is true, some messages will be printed to stdout
        indicating what is happening.

        .. versionadded:: 4.0
            The `concurrency` parameter.

        .. versionadded:: 4.2
            The `concurrency` parameter can now be a list of strings.

        .. versionadded:: 5.0
            The `check_preimported` and `context` parameters.

        .. versionadded:: 5.3
            The `source_pkgs` parameter.

        .. versionadded:: 6.0
            The `messages` parameter.

        """
        # data_file=None means no disk file at all. data_file missing means
        # use the value from the config file.
        self._no_disk = data_file is None
        if data_file is _DEFAULT_DATAFILE:
            data_file = None

        self.config = None

        # This is injectable by tests.
        self._debug_file = None

        self._auto_load = self._auto_save = auto_data
        self._data_suffix_specified = data_suffix

        # Is it ok for no data to be collected?
        self._warn_no_data = True
        self._warn_unimported_source = True
        self._warn_preimported_source = check_preimported
        self._no_warn_slugs = None
        self._messages = messages

        # A record of all the warnings that have been issued.
        self._warnings = []

        # Other instance attributes, set later.
        self._data = self._collector = None
        self._plugins = None
        self._inorout = None
        self._data_suffix = self._run_suffix = None
        self._exclude_re = None
        self._debug = None
        self._file_mapper = None

        # State machine variables:
        # Have we initialized everything?
        self._inited = False
        self._inited_for_start = False
        # Have we started collecting and not stopped it?
        self._started = False
        # Should we write the debug output?
        self._should_write_debug = True

        # Build our configuration from a number of sources.
        self.config = read_coverage_config(
            config_file=config_file, warn=self._warn,
            data_file=data_file, cover_pylib=cover_pylib, timid=timid,
            branch=branch, parallel=bool_or_none(data_suffix),
            source=source, source_pkgs=source_pkgs, run_omit=omit, run_include=include, debug=debug,
            report_omit=omit, report_include=include,
            concurrency=concurrency, context=context,
            )

        # If we have sub-process measurement happening automatically, then we
        # want any explicit creation of a Coverage object to mean, this process
        # is already coverage-aware, so don't auto-measure it.  By now, the
        # auto-creation of a Coverage object has already happened.  But we can
        # find it and tell it not to save its data.
        if not env.METACOV:
            _prevent_sub_process_measurement()

    def _init(self):
        """Set all the initial state.

        This is called by the public methods to initialize state. This lets us
        construct a :class:`Coverage` object, then tweak its state before this
        function is called.

        """
        if self._inited:
            return

        self._inited = True

        # Create and configure the debugging controller. COVERAGE_DEBUG_FILE
        # is an environment variable, the name of a file to append debug logs
        # to.
        self._debug = DebugControl(self.config.debug, self._debug_file)

        if "multiprocessing" in (self.config.concurrency or ()):
            # Multi-processing uses parallel for the subprocesses, so also use
            # it for the main process.
            self.config.parallel = True

        # _exclude_re is a dict that maps exclusion list names to compiled regexes.
        self._exclude_re = {}

        set_relative_directory()
        self._file_mapper = relative_filename if self.config.relative_files else abs_file

        # Load plugins
        self._plugins = Plugins.load_plugins(self.config.plugins, self.config, self._debug)

        # Run configuring plugins.
        for plugin in self._plugins.configurers:
            # We need an object with set_option and get_option. Either self or
            # self.config will do. Choosing randomly stops people from doing
            # other things with those objects, against the public API.  Yes,
            # this is a bit childish. :)
            plugin.configure([self, self.config][int(time.time()) % 2])

    def _post_init(self):
        """Stuff to do after everything is initialized."""
        if self._should_write_debug:
            self._should_write_debug = False
            self._write_startup_debug()

        # '[run] _crash' will raise an exception if the value is close by in
        # the call stack, for testing error handling.
        if self.config._crash and self.config._crash in short_stack(limit=4):
            raise Exception(f"Crashing because called by {self.config._crash}")

    def _write_startup_debug(self):
        """Write out debug info at startup if needed."""
        wrote_any = False
        with self._debug.without_callers():
            if self._debug.should('config'):
                config_info = human_sorted_items(self.config.__dict__.items())
                config_info = [(k, v) for k, v in config_info if not k.startswith('_')]
                write_formatted_info(self._debug, "config", config_info)
                wrote_any = True

            if self._debug.should('sys'):
                write_formatted_info(self._debug, "sys", self.sys_info())
                for plugin in self._plugins:
                    header = "sys: " + plugin._coverage_plugin_name
                    info = plugin.sys_info()
                    write_formatted_info(self._debug, header, info)
                wrote_any = True

        if wrote_any:
            write_formatted_info(self._debug, "end", ())

    def _should_trace(self, filename, frame):
        """Decide whether to trace execution in `filename`.

        Calls `_should_trace_internal`, and returns the FileDisposition.

        """
        disp = self._inorout.should_trace(filename, frame)
        if self._debug.should('trace'):
            self._debug.write(disposition_debug_msg(disp))
        return disp

    def _check_include_omit_etc(self, filename, frame):
        """Check a file name against the include/omit/etc, rules, verbosely.

        Returns a boolean: True if the file should be traced, False if not.

        """
        reason = self._inorout.check_include_omit_etc(filename, frame)
        if self._debug.should('trace'):
            if not reason:
                msg = f"Including {filename!r}"
            else:
                msg = f"Not including {filename!r}: {reason}"
            self._debug.write(msg)

        return not reason

    def _warn(self, msg, slug=None, once=False):
        """Use `msg` as a warning.

        For warning suppression, use `slug` as the shorthand.

        If `once` is true, only show this warning once (determined by the
        slug.)

        """
        if self._no_warn_slugs is None:
            if self.config is not None:
                self._no_warn_slugs = list(self.config.disable_warnings)

        if self._no_warn_slugs is not None:
            if slug in self._no_warn_slugs:
                # Don't issue the warning
                return

        self._warnings.append(msg)
        if slug:
            msg = f"{msg} ({slug})"
        if self._debug is not None and self._debug.should('pid'):
            msg = f"[{os.getpid()}] {msg}"
        warnings.warn(msg, category=CoverageWarning, stacklevel=2)

        if once:
            self._no_warn_slugs.append(slug)

    def _message(self, msg):
        """Write a message to the user, if configured to do so."""
        if self._messages:
            print(msg)

    def get_option(self, option_name):
        """Get an option from the configuration.

        `option_name` is a colon-separated string indicating the section and
        option name.  For example, the ``branch`` option in the ``[run]``
        section of the config file would be indicated with `"run:branch"`.

        Returns the value of the option.  The type depends on the option
        selected.

        As a special case, an `option_name` of ``"paths"`` will return an
        OrderedDict with the entire ``[paths]`` section value.

        .. versionadded:: 4.0

        """
        return self.config.get_option(option_name)

    def set_option(self, option_name, value):
        """Set an option in the configuration.

        `option_name` is a colon-separated string indicating the section and
        option name.  For example, the ``branch`` option in the ``[run]``
        section of the config file would be indicated with ``"run:branch"``.

        `value` is the new value for the option.  This should be an
        appropriate Python value.  For example, use True for booleans, not the
        string ``"True"``.

        As an example, calling::

            cov.set_option("run:branch", True)

        has the same effect as this configuration file::

            [run]
            branch = True

        As a special case, an `option_name` of ``"paths"`` will replace the
        entire ``[paths]`` section.  The value should be an OrderedDict.

        .. versionadded:: 4.0

        """
        self.config.set_option(option_name, value)

    def load(self):
        """Load previously-collected coverage data from the data file."""
        self._init()
        if self._collector:
            self._collector.reset()
        should_skip = self.config.parallel and not os.path.exists(self.config.data_file)
        if not should_skip:
            self._init_data(suffix=None)
        self._post_init()
        if not should_skip:
            self._data.read()

    def _init_for_start(self):
        """Initialization for start()"""
        # Construct the collector.
        concurrency = self.config.concurrency or []
        if "multiprocessing" in concurrency:
            if not patch_multiprocessing:
                raise ConfigError(                      # pragma: only jython
                    "multiprocessing is not supported on this Python"
                )
            patch_multiprocessing(rcfile=self.config.config_file)

        dycon = self.config.dynamic_context
        if not dycon or dycon == "none":
            context_switchers = []
        elif dycon == "test_function":
            context_switchers = [should_start_context_test_function]
        else:
            raise ConfigError(f"Don't understand dynamic_context setting: {dycon!r}")

        context_switchers.extend(
            plugin.dynamic_context for plugin in self._plugins.context_switchers
        )

        should_start_context = combine_context_switchers(context_switchers)

        self._collector = Collector(
            should_trace=self._should_trace,
            check_include=self._check_include_omit_etc,
            should_start_context=should_start_context,
            file_mapper=self._file_mapper,
            timid=self.config.timid,
            branch=self.config.branch,
            warn=self._warn,
            concurrency=concurrency,
            )

        suffix = self._data_suffix_specified
        if suffix:
            if not isinstance(suffix, str):
                # if data_suffix=True, use .machinename.pid.random
                suffix = True
        elif self.config.parallel:
            if suffix is None:
                suffix = True
            elif not isinstance(suffix, str):
                suffix = bool(suffix)
        else:
            suffix = None

        self._init_data(suffix)

        self._collector.use_data(self._data, self.config.context)

        # Early warning if we aren't going to be able to support plugins.
        if self._plugins.file_tracers and not self._collector.supports_plugins:
            self._warn(
                "Plugin file tracers ({}) aren't supported with {}".format(
                    ", ".join(
                        plugin._coverage_plugin_name
                            for plugin in self._plugins.file_tracers
                        ),
                    self._collector.tracer_name(),
                    )
                )
            for plugin in self._plugins.file_tracers:
                plugin._coverage_enabled = False

        # Create the file classifying substructure.
        self._inorout = InOrOut(
            warn=self._warn,
            debug=(self._debug if self._debug.should('trace') else None),
        )
        self._inorout.configure(self.config)
        self._inorout.plugins = self._plugins
        self._inorout.disp_class = self._collector.file_disposition_class

        # It's useful to write debug info after initing for start.
        self._should_write_debug = True

        atexit.register(self._atexit)

    def _init_data(self, suffix):
        """Create a data file if we don't have one yet."""
        if self._data is None:
            # Create the data file.  We do this at construction time so that the
            # data file will be written into the directory where the process
            # started rather than wherever the process eventually chdir'd to.
            ensure_dir_for_file(self.config.data_file)
            self._data = CoverageData(
                basename=self.config.data_file,
                suffix=suffix,
                warn=self._warn,
                debug=self._debug,
                no_disk=self._no_disk,
            )

    def start(self):
        """Start measuring code coverage.

        Coverage measurement only occurs in functions called after
        :meth:`start` is invoked.  Statements in the same scope as
        :meth:`start` won't be measured.

        Once you invoke :meth:`start`, you must also call :meth:`stop`
        eventually, or your process might not shut down cleanly.

        """
        self._init()
        if not self._inited_for_start:
            self._inited_for_start = True
            self._init_for_start()
        self._post_init()

        # Issue warnings for possible problems.
        self._inorout.warn_conflicting_settings()

        # See if we think some code that would eventually be measured has
        # already been imported.
        if self._warn_preimported_source:
            self._inorout.warn_already_imported_files()

        if self._auto_load:
            self.load()

        self._collector.start()
        self._started = True
        self._instances.append(self)

    def stop(self):
        """Stop measuring code coverage."""
        if self._instances:
            if self._instances[-1] is self:
                self._instances.pop()
        if self._started:
            self._collector.stop()
        self._started = False

    def _atexit(self):
        """Clean up on process shutdown."""
        if self._debug.should("process"):
            self._debug.write(f"atexit: pid: {os.getpid()}, instance: {self!r}")
        if self._started:
            self.stop()
        if self._auto_save:
            self.save()

    def erase(self):
        """Erase previously collected coverage data.

        This removes the in-memory data collected in this session as well as
        discarding the data file.

        """
        self._init()
        self._post_init()
        if self._collector:
            self._collector.reset()
        self._init_data(suffix=None)
        self._data.erase(parallel=self.config.parallel)
        self._data = None
        self._inited_for_start = False

    def switch_context(self, new_context):
        """Switch to a new dynamic context.

        `new_context` is a string to use as the :ref:`dynamic context
        <dynamic_contexts>` label for collected data.  If a :ref:`static
        context <static_contexts>` is in use, the static and dynamic context
        labels will be joined together with a pipe character.

        Coverage collection must be started already.

        .. versionadded:: 5.0

        """
        if not self._started:                           # pragma: part started
            raise CoverageException("Cannot switch context, coverage is not started")

        if self._collector.should_start_context:
            self._warn("Conflicting dynamic contexts", slug="dynamic-conflict", once=True)

        self._collector.switch_context(new_context)

    def clear_exclude(self, which='exclude'):
        """Clear the exclude list."""
        self._init()
        setattr(self.config, which + "_list", [])
        self._exclude_regex_stale()

    def exclude(self, regex, which='exclude'):
        """Exclude source lines from execution consideration.

        A number of lists of regular expressions are maintained.  Each list
        selects lines that are treated differently during reporting.

        `which` determines which list is modified.  The "exclude" list selects
        lines that are not considered executable at all.  The "partial" list
        indicates lines with branches that are not taken.

        `regex` is a regular expression.  The regex is added to the specified
        list.  If any of the regexes in the list is found in a line, the line
        is marked for special treatment during reporting.

        """
        self._init()
        excl_list = getattr(self.config, which + "_list")
        excl_list.append(regex)
        self._exclude_regex_stale()

    def _exclude_regex_stale(self):
        """Drop all the compiled exclusion regexes, a list was modified."""
        self._exclude_re.clear()

    def _exclude_regex(self, which):
        """Return a compiled regex for the given exclusion list."""
        if which not in self._exclude_re:
            excl_list = getattr(self.config, which + "_list")
            self._exclude_re[which] = join_regex(excl_list)
        return self._exclude_re[which]

    def get_exclude_list(self, which='exclude'):
        """Return a list of excluded regex patterns.

        `which` indicates which list is desired.  See :meth:`exclude` for the
        lists that are available, and their meaning.

        """
        self._init()
        return getattr(self.config, which + "_list")

    def save(self):
        """Save the collected coverage data to the data file."""
        data = self.get_data()
        data.write()

    def combine(self, data_paths=None, strict=False, keep=False):
        """Combine together a number of similarly-named coverage data files.

        All coverage data files whose name starts with `data_file` (from the
        coverage() constructor) will be read, and combined together into the
        current measurements.

        `data_paths` is a list of files or directories from which data should
        be combined. If no list is passed, then the data files from the
        directory indicated by the current data file (probably the current
        directory) will be combined.

        If `strict` is true, then it is an error to attempt to combine when
        there are no data files to combine.

        If `keep` is true, then original input data files won't be deleted.

        .. versionadded:: 4.0
            The `data_paths` parameter.

        .. versionadded:: 4.3
            The `strict` parameter.

        .. versionadded: 5.5
            The `keep` parameter.
        """
        self._init()
        self._init_data(suffix=None)
        self._post_init()
        self.get_data()

        aliases = None
        if self.config.paths:
            aliases = PathAliases(relative=self.config.relative_files)
            for paths in self.config.paths.values():
                result = paths[0]
                for pattern in paths[1:]:
                    aliases.add(pattern, result)

        combine_parallel_data(
            self._data,
            aliases=aliases,
            data_paths=data_paths,
            strict=strict,
            keep=keep,
            message=self._message,
        )

    def get_data(self):
        """Get the collected data.

        Also warn about various problems collecting data.

        Returns a :class:`coverage.CoverageData`, the collected coverage data.

        .. versionadded:: 4.0

        """
        self._init()
        self._init_data(suffix=None)
        self._post_init()

        for plugin in self._plugins:
            if not plugin._coverage_enabled:
                self._collector.plugin_was_disabled(plugin)

        if self._collector and self._collector.flush_data():
            self._post_save_work()

        return self._data

    def _post_save_work(self):
        """After saving data, look for warnings, post-work, etc.

        Warn about things that should have happened but didn't.
        Look for unexecuted files.

        """
        # If there are still entries in the source_pkgs_unmatched list,
        # then we never encountered those packages.
        if self._warn_unimported_source:
            self._inorout.warn_unimported_source()

        # Find out if we got any data.
        if not self._data and self._warn_no_data:
            self._warn("No data was collected.", slug="no-data-collected")

        # Touch all the files that could have executed, so that we can
        # mark completely unexecuted files as 0% covered.
        if self._data is not None:
            file_paths = collections.defaultdict(list)
            for file_path, plugin_name in self._inorout.find_possibly_unexecuted_files():
                file_path = self._file_mapper(file_path)
                file_paths[plugin_name].append(file_path)
            for plugin_name, paths in file_paths.items():
                self._data.touch_files(paths, plugin_name)

        if self.config.note:
            self._warn("The '[run] note' setting is no longer supported.")

    # Backward compatibility with version 1.
    def analysis(self, morf):
        """Like `analysis2` but doesn't return excluded line numbers."""
        f, s, _, m, mf = self.analysis2(morf)
        return f, s, m, mf

    def analysis2(self, morf):
        """Analyze a module.

        `morf` is a module or a file name.  It will be analyzed to determine
        its coverage statistics.  The return value is a 5-tuple:

        * The file name for the module.
        * A list of line numbers of executable statements.
        * A list of line numbers of excluded statements.
        * A list of line numbers of statements not run (missing from
          execution).
        * A readable formatted string of the missing line numbers.

        The analysis uses the source file itself and the current measured
        coverage data.

        """
        analysis = self._analyze(morf)
        return (
            analysis.filename,
            sorted(analysis.statements),
            sorted(analysis.excluded),
            sorted(analysis.missing),
            analysis.missing_formatted(),
            )

    def _analyze(self, it):
        """Analyze a single morf or code unit.

        Returns an `Analysis` object.

        """
        # All reporting comes through here, so do reporting initialization.
        self._init()
        self._post_init()

        data = self.get_data()
        if not isinstance(it, FileReporter):
            it = self._get_file_reporter(it)

        return Analysis(data, self.config.precision, it, self._file_mapper)

    def _get_file_reporter(self, morf):
        """Get a FileReporter for a module or file name."""
        plugin = None
        file_reporter = "python"

        if isinstance(morf, str):
            mapped_morf = self._file_mapper(morf)
            plugin_name = self._data.file_tracer(mapped_morf)
            if plugin_name:
                plugin = self._plugins.get(plugin_name)

                if plugin:
                    file_reporter = plugin.file_reporter(mapped_morf)
                    if file_reporter is None:
                        raise PluginError(
                            "Plugin {!r} did not provide a file reporter for {!r}.".format(
                                plugin._coverage_plugin_name, morf
                            )
                        )

        if file_reporter == "python":
            file_reporter = PythonFileReporter(morf, self)

        return file_reporter

    def _get_file_reporters(self, morfs=None):
        """Get a list of FileReporters for a list of modules or file names.

        For each module or file name in `morfs`, find a FileReporter.  Return
        the list of FileReporters.

        If `morfs` is a single module or file name, this returns a list of one
        FileReporter.  If `morfs` is empty or None, then the list of all files
        measured is used to find the FileReporters.

        """
        if not morfs:
            morfs = self._data.measured_files()

        # Be sure we have a collection.
        if not isinstance(morfs, (list, tuple, set)):
            morfs = [morfs]

        file_reporters = [self._get_file_reporter(morf) for morf in morfs]
        return file_reporters

    def report(
        self, morfs=None, show_missing=None, ignore_errors=None,
        file=None, omit=None, include=None, skip_covered=None,
        contexts=None, skip_empty=None, precision=None, sort=None
    ):
        """Write a textual summary report to `file`.

        Each module in `morfs` is listed, with counts of statements, executed
        statements, missing statements, and a list of lines missed.

        If `show_missing` is true, then details of which lines or branches are
        missing will be included in the report.  If `ignore_errors` is true,
        then a failure while reporting a single file will not stop the entire
        report.

        `file` is a file-like object, suitable for writing.

        `include` is a list of file name patterns.  Files that match will be
        included in the report. Files matching `omit` will not be included in
        the report.

        If `skip_covered` is true, don't report on files with 100% coverage.

        If `skip_empty` is true, don't report on empty files (those that have
        no statements).

        `contexts` is a list of regular expressions.  Only data from
        :ref:`dynamic contexts <dynamic_contexts>` that match one of those
        expressions (using :func:`re.search <python:re.search>`) will be
        included in the report.

        `precision` is the number of digits to display after the decimal
        point for percentages.

        All of the arguments default to the settings read from the
        :ref:`configuration file <config>`.

        Returns a float, the total percentage covered.

        .. versionadded:: 4.0
            The `skip_covered` parameter.

        .. versionadded:: 5.0
            The `contexts` and `skip_empty` parameters.

        .. versionadded:: 5.2
            The `precision` parameter.

        """
        with override_config(
            self,
            ignore_errors=ignore_errors, report_omit=omit, report_include=include,
            show_missing=show_missing, skip_covered=skip_covered,
            report_contexts=contexts, skip_empty=skip_empty, precision=precision,
            sort=sort
        ):
            reporter = SummaryReporter(self)
            return reporter.report(morfs, outfile=file)

    def annotate(
        self, morfs=None, directory=None, ignore_errors=None,
        omit=None, include=None, contexts=None,
    ):
        """Annotate a list of modules.

        .. note::

            This method has been obsoleted by more modern reporting tools,
            including the :meth:`html_report` method.  It will be removed in a
            future version.

        Each module in `morfs` is annotated.  The source is written to a new
        file, named with a ",cover" suffix, with each line prefixed with a
        marker to indicate the coverage of the line.  Covered lines have ">",
        excluded lines have "-", and missing lines have "!".

        See :meth:`report` for other arguments.

        """
        print("The annotate command will be removed in a future version.")
        print("Get in touch if you still use it: ned@nedbatchelder.com")

        with override_config(self,
            ignore_errors=ignore_errors, report_omit=omit,
            report_include=include, report_contexts=contexts,
        ):
            reporter = AnnotateReporter(self)
            reporter.report(morfs, directory=directory)

    def html_report(
        self, morfs=None, directory=None, ignore_errors=None,
        omit=None, include=None, extra_css=None, title=None,
        skip_covered=None, show_contexts=None, contexts=None,
        skip_empty=None, precision=None,
    ):
        """Generate an HTML report.

        The HTML is written to `directory`.  The file "index.html" is the
        overview starting point, with links to more detailed pages for
        individual modules.

        `extra_css` is a path to a file of other CSS to apply on the page.
        It will be copied into the HTML directory.

        `title` is a text string (not HTML) to use as the title of the HTML
        report.

        See :meth:`report` for other arguments.

        Returns a float, the total percentage covered.

        .. note::

            The HTML report files are generated incrementally based on the
            source files and coverage results. If you modify the report files,
            the changes will not be considered.  You should be careful about
            changing the files in the report folder.

        """
        with override_config(self,
            ignore_errors=ignore_errors, report_omit=omit, report_include=include,
            html_dir=directory, extra_css=extra_css, html_title=title,
            html_skip_covered=skip_covered, show_contexts=show_contexts, report_contexts=contexts,
            html_skip_empty=skip_empty, precision=precision,
        ):
            reporter = HtmlReporter(self)
            ret = reporter.report(morfs)
            return ret

    def xml_report(
        self, morfs=None, outfile=None, ignore_errors=None,
        omit=None, include=None, contexts=None, skip_empty=None,
    ):
        """Generate an XML report of coverage results.

        The report is compatible with Cobertura reports.

        Each module in `morfs` is included in the report.  `outfile` is the
        path to write the file to, "-" will write to stdout.

        See :meth:`report` for other arguments.

        Returns a float, the total percentage covered.

        """
        with override_config(self,
            ignore_errors=ignore_errors, report_omit=omit, report_include=include,
            xml_output=outfile, report_contexts=contexts, skip_empty=skip_empty,
        ):
            return render_report(self.config.xml_output, XmlReporter(self), morfs, self._message)

    def json_report(
        self, morfs=None, outfile=None, ignore_errors=None,
        omit=None, include=None, contexts=None, pretty_print=None,
        show_contexts=None
    ):
        """Generate a JSON report of coverage results.

        Each module in `morfs` is included in the report.  `outfile` is the
        path to write the file to, "-" will write to stdout.

        See :meth:`report` for other arguments.

        Returns a float, the total percentage covered.

        .. versionadded:: 5.0

        """
        with override_config(self,
            ignore_errors=ignore_errors, report_omit=omit, report_include=include,
            json_output=outfile, report_contexts=contexts, json_pretty_print=pretty_print,
            json_show_contexts=show_contexts
        ):
            return render_report(self.config.json_output, JsonReporter(self), morfs, self._message)

    def sys_info(self):
        """Return a list of (key, value) pairs showing internal information."""

        import coverage as covmod

        self._init()
        self._post_init()

        def plugin_info(plugins):
            """Make an entry for the sys_info from a list of plug-ins."""
            entries = []
            for plugin in plugins:
                entry = plugin._coverage_plugin_name
                if not plugin._coverage_enabled:
                    entry += " (disabled)"
                entries.append(entry)
            return entries

        info = [
            ('coverage_version', covmod.__version__),
            ('coverage_module', covmod.__file__),
            ('tracer', self._collector.tracer_name() if self._collector else "-none-"),
            ('CTracer', 'available' if CTracer else "unavailable"),
            ('plugins.file_tracers', plugin_info(self._plugins.file_tracers)),
            ('plugins.configurers', plugin_info(self._plugins.configurers)),
            ('plugins.context_switchers', plugin_info(self._plugins.context_switchers)),
            ('configs_attempted', self.config.attempted_config_files),
            ('configs_read', self.config.config_files_read),
            ('config_file', self.config.config_file),
            ('config_contents',
                repr(self.config._config_contents)
                if self.config._config_contents
                else '-none-'
            ),
            ('data_file', self._data.data_filename() if self._data is not None else "-none-"),
            ('python', sys.version.replace('\n', '')),
            ('platform', platform.platform()),
            ('implementation', platform.python_implementation()),
            ('executable', sys.executable),
            ('def_encoding', sys.getdefaultencoding()),
            ('fs_encoding', sys.getfilesystemencoding()),
            ('pid', os.getpid()),
            ('cwd', os.getcwd()),
            ('path', sys.path),
            ('environment', human_sorted(
                f"{k} = {v}"
                for k, v in os.environ.items()
                if (
                    any(slug in k for slug in ("COV", "PY")) or
                    (k in ("HOME", "TEMP", "TMP"))
                )
            )),
            ('command_line', " ".join(getattr(sys, 'argv', ['-none-']))),
            ]

        if self._inorout:
            info.extend(self._inorout.sys_info())

        info.extend(CoverageData.sys_info())

        return info


# Mega debugging...
# $set_env.py: COVERAGE_DEBUG_CALLS - Lots and lots of output about calls to Coverage.
if int(os.environ.get("COVERAGE_DEBUG_CALLS", 0)):              # pragma: debugging
    from coverage.debug import decorate_methods, show_calls

    Coverage = decorate_methods(show_calls(show_args=True), butnot=['get_data'])(Coverage)


def process_startup():
    """Call this at Python start-up to perhaps measure coverage.

    If the environment variable COVERAGE_PROCESS_START is defined, coverage
    measurement is started.  The value of the variable is the config file
    to use.

    There are two ways to configure your Python installation to invoke this
    function when Python starts:

    #. Create or append to sitecustomize.py to add these lines::

        import coverage
        coverage.process_startup()

    #. Create a .pth file in your Python installation containing::

        import coverage; coverage.process_startup()

    Returns the :class:`Coverage` instance that was started, or None if it was
    not started by this call.

    """
    cps = os.environ.get("COVERAGE_PROCESS_START")
    if not cps:
        # No request for coverage, nothing to do.
        return None

    # This function can be called more than once in a process. This happens
    # because some virtualenv configurations make the same directory visible
    # twice in sys.path.  This means that the .pth file will be found twice,
    # and executed twice, executing this function twice.  We set a global
    # flag (an attribute on this function) to indicate that coverage.py has
    # already been started, so we can avoid doing it twice.
    #
    # https://github.com/nedbat/coveragepy/issues/340 has more details.

    if hasattr(process_startup, "coverage"):
        # We've annotated this function before, so we must have already
        # started coverage.py in this process.  Nothing to do.
        return None

    cov = Coverage(config_file=cps)
    process_startup.coverage = cov
    cov._warn_no_data = False
    cov._warn_unimported_source = False
    cov._warn_preimported_source = False
    cov._auto_save = True
    cov.start()

    return cov


def _prevent_sub_process_measurement():
    """Stop any subprocess auto-measurement from writing data."""
    auto_created_coverage = getattr(process_startup, "coverage", None)
    if auto_created_coverage is not None:
        auto_created_coverage._auto_save = False
