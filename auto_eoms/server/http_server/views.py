import os

from django.http import StreamingHttpResponse

# Create your views here.
from utils.constant_key import APK_LOCATION_KEY


def download_apk(request):
    """
    下载apk
    :param request:
    :return:
    """
    if request.method == "GET":
        apk = request.GET.get(APK_LOCATION_KEY)

        def file_iterator(file_name, chunk_size=512):
            with open(file_name, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        response = StreamingHttpResponse(file_iterator(apk))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(apk.split(os.sep)[-1])
        return response

