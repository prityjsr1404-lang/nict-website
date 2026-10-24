import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "nict-25yrs-change-me-in-production")
    WTF_CSRF_ENABLED = True

    INSTITUTE_NAME = "National Institute of Computer Technology"
    INSTITUTE_SHORT = "NICT"
    FOUNDED_YEAR = 2001

    # ============ CONTACT ============
    PHONE = "+91 9204110306"
    EMAIL = "nictjsr@gmail.com"

    # ============ BRANCH 1: MAIN CAMPUS ============
    MAIN_BRANCH_NAME = "Main Campus (Head Office)"
    MAIN_BRANCH_ADDRESS = "Bagbera Railway Colony Lal Building Chowk, Jamshedpur – 831002"
    MAIN_BRANCH_PHONE = "+91 9204110306"
    MAIN_BRANCH_EMAIL = "nictjsr@gmail.com"

    # ============ BRANCH 2: NEW CAMPUS ============
    NEW_BRANCH_NAME = "New Campus (Laxminagar Branch)"
    NEW_BRANCH_ADDRESS = "1st Floor, Shree Kailash Tower, Laxminagar,Near Hanuman Mandir, Jamshedpur – 831007"
    NEW_BRANCH_PHONE = "+91 9508994032"
    NEW_BRANCH_EMAIL = "nictjsr@gmail.com"

    # ============ OFFICE HOURS ============
    OFFICE_HOURS = "Monday – Friday: 7:00 AM – 8:00 PM | Sunday off"