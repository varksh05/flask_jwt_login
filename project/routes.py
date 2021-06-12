from project import api, config
from project.resources import AuthResource, RoleResource, ProcessResource

# Auth Resources
api.add_resource(AuthResource.Registration, config.REGISTRATION_URL)
api.add_resource(AuthResource.Login, config.LOGIN_URL)
api.add_resource(AuthResource.ChangePassword, config.CHANGE_PASSWORD_URL)
api.add_resource(AuthResource.Logout, config.LOGOUT_URL)

# Roles Resources
api.add_resource(RoleResource.CreateRole, config.ROLE_CREATE_URL)
api.add_resource(RoleResource.GetOneRole, config.ROLE_URL)
api.add_resource(RoleResource.GetAllRole, config.ROLES_URL)
api.add_resource(RoleResource.GetAllActiveRole, config.ROLES_ACTIVE_URL)
api.add_resource(RoleResource.GetAllInactiveRole, config.ROLES_INACTIVE_URL)
api.add_resource(RoleResource.GetRolesAutoCompleteList, config.ROLE_AUTOCOMPLETE_URL)
api.add_resource(RoleResource.GetRolesAutoCompleteActiveList, config.ROLE_ACTIVE_AUTOCOMPLETE_URL)
api.add_resource(RoleResource.GetRolesAutoCompleteInactiveList, config.ROLE_INACTIVE_AUTOCOMPLETE_URL)
api.add_resource(RoleResource.UpdateRole, config.ROLE_UPDATE_URL)
api.add_resource(RoleResource.DeleteRole, config.ROLE_DELETE_URL)
api.add_resource(RoleResource.ActivateRole, config.ROLE_ACTIVATE_URL)

# Processs Resources
# api.add_resource(ProcessResource.CreateProcess, config.PROCESS_CREATE_URL)
# api.add_resource(ProcessResource.GetOneProcess, config.PROCESS_URL)
# api.add_resource(ProcessResource.GetAllProcess, config.PROCESSS_URL)
# api.add_resource(ProcessResource.GetProcesssAutoCompleteList, config.PROCESS_AUTOCOMPLETE_URL)
# api.add_resource(ProcessResource.UpdateProcess, config.PROCESS_UPDATE_URL)
# api.add_resource(ProcessResource.DeleteProcess, config.PROCESS_DELETE_URL)
# api.add_resource(ProcessResource.ActivateProcess, config.PROCESS_ACTIVATE_URL)
# api.add_resource(ProcessResource.RemoveProcess, config.PROCESS_REMOVE_URL)
# api.add_resource(RoleResource.RemoveRole, config.ROLE_REMOVE_URL)
