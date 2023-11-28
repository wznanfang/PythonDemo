import pandas as pd


def salary():
    # 读取Excel文件
    df = pd.read_excel('E:/1/1.xlsx')

    # 筛选出员工名为"张三"的薪资情况
    zhangsan_salary = df[df['姓名'] == '张三']

    print(zhangsan_salary)

    # 筛选出员工名为"张三"且月份为"2023-01"的薪资情况
    zhangsan_jan_salary = df[(df['姓名'] == '张三') & (df['月份'] == '2023-1')]
    print(zhangsan_jan_salary)

    # 计算张三工资总和
    zhangsan_salary_sum = df[df['姓名'] == '张三']['薪资'].sum()
    print(zhangsan_salary_sum)

    # 计算张三工资平均值
    zhangsan_salary_mean = df[df['姓名'] == '张三']['薪资'].mean()
    print(zhangsan_salary_mean)


if __name__ == "__main__":
    salary()
