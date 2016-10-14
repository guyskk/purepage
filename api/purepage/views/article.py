import arrow
from purepage.ext import r, db, g, abort
from purepage.util import clear_empty


class Article:
    """
    文章

    $shared:
        article:
            id?str: ID
            author?str: 作者
            catalog?str: 目录
            name?str: 名称
            title?str: 标题
            summary?str: 摘要
            tags:
              - str&desc="标签"
    """

    def post(self, catalog, name, title, summary, tags, content):
        """
        创建文章

        $input:
            catalog?str: 目录
            title?str: 标题
            name?str&optional: 名称
            summary?str&optional: 摘要
            tags:
              - str
            content?str: 内容
        $output:
            id?str: ID
        """
        if not name:
            name = title[:32]
        if not summary:
            summary = content[:160]
        id = "/".join([g.user["id"], catalog, name])
        resp = db.run(r.table("article").insert({
            "id": id,
            "author": g.user["id"],
            "catalog": catalog,
            "name": name,
            "title": title,
            "summary": summary,
            "tags": tags,
            "content": content,
            "date_create": arrow.utcnow().datetime,
            "date_modify": arrow.utcnow().datetime
        }))
        if resp["errors"]:
            abort(400, "Conflict", "创建失败: %s" % resp["first_error"])
        return {"id": id}

    def put(self, id, **kwargs):
        """
        修改文章

        $input:
            id?str: ID
            title?str: 标题
            summary?str: 摘要
            tags:
              - str
            content?str: 内容
        $output: @message
        $error:
            400.ArticleNotFound: 文章不存在
            403.PermissionDeny: 只能修改自己的文章
        """
        q = r.table("article").get(id)
        art = db.run(q)
        if not art:
            abort(400, "ArticleNotFound", "文章不存在")
        if art["author"] != g.user["id"]:
            abort(403, "PermissionDeny", "只能修改自己的文章")
        db.run(q.update({
            **kwargs,
            "date_modify": arrow.utcnow().datetime
        }))
        return {"message": "OK"}

    def patch(self, id, **kwargs):
        """
        增量修改文章基本信息

        $input:
            id?str: ID
            title?str&optional: 标题
            summary?str&optional: 摘要
            tags:
              - &optional
              - str
            content?str&optional: 内容
        $output: @message
        $error:
            400.ArticleNotFound: 文章不存在
            403.PermissionDeny: 只能修改自己的文章
        """
        kwargs = clear_empty(kwargs)
        q = r.table("article").get(id)
        art = db.run(q)
        if not art:
            abort(400, "ArticleNotFound", "文章不存在")
        if art["author"] != g.user["id"]:
            abort(403, "PermissionDeny", "只能修改自己的文章")
        db.run(q.update({
            **kwargs,
            "date_modify": arrow.utcnow().datetime
        }))
        return {"message": "OK"}

    def get(self, id):
        """
        获取一篇文章

        $input:
            id?str: ID
        $output:
            $self@article: 文章信息
            content?str: 内容
        $error:
            404.NotFound: 文章不存在
        """
        article = db.run(r.table("article").get(id))
        if not article:
            abort(404, "NotFound", "文章不存在")
        return article

    def get_top(self, page, per_page, tag):
        """
        获取最新的文章，结果按时间倒序排序

        $input:
            $self@pagging: 分页
            tag?str&optional: 标签
        $output:
            - @article
        """
        q = r.table("article")
        if tag:
            q = q.filter(lambda x: tag in x["tags"])
        q = q.order_by(r.desc("date_modify"))
        return db.pagging(q, page, per_page)

    def get_list(self, page, per_page, author, catalog, tag):
        """
        获取作者文章列表，结果按时间倒序排序

        $input:
            $self@pagging: 分页
            author?str: 作者
            catalog?str&optional: 目录
            tag?str&optional: 标签
        $output:
            - @article
        """
        q = r.table("article").get_all(author, index="author")
        if catalog:
            q = q.filter({"catalog": catalog})
        if tag:
            q = q.filter(lambda x: x["tags"].contains(tag))
        q = q.order_by(r.desc("date_modify"))
        return db.pagging(q, page, per_page)
