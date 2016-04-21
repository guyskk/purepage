from kkblog import util


def test_read_articles():
    articles = list(util.read_articles("tests/data"))
    assert len(articles) == 1
    assert any(meta["article"] == "论单元测试的重要性" for meta, html in articles)
    assert any(meta["catalog"] == "测试" for meta, html in articles)
    assert any("论单元测试的重要性" in html for meta, html in articles)
