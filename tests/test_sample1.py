import re

import pytest
from sphinx.testing.util import (
    assert_re_search,
    path,
)

# sphinx_intl = pytest.mark.sphinx(
sphinx_ext = pytest.mark.sphinx(
    testroot="intl",
    confoverrides={
        "language": "xx",
        "locale_dirs": ["."],
        "gettext_compact": False,
        "extensions": ["sphinxext.showorig"],
    },
)


@pytest.fixture
def sample_fixture():
    return "output from sample_fixture"


def test_dummy(sample_fixture):
    assert sample_fixture == "output from sample_fixture"


@sphinx_ext
@pytest.mark.sphinx("pseudoxml")
@pytest.mark.test_params(shared_result="test_ext_pseudoxml")
def test_generate_pxml(app):
    # --- only test for generation without failure
    # expect no error by build
    app.build()


def read_text_from_sphinx_path(path_: path):
    from sphinx import version_info as sphinx_version_info

    if sphinx_version_info < (3,):
        return path_.text()
    else:
        return path_.read_text()


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_meta(app):
    app.build()
    # --- test for meta
    result = read_text_from_sphinx_path(app.outdir / "index.html")
    expected_expr = '<meta content="TESTDATA FOR I18N" name="description" />'
    assert expected_expr in result
    expected_expr = '<meta content="I18N, SPHINX, MARKUP" name="keywords" />'
    assert expected_expr in result
    expected_expr = (
        '<p class="caption"><span class="caption-text">HIDDEN TOC</span></p>'
    )
    assert expected_expr in result


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_footnotes(app):
    app.build()
    # --- test for #955 cant-build-html-with-footnotes-when-using
    # expect no error by build
    read_text_from_sphinx_path(app.outdir / "footnote.html")


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_undefined_refs(app):
    app.build()
    # --- links to undefined reference
    result = read_text_from_sphinx_path(app.outdir / "refs_inconsistency.html")

    expected_expr = (
        '<a class="reference external" '
        'href="http://www.example.com">reference</a>'
    )
    assert len(re.findall(expected_expr, result)) == 2

    expected_expr = (
        '<a class="reference internal" ' 'href="#reference">reference</a>'
    )
    assert len(re.findall(expected_expr, result)) == 0

    expected_expr = (
        '<a class="reference internal" '
        'href="#i18n-with-refs-inconsistency">I18N WITH '
        "REFS INCONSISTENCY</a>"
    )
    assert len(re.findall(expected_expr, result)) == 1


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_index_entries(app):
    app.build()
    # --- index entries: regression test for #976
    result = read_text_from_sphinx_path(app.outdir / "genindex.html")

    def wrap(tag, keyword):
        start_tag = "<%s[^>]*>" % tag
        end_tag = "</%s>" % tag
        return r"%s\s*%s\s*%s" % (start_tag, keyword, end_tag)

    def wrap_nest(parenttag, childtag, keyword):
        start_tag1 = "<%s[^>]*>" % parenttag
        start_tag2 = "<%s[^>]*>" % childtag
        return r"%s\s*%s\s*%s" % (start_tag1, keyword, start_tag2)

    expected_exprs = [
        wrap("a", "NEWSLETTER"),
        wrap("a", "MAILING LIST"),
        wrap("a", "RECIPIENTS LIST"),
        wrap("a", "FIRST SECOND"),
        wrap("a", "SECOND THIRD"),
        wrap("a", "THIRD, FIRST"),
        wrap_nest("li", "ul", "ENTRY"),
        wrap_nest("li", "ul", "SEE"),
        wrap("a", "MODULE"),
        wrap("a", "KEYWORD"),
        wrap("a", "OPERATOR"),
        wrap("a", "OBJECT"),
        wrap("a", "EXCEPTION"),
        wrap("a", "STATEMENT"),
        wrap("a", "BUILTIN"),
    ]
    for expr in expected_exprs:
        assert_re_search(expr, result, re.M)


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_versionchanges(app):
    app.build()
    # --- versionchanges
    result = read_text_from_sphinx_path(app.outdir / "versionchange.html")

    def get_content(result, name):
        matched = re.search(
            r'<div class="%s">\n*(.*?)</div>' % name, result, re.DOTALL
        )
        if matched:
            return matched.group(1)
        else:
            return ""

    # In sphinx.addnodes.versionmodified node (used by "versionadded",
    # "versionmodified", and "deprecated" directives), first paragraph
    # is regarded as not translatable, while content after first para
    # is regarded as translatable.
    # See sphinx.domains.changeset module source code
    # (sphinx/domains/changeset.py file in sphinx source code)
    expect1 = (
        """<p><span class="versionmodified deprecated">"""
        """Deprecated since version 1.0: </span>"""
        """THIS IS THE <em>FIRST</em> PARAGRAPH OF DEPRECATED.</p>\n"""
        """<p class="trans-translated-text">"""
        """THIS IS THE <em>SECOND</em> PARAGRAPH OF DEPRECATED."""
        """<span class="trans-original-text">\n"""
        """This is the *second* paragraph of deprecated.</span></p>\n"""
    )
    matched_content = get_content(result, "deprecated")
    assert expect1 == matched_content

    expect2 = (
        """<p><span class="versionmodified added">"""
        """New in version 1.0: </span>"""
        """THIS IS THE <em>FIRST</em> PARAGRAPH OF VERSIONADDED.</p>\n"""
    )
    matched_content = get_content(result, "versionadded")
    assert expect2 == matched_content

    expect3 = (
        """<p><span class="versionmodified changed">"""
        """Changed in version 1.0: </span>"""
        """THIS IS THE <em>FIRST</em> PARAGRAPH OF VERSIONCHANGED.</p>\n"""
    )
    matched_content = get_content(result, "versionchanged")
    assert expect3 == matched_content


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_docfields(app):
    app.build()
    # --- docfields
    # expect no error by build
    read_text_from_sphinx_path(app.outdir / "docfields.html")


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_template(app):
    app.build()
    # --- gettext template
    result = read_text_from_sphinx_path(app.outdir / "contents.html")
    assert "WELCOME" in result
    assert "SPHINX 2013.120" in result


@sphinx_ext
@pytest.mark.sphinx("html")
@pytest.mark.test_params(shared_result="test_ext_basic")
def test_html_rebuild_mo(app):
    app.build()
    # --- rebuild by .mo mtime
    app.builder.build_update()
    app.env.find_files(app.config, app.builder)
    _, updated, _ = app.env.get_outdated_files(config_changed=False)
    assert len(updated) == 0

    mtime = (app.srcdir / "xx" / "LC_MESSAGES" / "bom.mo").stat().st_mtime
    (app.srcdir / "xx" / "LC_MESSAGES" / "bom.mo").utime(
        (mtime + 5, mtime + 5)
    )
    app.env.find_files(app.config, app.builder)
    _, updated, _ = app.env.get_outdated_files(config_changed=False)
    assert len(updated) == 1
