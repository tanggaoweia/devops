from django.db import models

# Create your models here.


class ModelsAndNetworksInfo(models.Model):
    """
    模型和网络结构信息
    """
    id = models.AutoField(primary_key=True)                         # 自增id
    models_name = models.CharField(max_length=500)                  # 模型名称
    common_path = models.CharField(max_length=500)                  # 模型和网络的公用地址
    models_path = models.CharField(max_length=500)                  # 模型路径
    models_size = models.CharField(max_length=500)                  # 模型文件大小
    networks_path = models.CharField(max_length=500)                # 网络结构路径
    total_params = models.CharField(max_length=255)                 # 总参数
    flops = models.CharField(max_length=255)                        # 算力
    flops_result_info = models.CharField(max_length=5000)                 # 结果信息
    flops_result = models.CharField(max_length=20, default='脚本未执行')       # 算力测试结果
    create_time = models.DateTimeField(auto_now_add=True)           # 创建时间
