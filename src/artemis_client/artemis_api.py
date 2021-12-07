from typing import TypedDict, List, Optional


class LoginVM(TypedDict):
    username: str
    password: str
    rememberMe: bool


class UserDTORequired(TypedDict):
    login: str
    name: str
    firstName: str
    lastName: str
    email: str
    activated: bool
    langKey: str
    createdBy: str
    createdDate: str
    lastModifiedBy: str
    lastModifiedDate: str
    id: int
    authorities: List[str]


class UserDTO(UserDTORequired, total=False):
    visibleRegistrationNumber: str
    imageUrl: str
    groups: List[str]
    lastNotificationRead: str
