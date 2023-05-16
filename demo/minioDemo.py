import os
from minio import Minio
from minio.error import S3Error
from datetime import timedelta
from minio.deleteobjects import DeleteObject


class Bucket(object):
    client = None
    policy = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetBucketLocation","s3:ListBucket"],"Resource":["arn:aws:s3:::%s"]},{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::%s/*"]}]}'

    def __new__(cls, *args, **kwargs):
        if not cls.client:
            cls.client = object.__new__(cls)
        return cls.client

    # 连接ES
    def __init__(self):
        self.client = Minio(endpoint="192.168.7.129:9001", access_key="minioadmin", secret_key="minioadmin", secure=False)

    # 判断桶是否存在
    def exists_bucket(self, bucket_name):
        return self.client.bucket_exists(bucket_name=bucket_name)

    # 创建桶 + 赋予策略
    def create_bucket(self, bucket_name: str, is_policy: bool = True):
        if self.exists_bucket(bucket_name=bucket_name):
            return True
        else:
            self.client.make_bucket(bucket_name=bucket_name)
        if is_policy:
            policy = self.policy % (bucket_name, bucket_name)
            self.client.set_bucket_policy(bucket_name=bucket_name, policy=policy)
        return True

    # 列出存储桶
    def get_bucket_list(self):
        buckets = self.client.list_buckets()
        bucket_list = []
        for bucket in buckets:
            bucket_list.append(
                {"bucket_name": bucket.name, "create_time": bucket.creation_date}
            )
        return bucket_list

    # 删除桶
    def remove_bucket(self, bucket_name):
        try:
            self.client.remove_bucket(bucket_name=bucket_name)
        except S3Error as e:
            print("[error]:", e)
            return False
        return True

    # 列出存储桶中所有对象
    def bucket_list_files(self, bucket_name, prefix):
        try:
            files_list = self.client.list_objects(bucket_name=bucket_name, prefix=prefix, recursive=True)
            for obj in files_list:
                print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
                      obj.etag, obj.size, obj.content_type)
        except S3Error as e:
            print("[error]:", e)

    # 列出桶存储策略
    def bucket_policy(self, bucket_name):
        try:
            policy = self.client.get_bucket_policy(bucket_name)
        except S3Error as e:
            print("[error]:", e)
            return None
        return policy

    # 从bucket 下载文件 + 写入指定文件
    def download_file(self, bucket_name, file, file_path, stream=1024 * 32):
        try:
            data = self.client.get_object(bucket_name, file)
            with open(file_path, "wb") as fp:
                for d in data.stream(stream):
                    fp.write(d)
        except S3Error as e:
            print("[error]:", e)

    # 下载保存文件保存本地
    def fget_file(self, bucket_name, file, file_path):
        self.client.fget_object(bucket_name, file, file_path)

    # 拷贝文件（最大支持5GB）
    def copy_file(self, bucket_name, file, file_path):
        self.client.copy_object(bucket_name, file, file_path)

    # 上传文件 + 写入
    def upload_file(self, bucket_name, file, file_path, content_type):
        try:
            with open(file_path, "rb") as file_data:
                file_stat = os.stat(file_path)
                self.client.put_object(bucket_name, file, file_data, file_stat.st_size, content_type=content_type)
        except S3Error as e:
            print("[error]:", e)

    # 上传文件
    def fput_file(self, bucket_name, file, file_path):
        try:
            self.client.fput_object(bucket_name, file, file_path)
        except S3Error as e:
            print("[error]:", e)

    # 获取文件元数据
    def stat_object(self, bucket_name, file):
        try:
            data = self.client.stat_object(bucket_name, file)
            print(data.bucket_name)
            print(data.object_name)
            print(data.last_modified)
            print(data.etag)
            print(data.size)
            print(data.metadata)
            print(data.content_type)
        except S3Error as e:
            print("[error]:", e)

    # 移除单个文件
    def remove_file(self, bucket_name, file):
        self.client.remove_object(bucket_name, file)

    # 删除多个文件
    def remove_files(self, bucket_name, file_list):
        delete_object_list = [DeleteObject(file) for file in file_list]
        for del_err in self.client.remove_objects(bucket_name, delete_object_list):
            print("del_err", del_err)

    # 获取文件访问链接,有效期为30分钟
    def presigned_get_object(self, bucket_name, file):
        return self.client.presigned_get_object(bucket_name, file, expires=timedelta(minutes=30))


if __name__ == '__main__':
    minioObj = Bucket()
    bucketName = 'wznf'
    minioObj.create_bucket(bucketName)
    filePrefix = '1/'
    filePath = 'C:/Users/Administrator/Pictures/uToolsWallpapers'
    for root, files in os.walk(filePath):
        for file in files:
            minioObj.fput_file(bucketName, filePrefix + file, os.path.join(root, file))
