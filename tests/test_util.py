from purepage import util


def test_read_articles():
    articles = list(util.read_articles("tests/data"))
    assert len(articles) == 1
    assert any(meta["article"] == "论单元测试的重要性" for meta, html in articles)
    assert any(meta["catalog"] == "测试" for meta, html in articles)
    assert any("论单元测试的重要性" in html for meta, html in articles)


def test_read_repo(tmpdir):
    path = tmpdir.dirpath('data').strpath
    url = 'https://github.com/guyskk/purepage-article.git'
    # test git clone
    articles = list(util.read_repo(url, path))
    assert any(meta["article"] == "python2编码问题" for meta, html in articles)
    assert any(meta["catalog"] == "2015" for meta, html in articles)
    # test git pull
    articles = list(util.read_repo(url, path))
    assert any(meta["article"] == "python2编码问题" for meta, html in articles)
    assert any(meta["catalog"] == "2015" for meta, html in articles)
