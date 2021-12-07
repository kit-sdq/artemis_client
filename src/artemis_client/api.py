from typing import TypedDict, List, Literal


Role = Literal["ROLE_ADMIN", "ROLE_INSTRUCTOR", "ROLE_TA", "ROLE_USER", "ROLE_EDITOR"]


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
    authorities: List[Role]


class UserDTO(UserDTORequired, total=False):
    visibleRegistrationNumber: str
    imageUrl: str
    groups: List[str]
    lastNotificationRead: str
