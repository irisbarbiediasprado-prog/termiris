import pytest
import sys
from pathlib import Path

lib_path = Path.home() / ".termiris/lib"
if str(lib_path) not in sys.path:
    sys.path.insert(0, str(lib_path))

from cli.metadata import extract_metadata

class TestExtractMetadata:
    def test_simple_hash(self):
        cmd, meta = extract_metadata(".file snapshot.ctx --hash=abc123")
        assert cmd == ".file snapshot.ctx"
        assert meta == {"hash": "abc123"}

    def test_multiple_metadata(self):
        cmd, meta = extract_metadata(".file snapshot.ctx --hash=abc123 --origin=delivery --retry=2")
        assert cmd == ".file snapshot.ctx"
        assert meta == {"hash": "abc123", "origin": "delivery", "retry": "2"}

    def test_no_metadata(self):
        cmd, meta = extract_metadata(".file snapshot.ctx")
        assert cmd == ".file snapshot.ctx"
        assert meta == {}

    def test_metadata_with_dashes(self):
        cmd, meta = extract_metadata(".file snapshot.ctx --my-key=value --foo-bar=baz")
        assert cmd == ".file snapshot.ctx"
        assert meta == {"my-key": "value", "foo-bar": "baz"}

    def test_metadata_with_path_values(self):
        cmd, meta = extract_metadata(".file /path/to/file --hash=abc/def/ghi")
        assert cmd == ".file /path/to/file"
        assert meta == {"hash": "abc/def/ghi"}

    def test_metadata_with_extra_spaces(self):
        cmd, meta = extract_metadata(".file   snapshot.ctx   --hash=abc123   --origin=delivery")
        assert cmd == ".file snapshot.ctx"
        assert meta == {"hash": "abc123", "origin": "delivery"}

    def test_metadata_after_positional_args(self):
        cmd, meta = extract_metadata(".file snapshot.ctx --hash=abc123 bar")
        assert cmd == ".file snapshot.ctx bar"
        assert meta == {"hash": "abc123"}

    def test_metadata_with_equals_in_value(self):
        cmd, meta = extract_metadata(".file snapshot.ctx --hash=abc=def")
        assert cmd == ".file snapshot.ctx"
        assert meta == {"hash": "abc=def"}

    def test_complex_command(self):
        cmd, meta = extract_metadata(".file snapshot.ctx --hash=abc123 --origin=delivery --retry=2 extra_arg")
        assert cmd == ".file snapshot.ctx extra_arg"
        assert meta == {"hash": "abc123", "origin": "delivery", "retry": "2"}
