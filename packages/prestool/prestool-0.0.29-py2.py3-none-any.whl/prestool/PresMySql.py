from .util import make_sql_str_util
import pymysql


class SqlStr:
    @staticmethod
    def select_sql_str(table, target=None, where=None, order=None, limit=None):
        return make_sql_str_util('select', table, select_target=target, where=where, order_by=order, limit=limit)

    @staticmethod
    def update_sql_str(table, target, where):
        return make_sql_str_util('update', table, update_target=target, where=where)

    @staticmethod
    def delete_sql_str(table, where):
        return make_sql_str_util('delete', table, where=where)

    @staticmethod
    def insert_sql_str(table, target):
        return make_sql_str_util('insert', table, insert_target=target)


class PresMySql(SqlStr):
    def __init__(self):
        self.mysql_host = ''
        self.mysql_port = 3306
        self.mysql_user = ''
        self.mysql_pwd = ''
        self.mysql_db_name = ''
        self.mysql_charset = 'utf8mb4'

    def connect(self):
        return pymysql.connect(
            host=self.mysql_host, user=self.mysql_user, password=self.mysql_pwd,
            db=self.mysql_db_name, charset=self.mysql_charset, port=self.mysql_port,
            cursorclass=pymysql.cursors.DictCursor)

    def exec_sql(self, sql_str, select=None):
        with self.connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql_str)
                if select == 'all':
                    return cursor.fetchall()
                elif select == 'one':
                    return cursor.fetchone()
            conn.commit()

    # 执行插入语句
    def to_insert(self, table, target):
        return self.exec_sql(self.insert_sql_str(table, target))

    # 执行删除语句
    def to_delete(self, table, where):
        return self.exec_sql(self.delete_sql_str(table, where))

    # 执行更新语句
    def to_update(self, table, target, where):
        return self.exec_sql(self.update_sql_str(table, target, where))

    # 查询符合条件的所有
    def to_query(self, table, target=None, where=None, order=None, limit=None, is_all=True):
        return self.exec_sql(
            self.select_sql_str(table, target, where, order, limit), 'all' if is_all else 'one')

    # 执行特殊查询
    def to_query_with_sql(self, sql_str, is_all=True):
        return self.exec_sql(sql_str, 'all' if is_all else 'one')
