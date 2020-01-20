from django.db import models


class PullRequestInfo(models.Model):
    """
    pullRequest 信息
    """
    pull_request_id = models.IntegerField(primary_key=True)  # pullRequest id
    title = models.CharField(max_length=5000)  # pullRequest 标题
    status = models.CharField(max_length=50)  # pullRequest 状态
    complete_time = models.DateTimeField(null=True)  # 完成时间


class BuildInfo(models.Model):
    """
    build 信息
    """
    id = models.AutoField(primary_key=True)
    pull_request_id = models.IntegerField(default=0)  # 没有pull request 信息时，默认id=0
    build_id = models.CharField(max_length=255)
    apk_type = models.CharField(max_length=50)
    commit_msg = models.CharField(max_length=1000)  # commit 信息
    jenkins_info_full_str = models.CharField(max_length=5000)  # jenkins 信息
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    last_sign_time = models.DateTimeField(auto_now=True)  # 最后一次测试打标时间


class ApkDetailInfo(models.Model):
    """
    apk 详细信息
    """
    id = models.AutoField(primary_key=True)  # 自增id
    build_id = models.CharField(max_length=500)
    apk_name = models.CharField(max_length=500)
    apk_type = models.CharField(max_length=50)
    apk_location = models.CharField(max_length=500)
    test_result = models.CharField(max_length=32, default='未测试')  # 测试结果
    test_desc = models.CharField(max_length=5000)  # 测试备注
    market_desc = models.CharField(max_length=5000)  # 市场部备注
    pull_request_items = models.CharField(max_length=1000)  # 打标选中的pullRequest项
    is_tab = models.CharField(max_length=2, default='0')  # 是否打标
    is_report = models.CharField(max_length=2, default='0')  # 是否打标
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    update_time = models.DateTimeField(auto_now=True)  # 更新时间


class ApkReportDetail(models.Model):
    """
    apk 测试报告详情
    """
    id = models.AutoField(primary_key=True)
    apk_id = models.IntegerField()
    test_report_name = models.CharField(max_length=255)  # 测试报告名称
    test_report_data = models.BinaryField()  # 测试报告内容
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
