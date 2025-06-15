from fastapi import status


class CustomException(BaseException):
    
    status_code = 500
    detail = ''


class UserAlreadyExistsException(CustomException):

    status_code = status.HTTP_409_CONFLICT
    detail = 'User already exists'


class PasswordsDoNotMatchException(CustomException):

    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Passwords do not match'


class IncorrectLoginOrPasswordException(CustomException):

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Incorrect login or password'


class EquipmentAlreadyExistsException(CustomException):

    status_code = status.HTTP_409_CONFLICT
    detail = 'Equipment already exists'
