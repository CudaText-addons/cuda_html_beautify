import sys
import os
import json
import cudatext
from .jsoncomment import JsonComment
from .html_format import *
from . import format_proc

format_proc.MSG = '[HTML Beautify] '
format_proc.INI = 'cuda_html_beautify.json'


def do_format(text):
    fn = format_proc.ini_filename()
    with open(fn) as f:
        parser = JsonComment(json)
        d = parser.loads(f.read())
    return do_html_format(text, d)

class Command:
    def config_global(self):
        format_proc.config_global()

    def config_local(self):
        format_proc.config_local()

    def run(self):
        format_proc.run(do_format)
