from typing import TypedDict, List, Literal

Role = Literal["ROLE_ADMIN", "ROLE_INSTRUCTOR", "ROLE_TA", "ROLE_USER", "ROLE_EDITOR"]

# The messy situation here may get better once
# PEP 655 https://www.python.org/dev/peps/pep-0655/
# is implemented.
# Also, Artemis uses different DTOs and even Attributes depending on the query

class LoginVM(TypedDict):
    username: str
    password: str
    rememberMe: bool

class SearchUserDTORequired(TypedDict):
    login: str
    name: str
    firstName: str
    lastName: str
    email: str
    activated: bool
    id: int


class SearchUserDTO(SearchUserDTORequired, total=False):
    visibleRegistrationNumber: str
    imageUrl: str
    groups: List[str]
    lastNotificationRead: str


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


class ManagedUserVM(UserDTO):
    password: str
