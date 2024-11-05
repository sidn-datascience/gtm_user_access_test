from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from pprint import pprint as print

SERVICE_ACCOUNT_FILE = './service_account.json'
SCOPES = [
  'https://www.googleapis.com/auth/tagmanager.manage.users',
  'https://www.googleapis.com/auth/tagmanager.readonly'
]

def get_credentials(service_account_file:str, scopes:list[str]) -> Credentials:
  creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
  return creds

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
  creds = get_credentials(SERVICE_ACCOUNT_FILE, SCOPES)

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
  creds = get_credentials(SERVICE_ACCOUNT_FILE, SCOPES)

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

def lookup_container_by_container_tag_id(container_tag_id:str) -> dict:
  """Looks up a container by its container tag ID.

  Args:
      container_tag_id (str): The unique identifier of the container.

  Returns:
      A dictionary representing the container information, or None if not found.
  """

  creds = get_credentials(SERVICE_ACCOUNT_FILE, SCOPES)
  service = build('tagmanager', 'v2', credentials=creds)

  container = service.accounts().containers().lookup(tagId=container_tag_id).execute()
  return container

def list_tag_manager_accesses(account_id:str) -> dict:
  """Lists the accesses for a given Tag Manager account.

  Args:
    account_id (str): The ID of the Tag Manager account.

  Returns:
    dict: The updated user access object as a dictionary.
  """
  creds = get_credentials(SERVICE_ACCOUNT_FILE, SCOPES)

  service = build('tagmanager', 'v2', credentials=creds)

  request = service.accounts().user_permissions().list(
    parent=f"accounts/{account_id}"
  )

  response = request.execute()
  return response

def add_or_update_permission(
  account_id:str,
  user_email:str,
  account_permission:str,
  container_permission:str,
  container_id:str | None  = None,
  container_tag_id:str | None = None,
) -> dict:
  """Adds or updates the access of an existing user for a given Tag Manager account and container.

  Args:
    account_id (str): The ID of the Tag Manager account.
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
    container_id (str or None): The ten digits ID of the Tag Manager container.
    container_tag_id (str or None): The Tag ID of the Tag Manager container, example: GTM-12345.

  Returns:
    dict: The newly created or updated user access object as a dictionary.
  """

  if container_id == None and container_tag_id == None:
    raise Exception('At least a "container_id" or "container_tag_id" must be specified.')
  
  if container_tag_id:
    if not container_tag_id.startswith('GTM-'):
      raise Exception("Invalid Container Tag ID. Must be somethink like GTM-XXXXXX")
    
    container = lookup_container_by_container_tag_id(container_tag_id=container_tag_id)
    container_id = container['containerId']

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