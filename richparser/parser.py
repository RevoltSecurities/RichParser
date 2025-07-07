from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
from rich.align import Align
import argparse
import sys

class RichParser:
    def __init__(self, description=""):
        self.console = Console()
        self.parser = argparse.ArgumentParser(add_help=False, usage=argparse.SUPPRESS)
        self.sections = {}
        self.description = description
        self.color_enabled = True
        self.subcommands = {}

        # Registering as  global default flags
        self._register_default_flag(self.parser, "-h", "--help", help="show this help message and exit.")
        self._register_default_flag(self.parser, "--plain", help="display the help message in plain text")

    def _register_default_flag(self, parser, *args, help):
        parser.add_argument(*args, action='store_true', help=help)
        section = "[DEFAULT FLAGS]"
        flag_names = ', '.join(arg for arg in args)
        self.sections.setdefault(section, []).append((flag_names, help))

    def add_argument(self, section=None, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)
        flag_names = ', '.join(arg for arg in args if arg.startswith("-"))
        help_text = kwargs.get('help', '')
        section = f"[{section.strip().upper()}]" if section else "[FLAGS]"
        self.sections.setdefault(section, []).append((flag_names, help_text))

    def add_subcommand(self, name, description):
        subparser = argparse.ArgumentParser(prog=name, add_help=False, usage=argparse.SUPPRESS)
        section_dict = {}

        # Adding as default flags to subcommand
        self._register_sub_default_flag(subparser, section_dict, "-h", "--help", help="show this help message and exit.")
        self._register_sub_default_flag(subparser, section_dict, "--plain", help="display the help message in plain text")

        self.subcommands[name] = {
            "description": description,
            "parser": subparser,
            "sections": section_dict
        }
        return subparser, section_dict

    def _register_sub_default_flag(self, parser, section_dict, *args, help):
        parser.add_argument(*args, action='store_true', help=help)
        section = "[DEFAULT FLAGS]"
        flag_names = ', '.join(args)
        section_dict.setdefault(section, []).append((flag_names, help))

    def add_subcommand_argument(self, cmd, section=None, *args, **kwargs):
        parser = self.subcommands[cmd]["parser"]
        section_dict = self.subcommands[cmd]["sections"]
        parser.add_argument(*args, **kwargs)
        flag_names = ', '.join(arg for arg in args if arg.startswith("-"))
        help_text = kwargs.get('help', '')
        section = f"[{section.strip().upper()}]" if section else "[FLAGS]"
        section_dict.setdefault(section, []).append((flag_names, help_text))

    def parse_args(self):
        if len(sys.argv) > 1 and sys.argv[1] in self.subcommands:
            cmd = sys.argv[1]
            args = self.subcommands[cmd]["parser"].parse_args(sys.argv[2:])
            if getattr(args, 'plain', False):
                self.color_enabled = False
            if getattr(args, 'help', False):
                self.display_subcommand_help(cmd)
                sys.exit(0)
            setattr(args, "mode", cmd)
            return args
        else:
            args = self.parser.parse_args()
            if getattr(args, 'plain', False):
                self.color_enabled = False
            if getattr(args, 'help', False):
                self.display_help()
                sys.exit(0)
            return args

    def display_help(self):
        if self.color_enabled:
            desc = Text(self.description, style="bold white", justify="center")
            self.console.print(Align.center(desc))
        else:
            self.console.print(self.description.center(self.console.width))
        self.console.print()

        if self.subcommands:
            if self.color_enabled:
                table = Table(title="Available Modes", box=box.ROUNDED, show_lines=True,
                              border_style="#4682B4", header_style="bold dodger_blue1")
                table.add_column("Mode", style="bold white")
                table.add_column("Description", style="bold white")
            else:
                table = Table(title="Available Modes\n", box=None)
                table.add_column("Mode")
                table.add_column("Description")

            for name, data in self.subcommands.items():
                table.add_row(name, data["description"])
            self.console.print(table)
            self.console.print()

        for section, options in self.sections.items():
            self._print_table_section(section, ["Flag", "Description"], options)

    def display_subcommand_help(self, cmd):
        sub = self.subcommands[cmd]
        if self.color_enabled:
            desc = Text(f"{cmd} - {sub['description']}", style="bold white", justify="center")
            self.console.print(Align.center(desc))
        else:
            self.console.print(f"{cmd} - {sub['description']}".center(self.console.width))
        self.console.print()

        for section, options in sub["sections"].items():
            self._print_table_section(section, ["Flag", "Description"], options)

    def _print_table_section(self, header, columns, rows):
        if self.color_enabled:
            section_name = header.strip("[]")
            styled_header = (
                Text("[", style="bold white") +
                Text(section_name, style="bold dodger_blue1") +
                Text("]", style="bold white")
            )
            self.console.print(styled_header)

            table = Table(
                box=box.ROUNDED,
                show_header=True,
                header_style="bold dodger_blue1",
                border_style="#4682B4",
                show_edge=True,
                pad_edge=True,
                show_lines=True
            )
            for col in columns:
                table.add_column(col, style="bold white")
            for row in rows:
                table.add_row(*[Text(cell, style="white") for cell in row])
        else:
            self.console.print(f"{header}:")
            table = Table(box=None, show_header=True, show_edge=False)
            for col in columns:
                table.add_column(col)
            for row in rows:
                table.add_row(*row)

        self.console.print(table)
        self.console.print()