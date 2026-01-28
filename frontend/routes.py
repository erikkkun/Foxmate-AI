from enum import Enum

class Route(str, Enum):
    HOME = "Dashboard"
    MY_INFO = "My Information"
    SIGNIN = "Sign-in"
    SETTINGS = "Settings"
    MEMBERSHIP = "Membership"
    CUSTOMIZE = "Customize"
    WEEKLY = "Weekly Report"
    WORKSHOP = "Workshop"
    FOX = "Your Fox"
    SHOP = "Shop"
    FAQ = "FAQ & Support"
    WELCOME = "welcome"
    LAUNCHING = "launching"
    AUTH = "auth"

