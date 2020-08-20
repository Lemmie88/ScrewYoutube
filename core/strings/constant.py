class Constant:
    PRIVATE = 'PRI'
    PUBLIC = 'PUB'

    VISIBILITY_CHOICES = [
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    ]

    NEW = 'NEW'
    PROCESSING = 'PRO'
    UPLOADING = 'UPL'
    READY = 'REA'

    VIDEO_STATUS_CHOICES = [
        (NEW, 'New'),
        (PROCESSING, 'Processing'),
        (UPLOADING, 'Uploading'),
        (READY, 'Ready'),
    ]

    # This is the length of the url code.
    DEFAULT_CODE_LENGTH = 10

    SUCCESS = {'status': 'ok'}
