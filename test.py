from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from pprint import pprint as print

def create_tag_manager_user_access(
  account_id:str,
  container_id:str,
  user_email:str,
  account_permission:str,
  container_permission:str
  ) -> dict:
  """Creates a new user access for a given Tag Manager account and container.

  Args:
    account_id (str): The ID of the Tag Manager account.
    container_id (str): The ID of the Tag Manager container.
    user_email (str): The email address of the user to add.
    account_permission (str, optional): The permission level for the user on the entire account. Defaults to 'accountPermissionUnspecified'. Valid options are:
      - 'accountPermissionUnspecified': Unspecified permission level (not recommended).
      - 'admin': Grants administrator access to the account.
      - 'noAccess': Revokes any access to the account.
      - 'user': Grants basic user access to the account (view information).
    container_permission (str, optional): The permission level for the user within the specific container. Defaults to 'containerPermissionUnspecified'. Valid options are:
      - 'containerPermissionUnspecified': Unspecified permission level (not recommended).
      - 'approve': Allows approving container versions.
      - 'edit': Allows editing the container content.
      - 'noAccess': Revokes any access to the container.
      - 'publish': Allows publishing container versions.
      - 'read': Allows viewing the container content.

  Returns:
    dict: The newly created user access object as a dictionary.
  """
  SERVICE_ACCOUNT_FILE = './service_account.json'

  SCOPES = ['https://www.googleapis.com/auth/tagmanager.manage.users']

  creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

  service = build('tagmanager', 'v2', credentials=creds)

  access_request_body = {
    "accountAccess":{
      "permission": account_permission # accountPermissionUnspecified, admin, noAccess, user
    },
    "accountId":account_id,
    "containerAccess": [
      {
        "containerId": container_id,
        "permission": container_permission # approve, containerPermissionUnspecified, edit, noAccess, publish, read
      }
    ],
    "emailAddress":user_email,
    "path": f"accounts/{account_id}"
  }

  request = service.accounts().user_permissions().create(
    parent=f"accounts/{account_id}",
    body=access_request_body
  )

  response = request.execute()
  return response

def update_tag_manager_user_access(
  account_id:str,
  container_id:str,
  user_email:str,
  account_permission:str,
  container_permission:str,
  user_permission_id:str,
  ) -> dict:
  """Updates access of an existing user for a given Tag Manager account and container.

  Args:
    account_id (str): The ID of the Tag Manager account.
    container_id (str): The ID of the Tag Manager container.
    user_email (str): The email address of the user to add.
    account_permission (str, optional): The permission level for the user on the entire account. Defaults to 'accountPermissionUnspecified'. Valid options are:
      - 'accountPermissionUnspecified': Unspecified permission level (not recommended).
      - 'admin': Grants administrator access to the account.
      - 'noAccess': Revokes any access to the account.
      - 'user': Grants basic user access to the account (view information).
    container_permission (str, optional): The permission level for the user within the specific container. Defaults to 'containerPermissionUnspecified'. Valid options are:
      - 'containerPermissionUnspecified': Unspecified permission level (not recommended).
      - 'approve': Allows approving container versions.
      - 'edit': Allows editing the container content.
      - 'noAccess': Revokes any access to the container.
      - 'publish': Allows publishing container versions.
      - 'read': Allows viewing the container content.

  Returns:
    dict: The updated user access object as a dictionary.
  """
  SERVICE_ACCOUNT_FILE = './service_account.json'

  SCOPES = ['https://www.googleapis.com/auth/tagmanager.manage.users']

  creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

  service = build('tagmanager', 'v2', credentials=creds)

  access_request_body = {
    "accountAccess":{
      "permission": account_permission # accountPermissionUnspecified, admin, noAccess, user
    },
    "accountId":account_id,
    "containerAccess": [
      {
        "containerId": container_id,
        "permission": container_permission # approve, containerPermissionUnspecified, edit, noAccess, publish, read
      }
    ],
    "emailAddress":user_email,
    "path": f"accounts/{account_id}"
  }

  request = service.accounts().user_permissions().update(
    path=f"accounts/{account_id}/user_permission{user_permission_id}",
    body=access_request_body
  )

  response = request.execute()
  return response

def list_tag_manager_accesses(account_id:str) -> dict:
  """Lists the accesses for a given Tag Manager account.

  Args:
    account_id (str): The ID of the Tag Manager account.

  Returns:
    dict: The updated user access object as a dictionary.
  """
  SERVICE_ACCOUNT_FILE = './service_account.json'

  SCOPES = ['https://www.googleapis.com/auth/tagmanager.manage.users']

  creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

  service = build('tagmanager', 'v2', credentials=creds)

  request = service.accounts().user_permissions().list(
    parent=f"accounts/{account_id}"
  )

  response = request.execute()
  return response

def add_or_update_permission(
  account_id:str,
  container_id:str,
  user_email:str,
  account_permission:str,
  container_permission:str
) -> dict:
  """Adds or updates the access of an existing user for a given Tag Manager account and container.

  Args:
    account_id (str): The ID of the Tag Manager account.
    container_id (str): The ID of the Tag Manager container.
    user_email (str): The email address of the user to add.
    account_permission (str, optional): The permission level for the user on the entire account. Defaults to 'accountPermissionUnspecified'. Valid options are:
      - 'accountPermissionUnspecified': Unspecified permission level (not recommended).
      - 'admin': Grants administrator access to the account.
      - 'noAccess': Revokes any access to the account.
      - 'user': Grants basic user access to the account (view information).
    container_permission (str, optional): The permission level for the user within the specific container. Defaults to 'containerPermissionUnspecified'. Valid options are:
      - 'containerPermissionUnspecified': Unspecified permission level (not recommended).
      - 'approve': Allows approving container versions.
      - 'edit': Allows editing the container content.
      - 'noAccess': Revokes any access to the container.
      - 'publish': Allows publishing container versions.
      - 'read': Allows viewing the container content.

  Returns:
    dict: The newly created or updated user access object as a dictionary.
  """

  access_list_for_this_account = list_tag_manager_accesses(account_id=account_id)

  extract_current_user_access = next((
    access for access
    in access_list_for_this_account.get('user_permissions',[])
    if access.get('emailAddress') == user_email
  ), None)

  if extract_current_user_access:
    response = update_tag_manager_user_access(
      account_id=account_id,
      container_id=container_id,
      user_email=user_email,
      account_permission=account_permission,
      container_permission=container_permission,
      user_permission_id=extract_current_user_access['path'].split('/')[-1]
    )
  else:
    response = create_tag_manager_user_access(
      account_id=account_id,
      container_id=container_id,
      user_email=user_email,
      account_permission=account_permission,
      container_permission=container_permission
    )
  
  return response