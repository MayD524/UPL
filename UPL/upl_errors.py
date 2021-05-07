class json_mishandled(Exception):
    """For dealing with mshandled json data/files"""

class download_exception(Exception):
    """Error in a download"""

class UPL_MISSING_FILE(Exception):
    """Missing files"""

class UPL_UNKNOWN_FILE(Exception):
    """Unknown files"""

class UPL_PERM_DENY(Exception):
    """Lack of permissions"""