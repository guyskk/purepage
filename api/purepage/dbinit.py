import rethinkdb as r

setups = [
    r.db_create("purepage"),
    r.table_create("user"),
    r.table_create("article"),
    r.table("user").index_create("email"),
    r.table("article").index_create("author"),
]
