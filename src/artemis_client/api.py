from typing import Any, TypedDict, List, Literal, Union

Role = Literal["ROLE_ADMIN", "ROLE_INSTRUCTOR", "ROLE_TA", "ROLE_USER", "ROLE_EDITOR"]

# The messy situation here may get better once
# PEP 655 https://www.python.org/dev/peps/pep-0655/
# is implemented.
# Also, Artemis uses different DTOs and even Attributes depending on the query


class LoginVM(TypedDict):
    username: str
    password: str
    rememberMe: bool


class BaseEntity(TypedDict):
    id: int


class SearchUserDTORequired(BaseEntity):
    login: str
    name: str
    firstName: str
    lastName: str
    email: str
    activated: bool


class SearchUserDTO(SearchUserDTORequired, total=False):
    visibleRegistrationNumber: str
    imageUrl: str
    groups: List[str]
    lastNotificationRead: str


class UserDTORequired(BaseEntity):
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
    authorities: List[Role]


class UserDTO(UserDTORequired, total=False):
    visibleRegistrationNumber: str
    imageUrl: str
    groups: List[str]
    lastNotificationRead: str


class ManagedUserVM(TypedDict):
    login: str
    firstName: str
    lastName: str
    email: str
    password: str
    imageUrl: str
    visibleRegistrationNumber: str
    authorities: List[Role]
    groups: List[str]


class GuidedTourSetting(TypedDict, total=False):
    guidedTourKey: str
    guidedTourStep: int
    guidedTourState: Literal["STARTED", "FINISHED"]


class Organization(BaseEntity, total=False):
    name: str
    shortName: str
    url: str
    description: str
    logoUrl: str
    emailPattern: str
    users: List["User"]  # Forward-reference as strings!
    courses: List["Course"]
    numberOfUsers: int
    numberOfCourses: int


class Account(TypedDict, total=False):
    activated: bool
    authorities: List[str]
    login: str
    email: str
    name: str
    firstName: str
    lastName: str
    langKey: str
    imageUrl: str
    guidedTourSettings: List[GuidedTourSetting]


class User(Account, BaseEntity, total=False):
    groups: List[str]
    organizations: List[Organization]
    createdBy: str
    createdDate: str
    lastModifiedBy: str
    lastModifiedDate: str
    lastNotificationRead: str
    visibleRegistrationNumber: str
    password: str


class Course(BaseEntity, total=False):
    title: str
    shortName: str
    studentGroupName: str
    teachingAssistantGroupName: str
    editorGroupName: str
    instructorGroupName: str
    testCourse: bool
    onlineCourse: bool
    maxComplaints: int
    maxTeamComplaints: int
    maxComplaintTimeDays: int
    postsEnabled: bool
    maxRequestMoreFeedbackTimeDays: int
    registrationEnabled: bool
    presentationScore: int
    accuracyOfScores: int
    requestMoreFeedbackEnabled: bool
    complaintsEnabled: bool
    semester: str
    endDate: str
    startDate: str
    maxPoints: int


class CourseStats(TypedDict):
    numberOfInstructors: int
    numberOfTeachingAssistants: int
    numberOfEditors: int
    numberOfStudents: int


class CourseWithStats(Course, CourseStats):
    pass


class Team(BaseEntity, total=False):
    name: str
    shortName: str
    image: str
    students: List[User]
    owner: User

    createdBy: str
    createdDate: str
    lastModifiedBy: str
    lastModifiedDate: str


class ExerciseCategory(TypedDict, total=False):
    color: str
    category: str


class TeamAssignmentConfig(BaseEntity, total=False):
    # exercise: Exercise
    minTeamSize: int
    maxTeamSize: int


SubmissionType = Literal[
    "MANUAL",
    "TIMEOUT",
    "INSTRUCTOR",
    "EXTERNAL",
    "TEST",
    "ILLEGAL",
]

SubmissionExerciseType = Literal[
    "programming",
    "modeling",
    "quiz",
    "text",
    "file-upload",
]


class GradingInstruction(BaseEntity, total=False):
    credits: int
    gradingScale: str
    instructionDescription: str
    feedback: str
    usageCount: int


FeedbackConflictType = Literal[
    "INCONSISTENT_COMMENT",
    "INCONSISTENT_SCORE",
    "INCONSISTENT_FEEDBACK",
]


class FeedbackConflict(BaseEntity, total=False):
    conflict: bool
    conflictingFeedbackId: int
    createdAt: str
    solvedAt: str
    type: FeedbackConflictType
    discard: bool


FeedbackCorrectionErrorType = Literal[
    "INCORRECT_SCORE",
    "UNNECESSARY_FEEDBACK",
    "MISSING_GRADING_INSTRUCTION",
    "INCORRECT_GRADING_INSTRUCTION",
    "EMPTY_NEGATIVE_FEEDBACK",
]


FeedbackType = Union[FeedbackCorrectionErrorType, Literal["CORRECT"]]


class Feedback(BaseEntity, total=False):
    gradingInstruction: GradingInstruction
    text: str
    detailText: str
    reference: str
    credits: int
    type: FeedbackType
    result: "Result"
    positive: bool
    conflictingTextAssessments: List[FeedbackConflict]
    suggestedFeedbackReference: str
    suggestedFeedbackOriginSubmissionReference: int
    suggestedFeedbackParticipationReference: int

    referenceType: str
    referenceId: str


AssessmentType = Literal["AUTOMATIC", "SEMI_AUTOMATIC", "MANUAL"]


class Result(BaseEntity, total=False):
    resultString: str
    completionDate: str
    successful: bool
    hasFeedback: bool
    score: float
    assessmentType: AssessmentType
    rated: bool
    hasComplaint: bool
    exampleResult: bool
    submission: "Submission"
    assessor: User
    feedbacks: List[Feedback]
    participation: "Participation"
    durationInMinutes: int


class Submission(BaseEntity, total=False):
    submitted: bool
    submissionDate: str
    type: SubmissionType
    exampleSubmission: bool
    submissionExerciseType: SubmissionExerciseType
    durationInMinutes: int
    results: List[Result]
    participation: "Participation"
    isSynced: bool


ParticipationType = Literal["student", "programming", "template", "solution"]

InitializationState = Literal[
    "UNINITIALIZED",
    "REPO_COPIED",
    "REPO_CONFIGURED",
    "BUILD_PLAN_COPIED",
    "BUILD_PLAN_CONFIGURED",
    "INITIALIZED",
    "FINISHED",
    "INACTIVE",
]


class Participation(BaseEntity, total=False):
    initializationState: InitializationState
    initializationDate: str
    presentationScore: int
    results: List[Result]
    submissions: List[Submission]
    exercise: "Exercise"
    type: ParticipationType

    participantName: str
    participantIdentifier: str
    submissionCount: str


class StudentParticipation(Participation, total=False):
    student: User
    team: Team
    participantIdentifier: str
    testRun: bool


TutorParticipationStatus = Literal[
    "NOT_PARTICIPATED",
    "REVIEWED_INSTRUCTIONS",
    "TRAINED",
    "COMPLETED",
]


class ExampleSubmission(BaseEntity, total=False):
    usedForTutorial: bool
    exercise: "Exercise"
    submission: Submission
    tutorParticipations: List["TutorParticipation"]
    assessmentExplanation: str


class TutorParticipation(BaseEntity, total=False):
    status: TutorParticipationStatus
    assessedExercise: "Exercise"
    tutor: User
    trainedExampleSubmissions: List[ExampleSubmission]


ParticipationStatus = Literal[
    "quiz-uninitialized",
    "quiz-active",
    "quiz-submitted",
    "quiz-not-started",
    "quiz-not-participated",
    "quiz-finished",
    "no-team-assigned",
    "uninitialized",
    "initialized",
    "inactive",
    "exercise-active",
    "exercise-submitted",
    "exercise-missed",
]


AttachmentType = Literal[
    "FILE",
    "URL",
]


class LearningGoal(BaseEntity, total=False):
    id: int
    title: str
    description: str
    course: Course
    exercises: List["Exercise"]
    lectureUnits: List["LectureUnit"]


LectureUnitType = Literal[
    "attachment",
    "exercise",
    "text",
    "video",
]


class LectureUnit(BaseEntity, total=False):
    name: str
    releaseDate: str
    lecture: "Lecture"
    learningGoals: List[LearningGoal]
    type: LectureUnitType


class AttachmentUnit(LectureUnit, total=False):
    description: str
    attachment: "Attachment"


class Attachment(BaseEntity, total=False):
    name: str
    link: str
    releaseDate: str
    version: int
    uploadDate: str
    attachmentType: AttachmentType
    lecture: "Lecture"
    exercise: "Exercise"
    attachmentUnit: AttachmentUnit


class Lecture(BaseEntity, total=False):
    title: str
    description: str
    startDate: str
    endDate: str
    attachments: List[Attachment]
    posts: List[Any]  # TODO
    lectureUnits: List[LectureUnit]
    course: Course


class ExerciseHint(BaseEntity, total=False):
    title: str
    content: str
    exercise: "Exercise"


class GradingCriterion(BaseEntity):
    title: str
    structuredGradingInstructions: List[GradingInstruction]


class ExerciseGroup(BaseEntity, total=False):
    title: str
    isMandatory: bool
    exam: Any  # todo
    exercises: List["Exercise"]


class Exercise(BaseEntity, total=False):
    problemStatement: str
    gradingInstructions: str
    title: str
    shortName: str
    releaseDate: str
    dueDate: str
    assessmentDueDate: str
    maxPoints: int
    bonusPoints: int
    assessmentType: AssessmentType
    allowComplaintsForAutomaticAssessments: bool
    difficulty: Literal["EASY", "MEDIUM", "HARD"]
    mode: Literal["INDIVIDUAL", "TEAM"]
    includedInOverallScore: Literal[
        "INCLUDED_COMPLETELY", "INCLUDED_AS_BONUS", "NOT_INCLUDED"
    ]
    teamAssignmentConfig: TeamAssignmentConfig
    categories: List[ExerciseCategory]
    type: Literal["programming", "modeling", "quiz", "text", "file-upload"]

    teams: List[Team]
    studentParticipations: List[StudentParticipation]
    tutorParticipations: List[TutorParticipation]
    course: Course
    participationStatus: ParticipationStatus
    exampleSubmissions: List[ExampleSubmission]
    attachments: List[Attachment]
    posts: List[Any]  # todo
    exerciseHints: List[ExerciseHint]
    gradingCriteria: List[GradingCriterion]
    exerciseGroup: ExerciseGroup
    learningGoals: List[LearningGoal]
