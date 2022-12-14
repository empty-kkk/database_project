import pymysql  # 一种写好的库，可自己pip安装，类似的库很多可以自行查找

param = {
    'host': 'localhost',  # 本机
    'port': 3306,  # 端口号，一般mysql为3306
    'db': 'huawei',  # 数据库名
    'user': 'root',  # 登陆用户
    'password': 'chy211003',  # 登陆用户的密码
    'charset': 'utf8',  # 字符编码
}
db = pymysql.connect(**param)  # 建立连接对象
cursor = db.cursor()  # 使用cursor()方法创建一个游标对象cur（不理解没关系）

# 这是在执行sql语句，execute里面的为删除数据表的语句
cursor.execute("DROP TABLE IF EXISTS HUAWEI")

# 创建HUAWEI表的sql语句
create_table_sql = """CREATE TABLE HUAWEI (
         NAME  VARCHAR(20) NOT NULL,
         AGE INT )"""
cursor.execute(create_table_sql)

# 创建records表的sql语句
create_table_sql2 = """CREATE TABLE records (
         NAME  VARCHAR(20) NOT NULL,
         SUBJECT VARCHAR(20),SCORE INT )"""
cursor.execute(create_table_sql2)


def sql_insert(name, age):  # 插入信息
    sql_in = "INSERT INTO HUAWEI(NAME,AGE) VALUES (%s,%d);"
    sql_in = sql_in % (repr(name), int(age))
    print('语句：' + sql_in)
    try:
        cursor.execute(sql_in)
        db.commit()
        print("插入成功！")
    except:
        print('Fail!')
        db.rollback()


def sql_show_first():  # 返回查询的所有数据
    sql_show = "SELECT * FROM HUAWEI"
    try:
        # 执行SQL语句
        cursor.execute(sql_show)
        # 获取所有记录列表
        results = cursor.fetchone()
        print("first_item: \n" + "name: %s | age: %d" % (results[0], results[1]))
    except:
        print("无法获取数据")
    return results


def sql_show_all():  # 返回查询的第一个数据
    sql_show = "SELECT * FROM HUAWEI"
    try:
        # 执行SQL语句
        cursor.execute(sql_show)
        # 获取所有记录列表
        result = cursor.fetchall()
        print("all items:")
        for row in result:
            fname = row[0]
            fage = row[1]
            # 打印结果
            print("name: %s | age: %d" % (fname, fage))
    except:
        print("无法获取数据")
    return result


def sql_delete(name, age):
    if name != 'None':
        sql_del = 'DELETE FROM HUAWEI WHERE NAME= %s' % (name)
        try:
            cursor.execute(sql_del)
            db.commit()
            print("删除成功");
        except:
            print("删除失败");
    elif age >= 0:
        sql_del = 'DELETE FROM HUAWEI WHERE AGE= %d' % (age)
        try:
            cursor.execute(sql_del)
            db.commit()
            print("删除成功");
        except:
            print("删除失败");
    else:
        print("删除条目格式错误")


def sql_update(old_name, old_age, new_name, new_age):
    try:
        sql_upd_age = "UPDATE HUAWEI SET AGE = %d WHERE NAME = '%s' " % (new_age, old_name)
        sql_upd_name = "UPDATE HUAWEI SET NAME = '%s' WHERE AGE = %d " % (new_name, old_age)
        cursor.execute(sql_upd_name)
        cursor.execute(sql_upd_age)
        db.commit()
    except:
        print("更新失败！")


def Inner_Join(table1, table2):
    sql_inner_join = "select * from %s inner join %s on %s.name = %s.name;" % (table1, table2, table1, table2)
    try:
        cursor.execute(sql_inner_join)
        db.commit()
    except:
        print("内联失败！")


def Left_Join(table1, table2):
    sql_left_join = "select * from %s left outer join %s on %s.name=%s.name" % (table1, table2, table1, table2)
    try:
        cursor.execute(sql_left_join)
        db.commit()
    except:
        print("左连接失败！")


class connected_item:
    def __init__(self, host, port, database, user, passwd):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.passwd = passwd
        self.lock = 0  # 未占用


class queue:
    def __init__(self, count):
        self.queue = []
        self.count = count
        for i in range(0, count):
            host = input("输入主机名")
            port = int(input("输入端口号"))
            database = input("输入数据库名")
            user = input("输入用户名")
            passwd = int(input("输入密码"))
            queue.append(connected_item(host, port, database, user, passwd))

    def GetConnection(self):
        if self.count>0:
            first_connection = self.queue[0]
            self.queue[0].lock=1
            self.queue.pop()
            self.count-=1;
            return first_connection
        else:
            return 0

    def FreeConnection(self,used_connection):
        self.queue.append(used_connection)
        self.count+=1
        return self

    def ClearPool(self):
        for i in self.queue:
            del(i)
        self.count=0

if __name__ == '__main__':
    print(db)
    print(cursor)
    sql_insert('chy', '19')
    sql_insert('kk', '22')
    sql_insert('ll', '20')
    sql_show_first();
    sql_show_all();
    sql_delete("None", 22);
    sql_show_all();
    sql_update('ll', 20, 'll', 30)
    sql_show_all();
    db.close()
