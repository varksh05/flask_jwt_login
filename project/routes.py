from project import api, config
from project.resources import AuthResource, RoleResource

api.add_resource(AuthResource.Registration, config.REGISTRATION_URL)
api.add_resource(AuthResource.Login, config.LOGIN_URL)
api.add_resource(AuthResource.ChangePassword, config.CHANGE_PASSWORD_URL)
api.add_resource(AuthResource.Logout, config.LOGOUT_URL)


api.add_resource(RoleResource.CreateRole, config.ROLE_CREATE_URL)
