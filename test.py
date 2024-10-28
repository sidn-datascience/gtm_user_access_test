from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

def create_tag_manager_user_access(
  account_id:str,
  container_id:str,
  user_email:str,
  account_permission:str = ' accountPermissionUnspecified',
  container_permission:str = ' containerPermissionUnspecified'
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


response = create_tag_manager_user_access(
  account_id='',
  container_id='',
  user_email='',
  account_permission='',
  container_permission=''
)
print(response)