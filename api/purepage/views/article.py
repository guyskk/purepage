import arrow
from purepage.ext import r, db, g, abort


class Article:
    """
    文章

    $shared:
        article:
            id?str: ID
            catalog?str: 目录
            name?str: 名称
            user:
                id?str: 用户ID
                username?str: 用户名
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
            name?str: 名称
            title?str: 标题
            summary?str: 摘要
            tags:
              - str
            content?str: 内容
        $output:
            id?str: ID
        """
        resp = db.run(r.table("article").insert({
            "catalog": catalog,
            "name": name,
            "user": {
                "id": g.user["id"],
                "username": g.user["username"],
            },
            "title": title,
            "summary": summary,
            "tags": tags,
            "content": content,
            "date_create": arrow.utcnow().datetime,
            "date_modify": arrow.utcnow().datetime
        }))
        return {"id": resp["generated_keys"][0]}

    def put(self, id, catalog, name, title, summary, tags, content):
        """
        修改文章

        $input:
            id?str: ID
            catalog?str: 目录
            name?str: 名称
            meta:
                title?str: 标题
                summary?str: 摘要
                tags:
                  - str
            content?str: 内容
        $output: @message
        """
        q = r.table("article").get(id)
        if not db.first(q):
            abort(400, "ArticleNotFound", "文章不存在")
        db.run(q.update({
            "catalog": catalog,
            "name": name,
            "title": title,
            "summary": summary,
            "tags": tags,
            "content": content,
            "date_modify": arrow.utcnow().datetime
        }))
        return {"message": "OK"}

    def get(self, id):
        """
        获取一篇文章

        $input:
            id?str: ID
        $output:
            $self@article&optional: 文章信息
            content?str: 内容
        """
        return db.run(r.table("article").get(id))

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

    def get_list(self, page, per_page, username, catalog, tag):
        """
        获取作者文章列表，结果按时间倒序排序

        $input:
            $self@pagging: 分页
            username?str: 用户名
            catalog?str&optional: 目录
            tag?str&optional: 标签
        $output:
            - @article
        """
        q = r.table("article").filter({"username": username})
        if catalog:
            q = q.filter({"catalog": catalog})
        if tag:
            q = q.filter(lambda x: tag in x["tags"])
        q = q.order_by(r.desc("date_modify"))
        return db.pagging(q, page, per_page)
