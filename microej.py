import os

from docutils import nodes
from pygments.style import Style
from pygments.token import (
    Comment,
    Error,
    Keyword,
    Literal,
    Generic,
    Operator,
    Name,
    Text,
    Whitespace,
)
from sphinx.util.docutils import ReferenceRole, SphinxRole


class MicroEJStyle(Style):

    """
    Pygments style for MircoEJ.

    Styles are defined here so that they affect both HTML and PDF output. For
    HTML output, a pygments.css is generated by Sphinx simply by using the
    MicroEJ Sphinx theme. For PDF output, the following option is required::

        pygments_style = 'microej.MicroEJStyle'

    This option also affects the HTML output, but is the same pygments class.
    """

    background_color = "#f8f8f8"
    default_style = ""

    styles = {
        Comment: "italic #48A23F",
        Comment.Hashbang: "italic #48A23F",
        Comment.Multiline: "italic #48A23F",
        Comment.Preproc: "italic #48A23F",
        Comment.PreprocFile: "italic #48A23F",
        Comment.Single: "italic #48A23F",
        Comment.Special: "italic #48A23F",

        Error: "#FF0000 bg:#f8f8f8",

        Keyword: "bold #cf4520",
        Keyword.Constant: "bold #cf4520",
        Keyword.Declaration: "bold #cf4520",
        Keyword.Namespace: "bold #cf4520",
        Keyword.Pseudo: "nobold",
        Keyword.Reserved: "bold #cf4520",
        Keyword.Type: "nobold #B00040",

        Literal: "#666666",
        Literal.Number: "#666666",
        Literal.String: "#ee502e",
        Literal.Number.Bin: "#666666",
        Literal.Number.Float: "#666666",
        Literal.Number.Hex: "#666666",
        Literal.Number.Integer: "#666666",
        Literal.Number.Oct: "#666666",
        Literal.String.Affix: "#ee502e",
        Literal.String.Backtick: "#ee502e",
        Literal.String.Char: "#ee502e",
        Literal.String.Delimiter: "#ee502e",
        Literal.String.Doc: "#ee502e italic",
        Literal.String.Double: "#ee502e",
        Literal.String.Escape: "#BB6622 bold",
        Literal.String.Heredoc: "#ee502e",
        Literal.String.Interpol: "#BB6688 bold",
        Literal.String.Other: "#cf4520",
        Literal.String.Regex: "#BB6688",
        Literal.String.Single: "#ee502e",
        Literal.String.Symbol: "#19177C",
        Literal.Number.Integer.Long: "#666666",

        Operator: "#666666",

        Generic.Deleted: "#A00000",
        Generic.Error: "#FF0000",
        Generic.Emph: "italic",
        Generic.Heading: "bold #000080",
        Generic.Inserted: "#00A000",
        Generic.Output: "#888",
        Generic.Prompt: "bold #008eaa",
        Generic.Strong: "bold",
        Generic.Subheading: "bold #800080",
        Generic.Traceback: "#04D",

        Name.Attribute: "#7D9029",
        Name.Builtin: "#cf4520",
        Name.Class: "#008eaa bold",
        Name.Constant: "#880000",
        Name.Decorator: "#AA22FF",
        Name.Entity: "#999999 bold",
        Name.Exception: "#D2413A bold",
        Name.Function: "#008eaa",
        Name.Label: "#A0A000",
        Name.Namespace: "#008eaa bold",
        Name.Tag: "#cf4520 bold",
        Name.Variable: "#19177C",
        Name.Builtin.Pseudo: "#cf4520",
        Name.Function.Magic: "#008eaa",
        Name.Variable.Class: "#19177C",
        Name.Variable.Global: "#19177C",
        Name.Variable.Instance: "#19177C",
        Name.Variable.Magic: "#19177C",

        Operator.Word: "#AA22FF bold",

        Text.Whitespace: "#bbbbbb",
        Whitespace: "#bbbbbb",
    }


class HttpCodeRef(ReferenceRole):

    """
    A custom role to format external links as code/literals.

    In the source docbook, links were styled as monospace text. This preserves
    that functionality and also makes the monospace text a clickable link. A
    normal URL link can also be used instead, but will be formatted with the
    default font.
    """

    def run(self):
        reference = nodes.reference('', '', internal=False, refuri=self.target)

        if self.has_explicit_title:
            reference += nodes.literal(self.title, self.title)
        else:
            reference += nodes.literal(self.target, self.target)

        return [reference], []


def can_build_independent_docs():
    return os.environ.get('MICROEJ_DOCSET', None) is not None


def get_project_name():
    """
    Set up the project name if we're building multiple docs from single source.

    This documentation project supports building multiple documentation sets
    from a common source. In order to enable this while building, define an
    environment variable ``MICROEJ_DOCSET`` -- this is the name of the path that
    you are building an independent documentation set for. For instance::

        MICROEJ_DOCSET=SandboexAppDevGuide make clean html

    This environment variable can also be defined on Read the Docs.
    """
    docset = os.environ.get('MICROEJ_DOCSET', None)
    if docset == 'SandboxedAppDevGuide':
        return 'Sandboxed Application Developer Guide'
    elif docset == 'StandaloneAppDevGuide':
        return 'Standalone Application Developer Guide'
    elif docset == 'ApplicationDeveloperGuide':
        return 'Application Developer Guide'
    elif docset == 'Landing':
        return 'MicroEJ Documentation'


def set_project_version(app, config):
    """
    Event listener to replace the project's release with changeset.

    This will only work on Read the Docs currently, it uses information passed
    into the project's build to obtain the commit id. This sets some additional
    variables in the tex output. See ``microej.sty`` for more information.
    """
    # We have to do this here, as Read the Docs appends this to the end of the
    # config file. It's not ready until we're in the build.
    commit_id = config.html_context.get('commit', None)
    if commit_id:
        config.release = f'Commit {commit_id}'
        config.latex_elements['preamble'] += (
            r'\renewcommand{\microejversion}{Revision \texttt ' + commit_id + "}"
        )


def setup(app):
    from docutils.parsers.rst import roles

    roles.register_local_role('http', HttpCodeRef())

    if can_build_independent_docs():
        docset = os.environ.get('MICROEJ_DOCSET', None)
        app.srcdir += '/' + docset

    app.connect('config-inited', set_project_version)

    return {
        'version': '1.0.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
