import threading
import time

from core import strings

TIMEOUT = 60
THREAD_NAME = "core main thread"


def process_video():
    """
    This function converts the video to HLS format and uploads it to AWS.
    """
    from core.models import Video

    while Video.objects.filter(status=strings.Constants.NEW).exists():
        for video in Video.objects.filter(status=strings.Constants.NEW):
            video.is_processing()
            video.update_video_duration()
            video.generate_thumbnails()
            video.convert_to_hls()


def run():
    """
    This function ensures that only one instance of the thread is running at any time.
    """

    def _run():
        while True:
            process_video()
            time.sleep(TIMEOUT)

    is_thread_alive = False

    for thread in threading.enumerate():
        if thread.name == THREAD_NAME:
            is_thread_alive = True
            break

    if is_thread_alive is False:
        thread = threading.Thread(target=_run)
        thread.name = THREAD_NAME
        thread.start()
