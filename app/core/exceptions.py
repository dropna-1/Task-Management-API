from winreg import ExpandEnvironmentStrings


class ProjectNotFoundError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class ForbiddenError(Exception):
    pass

class MemberAlreadyExistError(Exception):
    pass

class MemberNotExistError(Exception):
    pass

class PasswordWrongError(Exception):
    pass

class TaskAlreadyExistError(Exception):
    pass

class TaskAlreadySelectedError(Exception):
    pass

class TaskNotExistError(Exception):
    pass

class TaskNotFoundError(Exception):
    pass

class PromotedError(Exception):
    pass

class DemotedError(Exception):
    pass