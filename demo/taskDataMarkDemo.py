import random
import json
import pymysql
from elasticsearch import Elasticsearch


# 连接mysql
def mysqlClient():
    client = pymysql.connect(host='192.168.7.129', user='root', password='root', database='dmp')
    return client


# 连接ES
def esClient():
    client = Elasticsearch([{'host': '192.168.7.129', 'port': 9200}])
    return client


class taskDataMarkInfo:
    def __init__(self, uid, pid, taskTagId, name, originalImgUrl, taskBucketDataId):
        self._class = 'com.glasssix.dmp.task.common.entity.es.TaskDataMarkInfo'
        self.uid = uid
        self.pid = pid
        self.taskTagId = taskTagId
        self.name = name
        self.originalImgUrl = originalImgUrl
        self.taskBucketDataId = taskBucketDataId


if __name__ == "__main__":
    mark_info = '[{"id":"1648862520934912002","name":"分类5"},{"id":"1648862497455198209","name":"分类4"},{"id":"1648862464664129537","name":"分类3"},' \
                '{"id":"1648862442564341762","name":"分类2"},{"id":"1648862403607646209","name":"分类1"}]'
    data_list = json.loads(mark_info)
    # 连接ES
    esClient = esClient()
    # 连接mysql
    mysqlClient = mysqlClient()
    mysqlCursor = mysqlClient.cursor()
    taskId = 1644177678620078081
    sql = 'select * from task_bucket_data where task_id=%s'
    mysqlCursor.execute(sql, taskId)
    myResult = mysqlCursor.fetchall()
    for data in myResult:
        taskBucketDataId = data[0]
        originalImgUrl = data[6]
        # 组装对应的标注信息数据
        for mark in data_list:
            tagId = mark['id']
            tagName = mark['name']
            mark_data = taskDataMarkInfo(random.randint(10 ** 17, 10 ** 18 - 1), 0, tagId, tagName, originalImgUrl, taskBucketDataId)
            # 往ES写数据
            res = esClient.index(index='task_data_mark_info', body=json.dumps(mark_data.__dict__, ensure_ascii=False))
            # 更改任务标签的使用数量
            sql = 'update task_tag set number = number+1 where id = %s'
            mysqlCursor.execute(sql, tagId)
            mysqlClient.commit()
        # 更改任务数据的标注状态
        sql = 'update task_bucket_data set mark_type = 1 where id=%s'
        mysqlCursor.execute(sql, taskBucketDataId)
        mysqlClient.commit()
