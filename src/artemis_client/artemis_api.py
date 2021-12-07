from typing import TypedDict, List


class LoginVM(TypedDict):
    username: str
    password: str
    rememberMe: bool


class UserDTO(TypedDict):
    login: str
    name: str
    firstName: str
    lastName: str
    email: str
    visibleRegistrationNumber: str
    imageUrl: str
    activated: bool
    langKey: str
    createdBy: str
    createdDate: str
    lastModifiedBy: str
    lastModifiedDate: str
    id: int
    lastNotificationRead: str
    authorities: List[str]
    groups: List[str]
