"""Admin API"""
import arrow
from purepage.ext import r, db, abort


class Admin:
    """
    后台管理

    $shared:
        user:
            id?str: ID
            username?str: 用户名
            role?str: 角色
            email?email&optional: 邮箱
            github?url&optional: Github地址
            avatar?url&default="http://purepage.org/static/avatar-default.png": 头像
            date_create?datetime&optional: 创建时间
            date_modify?datetime&optional: 修改时间
            timestamp?int&optional: 安全时间戳
            lastlogin_date?datetime&optional: 最近登录时间
            lastlogin_ip?ipv4&optional: 最近登录IP
            lastlogin_ua?str&optional: 最近登录设备UserAgent
    """  # noqa

    def put(self, id, username, role, email):
        """
        修改帐号信息

        $input:
            id?str: ID
            username?str: 用户名
            role?str: 角色
            email?email: 邮箱
        $output: @message
        """
        if role == "root":
            abort(403, "PermissionDeny", "不能设为root帐号")
        db.run(
            r.table("user").get(id).update({
                "username": username,
                "role": role,
                "email": email,
                "date_modify": arrow.utcnow().datetime,
                "timestamp": arrow.utcnow().timestamp
            })
        )
        return {"message": "OK"}

    def get(self, username):
        """
        查找帐号

        $input:
            username?str: 用户名或邮箱
        $output: @user&optional
        """
        q = r.or_(r.row["username"] == username, r.row["email"] == username)
        return db.first(r.table("user").filter(q))

    def get_list(self, page, per_page):
        """
        查看所有用户

        $input: @pagging
        $output:
            - @user
        """
        return db.pagging(r.table("user"), page, per_page)

    def delete(self, id):
        """
        删除帐号

        $input:
            id?str: ID
        $output: @message
        """
        user = db.run(r.table("user").get(id))
        if user and user["role"] == "root":
            abort(403, "PermissionDeny", "root帐号无法删除")
        db.run(r.table("user").get(id).delete())
        return {"message": "OK"}
