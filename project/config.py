# URL ITEM DECLARATION

# AUTH_URLS
REGISTRATION_URL = '/registration'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
ACCESS_LOGOUT_URL = '/logout/access'
REFRESH_LOGOUT_URL = '/logout/refresh'
TOKEN_REFRESH_URL = '/token/refresh'
CHANGE_PASSWORD_URL = '/user/changepassword/<ObjectId:id>'

# ROLES-MASTER-URL
ROLES_URL = '/roles'
ROLES_ACTIVE_URL = '/roles/active'
ROLES_INACTIVE_URL = '/roles/inactive'
ROLE_URL = '/role/<ObjectId:id>'
ROLE_CREATE_URL = '/role/create'
ROLE_AUTOCOMPLETE_URL = '/roles/autoComplete'
ROLE_ACTIVE_AUTOCOMPLETE_URL = '/roles/autoComplete/active'
ROLE_INACTIVE_AUTOCOMPLETE_URL = '/roles/autoComplete/inactive'
ROLE_UPDATE_URL = '/role/update/<ObjectId:id>'
ROLE_DELETE_URL = '/role/delete/<ObjectId:id>'
ROLE_ACTIVATE_URL = '/role/activate/<ObjectId:id>'

#PROCESSS-MASTER-URL
PROCESSES_URL = '/processes'
PROCESS_URL = '/process/<ObjectId:id>'
PROCESS_CREATE_URL = '/process/create'
# PROCESS_AUTOCOMPLETE_URL = '/processs/autoComplete'
# PROCESS_UPDATE_URL = '/process/update/<ObjectId:id>'
# PROCESS_DELETE_URL = '/process/delete/<ObjectId:id>'
# PROCESS_ACTIVATE_URL = '/process/activate/<ObjectId:id>'
# PROCESS_REMOVE_URL = '/process/remove/<ObjectId:id>'