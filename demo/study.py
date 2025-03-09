import requests
import time
from bs4 import BeautifulSoup
import random

# 第一个接口获取所有模拟考试记录
list_url = "https://www.xc985.net/BeegoEduApi/api/pc/getsimexamlist/28169468/51-02139/1"
base_url = "https://www.xc985.net/BeegoEduApi/api/pc/gensimexamreListBysrId/28169469/{simId}/0"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "content-type": "application/json;charset=utf-8",
    "Authorization": "Beego aHVhaGFuOmJlZWdvMjAxNQ==",
    "token": "1"
}


# 获得考试题相关id
def get_sim_ids():
    """获取所有模拟考试ID"""
    sim_records = []
    try:
        response = requests.get(list_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != 1:
            print(f"获取列表失败: {data.get('message')}")
            return []
        records = data.get("data", {}).get("SimExamStoreList", [])
        #遍历得到模拟考试ID和考试名称并返回列表
        for record in records:
            if record.get("simId"):
                sim_records.append((record.get("simId"), record.get("examName", "未知考试")))
        return sim_records
    except Exception as e:
        print(f"获取考试列表失败: {str(e)}")
        return []

# 下载考试题
def download_exam(sim_id, exam_name):
    """下载单个考试数据"""
    try:
        # 动态生成URL
        dynamic_url = base_url.format(simId=sim_id)
        print(f"正在下载：{exam_name}")

        response = requests.get(dynamic_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # 处理数据
        exam_info = data.get("data", {}).get("SimExamStore", {})
        exam_name = exam_info.get("ExamName", exam_name).replace(" ", "_")
        file_path = f"E:/{exam_name}.txt"  # 添加simId防止重复

        questions = data.get("data", {}).get("simExamExerciseListPage", [])

        def clean_html(text):
            return BeautifulSoup(text, "html.parser").get_text(separator="\n") if text else ""

        with open(file_path, "w", encoding="utf-8") as f:
            for index, question in enumerate(questions, 1):
                # keyType = question.get('keyType', '')
                # if keyType == '单选' or keyType == '判断改错题':
                #     continue
                title = question.get('title', '无题目内容')
                analyze = question.get('analyze', '暂无解析')

                f.write(f"题目{index}：{clean_html(title)}\n")
                f.write(f"答案{index}：{clean_html(analyze)}\n\n")

        print(f"已保存：{file_path}")
        return True

    except Exception as e:
        print(f"下载失败 {exam_name}: {str(e)}")
        return False


if __name__ == "__main__":

    # 获取所有考试记录
    sim_records = get_sim_ids()
    print(sim_records)
    if not sim_records:
        print("没有找到模拟考试记录")
        exit()

    print(f"共发现 {len(sim_records)} 个模拟考试")

    # 遍历下载每个考试
    for sim_id, exam_name in sim_records:
        success = download_exam(sim_id, exam_name)
        if not success:
            print(f"跳过 {exam_name}...")
        time.sleep(random.randint(0, 2))

    print("全部下载完成！")
