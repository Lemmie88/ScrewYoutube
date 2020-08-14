class Constants:
    PRIVATE = 'PRI'
    PUBLIC = 'PUB'

    VISIBILITY_CHOICES = [
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    ]

    UPLOADING = 'UPL'
    PROCESSING = 'PRO'
    READY = 'REA'

    VIDEO_STATUS_CHOICES = [
        (UPLOADING, 'Uploading'),
        (PROCESSING, 'Processing'),
        (READY, 'Ready'),
    ]

    # This is the length of the url code.
    DEFAULT_CODE_LENGTH = 10
