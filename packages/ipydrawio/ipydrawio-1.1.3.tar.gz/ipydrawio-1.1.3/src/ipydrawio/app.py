"""CLI for ipydrawio"""

# Copyright 2021 ipydrawio contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path

import traitlets as T
from jupyter_core.application import JupyterApp, base_aliases, base_flags

from ._version import __version__

try:
    # the clean command isn't _critical_
    from .clean import MX_CLEAN_ATTRS, clean_drawio_file
except ImportError:  # pragma: no cover
    clean_drawio_file = None


class BaseApp(JupyterApp):
    version = __version__

    @property
    def description(self):  # pragma: no cover
        return self.__doc__.splitlines()[0].strip()


if clean_drawio_file:

    class CleanApp(BaseApp):
        """clean drawio files"""

        dio_files = T.Tuple()
        pretty = T.Bool(True, help="pretty-print the XML").tag(config=True)
        mx_attrs = T.Tuple(MX_CLEAN_ATTRS, help="attributes to clean").tag(config=True)
        indent = T.Int(2, help="if pretty-printing, the indent level").tag(config=True)
        tabs = T.Bool(False, help="indent with tabs instead of spaces").tag(config=True)

        flags = dict(
            **base_flags,
            **{
                "no-pretty": (
                    {"CleanApp": {"pretty": False}},
                    "Do not pretty-print the XML",
                ),
                "tabs": (
                    {"CleanApp": {"tabs": True}},
                    "Indent with tabs instead of spaces",
                ),
            }
        )
        aliases = dict(
            **base_aliases,
            **{"mx-attrs": "CleanApp.mx_attrs", "indent": "CleanApp.indent"}
        )

        def parse_command_line(self, argv=None):
            super().parse_command_line(argv)
            self.dio_files = [Path(p).resolve() for p in self.extra_args]

        def start(self):
            for path in self.dio_files:
                clean_drawio_file(
                    path,
                    pretty=self.pretty,
                    mx_attrs=self.mx_attrs,
                    indent=self.indent,
                    tabs=self.tabs,
                )


class IPyDrawioApp(BaseApp):
    """ipydrawio utilities"""

    name = "ipydrawio"
    subcommands = dict()

    if clean_drawio_file:
        subcommands["clean"] = (CleanApp, CleanApp.__doc__.splitlines()[0])


main = launch_instance = IPyDrawioApp.launch_instance

if __name__ == "__main__":  # pragma: no cover
    main()
