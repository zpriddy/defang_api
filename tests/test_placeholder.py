# from src.defang_api.servelocal import DefangPostResource, RefangPostResource, ResponseObject, defang_post_json, defang_get
from src.defang_api.helpers.helpers import (
    ResponseObject,
    defang_post_json,
    defang_get,
    refang_post_json,
)

DEFANGED = "defanged"
DEFANGED_COLON = "colon"
DEFANGED_DOTS = "dots"
DEFANGED_DOTS_COLON = "dots_colon"


TEST_CASES = {
    "example.org": {
        DEFANGED: "example[.]org",
        DEFANGED_DOTS: "example[.]org",
        DEFANGED_COLON: "example[.]org",
        DEFANGED_DOTS_COLON: "example[.]org",
    },
    "http://example.org": {
        DEFANGED: "hXXp://example[.]org",
        DEFANGED_DOTS: "hXXp://example[.]org",
        DEFANGED_COLON: "hXXp[:]//example[.]org",
        DEFANGED_DOTS_COLON: "hXXp[:]//example[.]org",
    },
    "http://1.22.33.111/path": {
        DEFANGED: "hXXp://1[.]22.33.111/path",
        DEFANGED_DOTS: "hXXp://1[.]22[.]33[.]111/path",
        DEFANGED_COLON: "hXXp[:]//1[.]22.33.111/path",
        DEFANGED_DOTS_COLON: "hXXp[:]//1[.]22[.]33[.]111/path",
    },
    "HTTP://EVIL-guy.badguy.NET": {
        DEFANGED: "hXXp://EVIL-guy.badguy[.]NET",
        DEFANGED_DOTS: "hXXp://EVIL-guy[.]badguy[.]NET",
        DEFANGED_COLON: "hXXp[:]//EVIL-guy.badguy[.]NET",
        DEFANGED_DOTS_COLON: "hXXp[:]//EVIL-guy[.]badguy[.]NET",
    },
    "ssh://foobar.example.org/": {
        DEFANGED: "(ssh)://foobar.example[.]org/",
        DEFANGED_DOTS: "(ssh)://foobar[.]example[.]org/",
        DEFANGED_COLON: "(ssh)[:]//foobar.example[.]org/",
        DEFANGED_DOTS_COLON: "(ssh)[:]//foobar[.]example[.]org/",
    },
    "ftp://foo-bar.example.org": {
        DEFANGED: "fXp://foo-bar.example[.]org",
        DEFANGED_DOTS: "fXp://foo-bar[.]example[.]org",
        DEFANGED_COLON: "fXp[:]//foo-bar.example[.]org",
        DEFANGED_DOTS_COLON: "fXp[:]//foo-bar[.]example[.]org",
    },
    "http://sub.domain.org/path/to?bad=stuff": {
        DEFANGED: "hXXp://sub.domain[.]org/path/to?bad=stuff",
        DEFANGED_DOTS: "hXXp://sub[.]domain[.]org/path/to?bad=stuff",
        DEFANGED_COLON: "hXXp[:]//sub.domain[.]org/path/to?bad=stuff",
        DEFANGED_DOTS_COLON: "hXXp[:]//sub[.]domain[.]org/path/to?bad=stuff",
    },
    "ftp://user:pass@example.com/dir": {
        DEFANGED: "fXp://user:pass@example[.]com/dir",
        DEFANGED_DOTS: "fXp://user:pass@example[.]com/dir",
        DEFANGED_COLON: "fXp[:]//user:pass@example[.]com/dir",
        DEFANGED_DOTS_COLON: "fXp[:]//user:pass@example[.]com/dir",
    },
    "ftp://user:pass@127.13.1.2/dir": {
        DEFANGED: "fXp://user:pass@127[.]13.1.2/dir",
        DEFANGED_DOTS: "fXp://user:pass@127[.]13[.]1[.]2/dir",
        DEFANGED_COLON: "fXp[:]//user:pass@127[.]13.1.2/dir",
        DEFANGED_DOTS_COLON: "fXp[:]//user:pass@127[.]13[.]1[.]2/dir",
    },
    "twitter://FooBar": {
        DEFANGED: "(twitter)://FooBar",
        DEFANGED_DOTS: "(twitter)://FooBar",
        DEFANGED_COLON: "(twitter)[:]//FooBar",
        DEFANGED_DOTS_COLON: "(twitter)[:]//FooBar",
    },
    "twitter://FooBar?go=yes": {
        DEFANGED: "(twitter)://FooBar?go=yes",
        DEFANGED_DOTS: "(twitter)://FooBar?go=yes",
        DEFANGED_COLON: "(twitter)[:]//FooBar?go=yes",
        DEFANGED_DOTS_COLON: "(twitter)[:]//FooBar?go=yes",
    },
    "twitter://FooBar?next=http://evil.com?execute=yes": {
        DEFANGED: "(twitter)://FooBar?next=hXXp://evil[.]com?execute=yes",
        DEFANGED_DOTS: "(twitter)://FooBar?next=hXXp://evil[.]com?execute=yes",
        DEFANGED_COLON: "(twitter)[:]//FooBar?next=hXXp[:]//evil[.]com?execute=yes",
        DEFANGED_DOTS_COLON: "(twitter)[:]//FooBar?next=hXXp[:]//evil[.]com?execute=yes",
    },
    "10.10.10.1/myFile": {
        DEFANGED: "10[.]10.10.1/myFile",
        DEFANGED_DOTS: "10[.]10[.]10[.]1/myFile",
        DEFANGED_COLON: "10[.]10.10.1/myFile",
        DEFANGED_DOTS_COLON: "10[.]10[.]10[.]1/myFile",
    },
    "test": {
        DEFANGED: "test",
        DEFANGED_DOTS: "test",
        DEFANGED_COLON: "test",
        DEFANGED_DOTS_COLON: "test",
    },
    "test space": {
        DEFANGED: "test space",
        DEFANGED_DOTS: "test space",
        DEFANGED_COLON: "test space",
        DEFANGED_DOTS_COLON: "test space",
    },
    "server/": {
        DEFANGED: "server[/]",
        DEFANGED_DOTS: "server[/]",
        DEFANGED_COLON: "server[/]",
        DEFANGED_DOTS_COLON: "server[/]",
    },
    "http://test": {
        DEFANGED: "hXXp://test",
        DEFANGED_DOTS: "hXXp://test",
        DEFANGED_COLON: "hXXp[:]//test",
        DEFANGED_DOTS_COLON: "hXXp[:]//test",
    },
    "http://foo?next=http://evil.com": {
        DEFANGED: "hXXp://foo?next=hXXp://evil[.]com",
        DEFANGED_DOTS: "hXXp://foo?next=hXXp://evil[.]com",
        DEFANGED_COLON: "hXXp[:]//foo?next=hXXp[:]//evil[.]com",
        DEFANGED_DOTS_COLON: "hXXp[:]//foo?next=hXXp[:]//evil[.]com",
    },
    " http://foo?next=http://evil.com": {
        DEFANGED: "hXXp://foo?next=hXXp://evil[.]com",
        DEFANGED_DOTS: "hXXp://foo?next=hXXp://evil[.]com",
        DEFANGED_COLON: "hXXp[:]//foo?next=hXXp[:]//evil[.]com",
        DEFANGED_DOTS_COLON: "hXXp[:]//foo?next=hXXp[:]//evil[.]com",
    },
    "http://foo.com?next/http://evil.com": {
        DEFANGED: "hXXp://foo[.]com?next[/]hXXp://evil[.]com",
        DEFANGED_DOTS: "hXXp://foo[.]com?next[/]hXXp://evil[.]com",
        DEFANGED_COLON: "hXXp[:]//foo[.]com?next[/]hXXp[:]//evil[.]com",
        DEFANGED_DOTS_COLON: "hXXp[:]//foo[.]com?next[/]hXXp[:]//evil[.]com",
    },
}


import pytest


class MockResponseObject(ResponseObject):
    output = None
    errors = None
    url = None

    @property
    def response(self):
        return {"output": self.output, "error": self.errors}


def test_defang(monkeypatch):
    for fqdn, cases in TEST_CASES.items():
        defang_resouce = MockResponseObject()
        defang_resouce.args = {"url": fqdn, "dots": False, "colons": False}
        assert defang_post_json(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED],
        }
        assert defang_get(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED],
        }


def test_defang_dots(monkeypatch):
    for fqdn, cases in TEST_CASES.items():
        defang_resouce = MockResponseObject()
        defang_resouce.args = {"url": fqdn, "dots": True, "colons": False}
        assert defang_post_json(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED_DOTS],
        }
        assert defang_get(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED],
        }


def test_defang_colons(monkeypatch):
    for fqdn, cases in TEST_CASES.items():
        defang_resouce = MockResponseObject()
        defang_resouce.args = {"url": fqdn, "dots": False, "colons": True}
        assert defang_post_json(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED_COLON],
        }
        assert defang_get(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED],
        }


def test_defang_dots_colons(monkeypatch):
    for fqdn, cases in TEST_CASES.items():
        defang_resouce = MockResponseObject()
        defang_resouce.args = {"url": fqdn, "dots": True, "colons": True}
        assert defang_post_json(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED_DOTS_COLON],
        }
        assert defang_get(defang_resouce) == {
            "error": [],
            "output": cases[DEFANGED],
        }


def test_refang(monkeypatch):
    for fqdn, cases in TEST_CASES.items():
        for _, defanged in cases.items():
            defang_resouce = MockResponseObject()
            defang_resouce.args = {"url": defanged}
            output = refang_post_json(defang_resouce)
            output["output"] = output["output"].lower()
            assert output == {"error": [], "output": fqdn.lower().strip()}
