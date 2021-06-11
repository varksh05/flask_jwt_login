from project import api, config
from project.resources import AuthResource, RoleResource, OrgResource

# Auth Resources
api.add_resource(AuthResource.Registration, config.REGISTRATION_URL)
api.add_resource(AuthResource.Login, config.LOGIN_URL)
api.add_resource(AuthResource.ChangePassword, config.CHANGE_PASSWORD_URL)
api.add_resource(AuthResource.Logout, config.LOGOUT_URL)

# Roles Resources
api.add_resource(RoleResource.CreateRole, config.ROLE_CREATE_URL)
api.add_resource(RoleResource.GetOneRole, config.ROLE_URL)
api.add_resource(RoleResource.GetAllRole, config.ROLES_URL)
api.add_resource(RoleResource.GetRolesAutoCompleteList, config.ROLE_AUTOCOMPLETE_URL)
api.add_resource(RoleResource.UpdateRole, config.ROLE_UPDATE_URL)
api.add_resource(RoleResource.DeleteRole, config.ROLE_DELETE_URL)
api.add_resource(RoleResource.RemoveRole, config.ROLE_REMOVE_URL)
