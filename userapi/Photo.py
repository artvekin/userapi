class Photo:
    def __init__ (self, id, pic, small_pic):
        self.id         = id
        self.pic        = pic
        self.small_pic  = small_pic


class PhotosUploadInfo:
    def __init__(self, aid, upload_url = None, upload_hash = None, upload_rhash = None):
        self.upload_url     = upload_url
        self.upload_hash    = upload_hash
        self.upload_rhash   = upload_rhash
        self.aid            = aid

class Photos:
    def __init__(self, total, photos, ts = None, upload_info = None):
        self.total      = total
        self.photos     = photos
        self.ts         = ts
        self.upload     = upload_info
