

class Box:
    """
        框类
    """
    def __init__(self, x, y, width, height):
        """参数为点坐标、宽、高"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_max(self):
        """获得最大的点位置坐标"""
        max_x = self.x + self.width
        max_y = self.y + self.height
        return max_x, max_y

    def get_min(self):
        """获得最小的点位置坐标"""
        min_x = self.x
        min_y = self.y
        return min_x, min_y

    def get_area(self):
        """计算框的面积"""
        return self.width * self.height

    @classmethod
    def overlapping_area(cls, box1, box2):
        """
        计算两个框的重叠面积
        :param box1:
        :param box2:
        :return:
        """
        width = min(box1.get_max()[0], box2.get_max()[0]) - max(box1.get_min()[0], box2.get_min()[0])
        height = min(box1.get_max()[1], box2.get_max()[1]) - max(box1.get_min()[1], box2.get_min()[1])
        if width < 0 or height < 0:
            return 0
        else:
            return width * height
