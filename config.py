import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "nict-25yrs-change-me-in-production")
    WTF_CSRF_ENABLED = True
    INSTITUTE_NAME = "National Institute of Computer Technology"
    INSTITUTE_SHORT = "NICT"
    FOUNDED_YEAR = 2001
    ADDRESS = "Plot 45, Knowledge Park, Sector 12, Innovation City – 560001"
    PHONE = "+91 80 4567 8900"
    EMAIL = "admissions@nict.edu"