from kkblog import markdown
from datetime import datetime


def test_parse_article(tmpdir):
    meta, html = markdown.parse_article("tests/data/测试/论单元测试的重要性.md")
    expect_meta = {
        "catalog": "测试",
        "article": "论单元测试的重要性",
        "date": datetime(2016, 4, 5),
        "title": "论单元测试的重要性",
        "tags": ["测试", "Python"],
        "summary": "介绍单元测试的重要性和测试的基本流程，介绍测试的要点和相关测试工具"
    }
    assert meta == expect_meta

    # meta not in content
    assert "title" not in html
    assert "date" not in html
    assert "tags" not in html
    assert "summary" not in html

    # content
    assert "<h1>论单元测试的重要性</h1>" in html
    assert "<h2>为什么要单元测试</h2>" in html
    assert "<p>测试让自己对代码有信心</p>" in html
    assert "h3" not in html
    assert "pre" in html
    assert """<span class="kn">import</span>""" in html
