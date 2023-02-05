class ApiError(Exception):
    code = 422
    description = "Default message"

class UserAlreadyExists(ApiError):
    code = 412
    description = "Usuario con username o email ya existe"

class SpecialistAlreadyExists(ApiError):
    code = 412
    description = "Especialista con username o email ya existe"

class SpecialistIsNotRegister(ApiError):
    code = 412
    description = "Especialista aún no registrado"

class SpecialistWrongPassword(ApiError):
    code = 401
    description = "La contraseña ingresada es incorrecta"

class InvalidParams(ApiError):
    code = 400
    description = "Bad request"
