from pathlib import Path
from refactor.target_resolver import AnalysisIndexTargetResolver

def test_resolver_fast_full_cache(tmp_path):
    p=tmp_path/"mod.py"; p.write_text("class Foo:\n    def bar(self): pass\n\ndef baz(): pass")
    AnalysisIndexTargetResolver.clear_cache()
    r_fast=AnalysisIndexTargetResolver(root=tmp_path, mode="fast")
    assert r_fast.resolve("Foo") is not None
    assert r_fast.resolve("Foo.bar") is not None
    assert r_fast.resolve("baz") is not None
    assert r_fast.resolve("pkg:Foo") is not None
    assert r_fast.resolve("unknown") is None
    AnalysisIndexTargetResolver.clear_cache()
    r_full=AnalysisIndexTargetResolver(root=tmp_path, mode="full")
    assert r_full.resolve("Foo") is not None
    r_fast2=AnalysisIndexTargetResolver(root=tmp_path, mode="full")
    assert r_fast2.resolve("Foo")==r_full.resolve("Foo")

def test_clear_cache():
    AnalysisIndexTargetResolver.clear_cache()
    assert len(AnalysisIndexTargetResolver._GLOBAL_CACHE)==0
