CHECK_DOC = {
    'allowed_extensions' : [
        'pdf',
        'doc',
        'docx',
        'xls',
        'xlsx',
        'ppt',
        'pptx',
    ],
    'allowed_mimetypes' : [
        'application/pdf',
        'application/zip',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-powerpoint',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'application/CDFV2',
        'application/CDFV2-unknown',
        'application/xml',
    ],
    'allowed_verbose' : [
        'PDF',
        'ZIP',
        'Word',
        'Excel',
        'PowerPoint',
    ],
}


CHECK_WEB_IMAGE = {
    'allowed_extensions' : [
        'png',
        'jpg',
        'jpeg',
        'gif',
    ],
    'allowed_mimetypes' : [
        'image/png',
        'image/jpeg',
        'image/gif',
    ],
    'allowed_verbose' : [
        'PNG',
        'JPEG',
        'GIF',
    ],
}


CHECK_RAW_IMAGE = {
    'allowed_extensions' : [
        'png',
        'jpg',
        'jpeg',
        'gif',
        'tif',
        'tiff',
    ],
    'allowed_mimetypes' : [
        'image/png',
        'image/jpeg',
        'image/gif',
        'image/tiff',
    ],
    'allowed_verbose' : [
        'PNG',
        'JPEG',
        'GIF',
        'TIFF',
    ],
}
