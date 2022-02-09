from typing import Any, Optional, TypedDict, List, Literal, Union
from datetime import datetime


Role = Literal["ROLE_ADMIN", "ROLE_INSTRUCTOR", "ROLE_TA", "ROLE_USER", "ROLE_EDITOR"]

# The messy situation here may get better once
# PEP 655 https://www.python.org/dev/peps/pep-0655/
# is implemented.
# Also, Artemis uses different DTOs and even Attributes depending on the query
# Note: For now to reduce the number of classes all classes are set to
# total = False.

# Some types are not modeled out completely. In this case Any is used.


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
    lastNotificationRead: datetime


class UserDTORequired(BaseEntity):
    login: str
    name: str
    firstName: str
    lastName: str
    email: str
    activated: bool
    langKey: str
    createdBy: str
    createdDate: datetime
    lastModifiedBy: str
    lastModifiedDate: datetime
    authorities: List[Role]


class UserDTO(UserDTORequired, total=False):
    visibleRegistrationNumber: str
    imageUrl: str
    groups: List[str]
    lastNotificationRead: datetime


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
    authorities: List[Role]
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
    createdDate: datetime
    lastModifiedBy: str
    lastModifiedDate: datetime
    lastNotificationRead: datetime
    visibleRegistrationNumber: str
    password: str
    participantIdentifier: str
    resetDate: datetime
    internal: bool


class Course(BaseEntity, total=False):
    title: str
    testCourse: bool
    teachingAssistantGroupName: Optional[str]
    studentGroupName: Optional[str]
    endDate: datetime
    startDate: datetime
    maxPoints: float
    shortName: str
    semester: str
    requestMoreFeedbackEnabled: bool
    registrationEnabled: bool
    registrationConfirmationMessage: Optional[str]
    presentationScore: float
    postsEnabled: bool
    onlineCourse: bool
    maxTeamComplaints: int
    maxRequestMoreFeedbackTimeDays: int
    maxComplaints: int
    maxComplaintTimeDays: int
    instructorGroupName: Optional[str]
    editorGroupName: Optional[str]
    description: str
    customizeGroupNames: bool
    courseIcon: Optional[str]
    complaintsEnabled: bool
    color: Optional[str]
    accuracyOfScores: int


class CourseStats(TypedDict):
    numberOfInstructors: int
    numberOfTeachingAssistants: int
    numberOfEditors: int
    numberOfStudents: int


class CourseWithStats(Course, CourseStats):
    pass


class CourseWithExercises(Course):
    exercises: List["Exercise"]


class Team(BaseEntity, total=False):
    name: str
    shortName: str
    image: str
    students: List[User]
    owner: User

    createdBy: str
    createdDate: datetime
    lastModifiedBy: str
    lastModifiedDate: datetime


ExerciseCategory = str
# This is what is defined in the Artemis Web-Client
# but for some reason the backend sends just strings
# that can be parsed into these objects?!
# class ExerciseCategory(TypedDict, total=False):
#     color: str
#     category: str


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
    completionDate: datetime
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
    submissionDate: datetime
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
    type: ParticipationType
    # Todo: Better typing. Currently the subclasses only are differentiated by this value
    initializationState: InitializationState
    initializationDate: datetime
    presentationScore: int
    results: List[Result]
    submissions: List[Submission]
    exercise: "Exercise"

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


class ProgrammingExerciseStudentParticipation(StudentParticipation, total=False):
    repositoryUrl: str
    buildPlanId: str
    buildPlanUrl: str


class SolutionProgrammingExerciseParticipation(Participation, total=False):
    programmingExercise: "ProgrammingExercise"
    repositoryUrl: str
    buildPlanId: str
    buildPlanUrl: str


class TemplateProgrammingExerciseParticipation(Participation, total=False):
    programmingExercise: "ProgrammingExercise"
    repositoryUrl: str
    buildPlanId: str
    buildPlanUrl: str


class LearningGoal(BaseEntity, total=False):
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
    releaseDate: datetime
    lecture: "Lecture"
    learningGoals: List[LearningGoal]
    type: LectureUnitType


class AttachmentUnit(LectureUnit, total=False):
    description: str
    attachment: "Attachment"


class Attachment(BaseEntity, total=False):
    name: str
    link: str
    releaseDate: datetime
    version: int
    uploadDate: datetime
    attachmentType: AttachmentType
    lecture: "Lecture"
    exercise: "Exercise"
    attachmentUnit: AttachmentUnit


class Lecture(BaseEntity, total=False):
    title: str
    description: str
    startDate: datetime
    endDate: datetime
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


ExerciseType = Literal["programming", "modeling", "quiz", "text", "file-upload"]


# This is the equivalent to "class Exercise implements BaseEntity" in Artemis
class AbstractExercise(BaseEntity, total=False):
    type: ExerciseType
    problemStatement: str
    gradingInstructions: str
    title: str
    shortName: str
    releaseDate: datetime
    dueDate: datetime
    assessmentDueDate: datetime
    maxPoints: float
    bonusPoints: float
    assessmentType: AssessmentType
    allowComplaintsForAutomaticAssessments: bool
    difficulty: Literal["EASY", "MEDIUM", "HARD"]
    mode: Literal["INDIVIDUAL", "TEAM"]
    includedInOverallScore: Literal[
        "INCLUDED_COMPLETELY", "INCLUDED_AS_BONUS", "NOT_INCLUDED"
    ]
    teamAssignmentConfig: TeamAssignmentConfig
    categories: List[ExerciseCategory]
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

    ended: bool
    gradingInstructionFeedbackUsed: bool
    presentationScoreEnabled: bool
    released: bool
    secondCorrectionEnabled: bool
    studentAssignedTeamIdComputed: bool
    teamMode: bool
    visibleToStudents: bool


ProgrammingLanguage = Literal[
    'JAVA',
    'PYTHON',
    'C',
    'HASKELL',
    'KOTLIN',
    'VHDL',
    'ASSEMBLER',
    'SWIFT',
    'OCAML',
    'EMPTY',
]

ProjectType = Literal[
    'MAVEN',
    'ECLIPSE',
    'PLAIN',
    'XCODE',
]


class ProgrammingExercise(AbstractExercise, total=False):
    exerciseType: Literal["PROGRAMMING"]

    projectKey: str
    templateParticipation: TemplateProgrammingExerciseParticipation
    solutionParticipation: SolutionProgrammingExerciseParticipation
    testRepositoryUrl: str
    publishBuildPlanUrl: bool
    allowOnlineEditor: bool
    staticCodeAnalysisEnabled: bool
    maxStaticCodeAnalysisPenalty: float
    allowOfflineIde: bool
    programmingLanguage: ProgrammingLanguage
    packageName: str
    problemStatement: str
    sequentialTestRuns: bool
    showTestNamesToStudents: bool
    checkoutSolutionRepository: bool
    auxiliaryRepositories: List[Any]
    submissionPolicy: Any

    buildAndTestStudentSubmissionsAfterDueDate: datetime
    testCasesChanged: bool

    projectType: ProjectType
    isLocalSimulation: bool
    testRepositoryName: str


UMLDiagramType = Literal[
    'ClassDiagram',
    'ObjectDiagram',
    'ActivityDiagram',
    'UseCaseDiagram',
    'CommunicationDiagram',
    'ComponentDiagram',
    'DeploymentDiagram',
    'PetriNet',
    'SyntaxTree',
    'Flowchart',
]


class ModelingExercise(AbstractExercise, total=False):
    exerciseType: Literal["MODELING"]

    diagramType: UMLDiagramType
    sampleSolutionModel: str
    sampleSolutionExplanation: str


QuizStatus = Literal[
    "CLOSED",
    "OPEN_FOR_PRACTICE",
    "ACTIVE",
    "VISIBLE",
    "HIDDEN",
]


class QuizExercise(AbstractExercise, total=False):
    exerciseType: Literal["QUIZ"]

    remainingTime: int
    timeUntilPlannedStart: int
    visibleToStudents: bool
    randomizeQuestionOrder: bool
    isVisibleBeforeStart: bool
    isOpenForPractice: bool
    isPlannedToStart: bool
    duration: int
    quizPointStatistic: Any
    quizQuestions: List[Any]  # ToDo
    status: QuizStatus

    adjustedDueDate: datetime
    adjustedReleaseDate: datetime
    ended: bool
    started: bool

    isActiveQuiz: bool
    isPracticeModeAvailable: bool


class TextExercise(AbstractExercise, total=False):
    exerciseType: Literal["TEXT"]

    sampleSolution: str
    automaticAssessmentEnabled: bool


class FileUploadExercise(AbstractExercise, total=False):
    exerciseType: Literal["FILE_UPLOAD"]

    filePattern: str
    sampleSolution: str


Exercise = Union[ProgrammingExercise, ModelingExercise, QuizExercise, TextExercise, FileUploadExercise]


class ExamSession(BaseEntity):
    studentExam: "StudentExam"
    sessionToken: str
    initialSession: bool


class StudentExam(BaseEntity, total=False):
    workingTime: int
    submitted: bool
    started: bool
    testRun: bool
    submissionDate: datetime
    user: User
    exam: "Exam"
    exercises: List[Exercise]
    examSessions: List[ExamSession]

    ended: bool


class Exam(BaseEntity, total=False):
    title: str
    visibleDate: datetime
    startDate: datetime
    endDate: datetime
    publishResultsDate: datetime
    examStudentReviewStart: str
    examStudentReviewEnd: str
    gracePeriod: int
    examiner: str
    moduleNumber: str
    courseName: str

    startText: str
    endText: str
    confirmationStartText: str
    confirmationEndText: str
    maxPoints: float
    randomizeExerciseOrder: bool
    numberOfExercisesInExam: int
    numberOfCorrectionRoundsInExam: int
    course: Course
    exerciseGroups: List[ExerciseGroup]
    studentExams: List[StudentExam]
    registeredUsers: List[User]

    numberOfRegisteredUsers: int

    examArchivePath: str
    latestIndividualEndDate: datetime
