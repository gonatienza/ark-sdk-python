---
title: SDK examples
description: SDK Examples
---

# SDK examples

This page lists some useful SDK examples.

## Authenticate and read tenant DB policies

```python
from ark_sdk_python.auth import ArkISPAuth
from ark_sdk_python.models.auth import ArkSecret, ArkAuthMethod, ArkAuthProfile, IdentityArkAuthMethodSettings
from ark_sdk_python.services.sia.policies.db import ArkSIADBPoliciesService

if __name__ == "__main__":
    isp_auth = ArkISPAuth()
    isp_auth.authenticate(
        auth_profile=ArkAuthProfile(
            username='tina@cyberark.cloud.12345', auth_method=ArkAuthMethod.Identity, auth_method_settings=IdentityArkAuthMethodSettings()
        ),
        secret=ArkSecret(secret='CoolPassword'),
    )
    db_policies_service = ArkSIADBPoliciesService(isp_auth)
    policies = db_policies_service.list_policies()
```

## Authenticate and provision SIA databases and policy and connector

```python
if __name__ == '__main__':
    ArkSystemConfig.disable_verbose_logging()
    # Authenticate to the tenant with an auth profile to configure SIA
    username = 'user@cyberark.cloud.12345'
    print(f'Authenticating to the created tenant with user [{username}]')
    isp_auth = ArkISPAuth()
    isp_auth.authenticate(
        auth_profile=ArkAuthProfile(
            username=username, auth_method=ArkAuthMethod.Identity, auth_method_settings=IdentityArkAuthMethodSettings()
        ),
        secret=ArkSecret(secret='CoolPassword'),
    )

    # Create SIA DB Secret, Database, Connector and DB Policy
    sia_service = ArkSIAAPI(isp_auth)
    print('Adding SIA DB User Secret')
    secret = sia_service.secrets_db.add_secret(
        ArkSIADBAddSecret(secret_type=ArkSIADBSecretType.UsernamePassword, username='Administrator', password='CoolPassword')
    )
    print('Adding SIA Database')
    sia_service.workspace_db.add_database(
        ArkSIADBAddDatabase(
            name='mydomain.com',
            provider_engine=ArkSIADBDatabaseEngineType.PostgresSH,
            secret_id=secret.secret_id,
            read_write_endpoint="myendpoint.mydomain.com",
        )
    )
    print('Installing SIA Connector')
    sia_service.access.install_connector(
        ArkSIAInstallConnector(
            connector_os=ArkOsType.LINUX,
            connector_type=ArkWorkspaceType.ONPREM,
            connector_pool_id='pool_id',
            target_machine='1.2.3.4',
            username='root',
            private_key_path='/path/to/private.pem',
        )
    )
    print('Adding SIA DB Policy')
    sia_service.policies_db.add_policy(
        ArkSIADBAddPolicy(
            policy_name='IT Policy',
            status=ArkSIARuleStatus.Enabled,
            description='IT Policy',
            providers_data=ArkSIADBProvidersData(
                postgres=ArkSIADBPostgres(
                    resources=['postgres-onboarded-asset'],
                ),
            ),
            user_access_rules=[
                ArkSIADBAuthorizationRule(
                    rule_name='IT Rule',
                    user_data=ArkSIAUserData(roles=['DpaAdmin'], groups=[], users=[]),
                    connection_information=ArkSIADBConnectionInformation(
                        grant_access=2,
                        idle_time=10,
                        full_days=True,
                        hours_from='07:00',
                        hours_to='17:00',
                        time_zone='Asia/Jerusalem',
                        connect_as=ArkSIADBConnectAs(
                            db_auth=[
                                ArkSIADBLocalDBAuth(
                                    roles=['rds_superuser'],
                                    applied_to=[
                                        ArkSIADBAppliedTo(
                                            name='postgres-onboarded-asset',
                                            type=ArkSIADBResourceIdentifierType.RESOURCE,
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ),
                )
            ],
        )
    )
```

## Authenticate and provision SIA VM policies

```python
if __name__ == '__main__':
    isp_auth = ArkISPAuth()
    isp_auth.authenticate(
        auth_profile=ArkAuthProfile(
            username=username, auth_method=ArkAuthMethod.Identity, auth_method_settings=IdentityArkAuthMethodSettings()
        ),
        secret=ArkSecret(secret='CoolPassword'),
    )
    print('Adding SIA Policy')
    sia_service.policies.add_policy(
        ArkSIAVMAddPolicy(
            policy_name='IT Policy',
            description='IT Policy',
            status=ArkSIARuleStatus.Enabled,
            providers_data={
                ArkWorkspaceType.AWS: ArkSIAVMAWSProviderData(
                    account_ids=['965428623928'], tags=[{'key': 'team', 'value': 'IT'}], regions=[], vpc_ids=[]
                )
            },
            user_access_rules=[
                ArkSIAVMAuthorizationRule(
                    rule_name='IT Rule',
                    user_data=ArkSIAUserData(roles=['IT']),
                    connection_information=ArkSIAVMConnectionInformation(
                        full_days=True,
                        days_of_week=[],
                        time_zone='Asia/Jerusalem',
                        connect_as={
                            ArkWorkspaceType.AWS: {
                                ArkProtocolType.SSH: 'root',
                                ArkProtocolType.RDP: ArkSIAVMRDPLocalEphemeralUserConnectionData(
                                    local_ephemeral_user=ArkSIAVMLocalEphemeralUserConnectionMethodData(assign_groups={'Administrators'})
                                ),
                            }
                        },
                    ),
                )
            ],
        )
    )
```

## Authenticate and provision SIA VM RDP Target Set / Secret / Policy / Connector

```python
if __name__ == '__main__':
    ArkSystemConfig.disable_verbose_logging()
    # Authenticate to the tenant with an auth profile to configure SIA
    username = 'user@cyberark.cloud.12345'
    print(f'Authenticating to the created tenant with user [{username}]')
    isp_auth = ArkISPAuth()
    isp_auth.authenticate(
        auth_profile=ArkAuthProfile(
            username=username, auth_method=ArkAuthMethod.Identity, auth_method_settings=IdentityArkAuthMethodSettings()
        ),
        secret=ArkSecret(secret='CoolPassword'),
    )

    # Create SIA VM Secret, Target Set and VM Policy
    sia_service = ArkSIAAPI(isp_auth)
    print('Adding SIA VM User Secret')
    secret = sia_service.secrets_vm.add_secret(
        ArkSIAVMAddSecret(
            secret_type=ArkSIAVMSecretType.ProvisionerUser, 
            provisioner_username='Administrator', 
            provisioner_password='CoolPassword',
        ),
    )
    print('Installing SIA Connector')
    sia_service.access.install_connector(
        ArkSIAInstallConnector(
            connector_os=ArkOsType.LINUX,
            connector_type=ArkWorkspaceType.ONPREM,
            connector_pool_id='pool_id',
            target_machine='1.2.3.4',
            username='root',
            private_key_path='/path/to/private.pem',
        )
    )
    print('Adding SIA Target Set')
    sia_service.workspace_target_sets.add_target_set(
        ArkSIAAddTargetSet(
            name='mydomain.com',
            secret_type=ArkSIAVMSecretType.ProvisionerUser,
            secret_id=secret.secret_id,
        )
    )
    print('Adding SIA VM Policy')
    sia_service.policies_vm.add_policy(
        ArkSIAVMAddPolicy(
            policy_name='IT Policy',
            status=ArkSIARuleStatus.Enabled,
            description='IT Policy',
            providers_data={
                ArkWorkspaceType.ONPREM: ArkSIAVMOnPremProviderData(
                    fqdn_rules=[
                        ArkSIAVMFQDNRule(
                            operator=ArkSIAVMFQDNOperator.WILDCARD,
                            computername_pattern='*',
                            domain='mydomain.com',
                        ),
                    ],
                ),
            },
            user_access_rules=[
                ArkSIAVMAuthorizationRule(
                    rule_name='IT Rule',
                    user_data=ArkSIAUserData(roles=['DpaAdmin'], groups=[], users=[]),
                    connection_information=ArkSIAVMConnectionInformation(
                        grant_access=2,
                        idle_time=10,
                        full_days=True,
                        hours_from='07:00',
                        hours_to='17:00',
                        time_zone='Asia/Jerusalem',
                        connect_as={
                            ArkWorkspaceType.ONPREM: {
                                ArkProtocolType.RDP: ArkSIAVMRDPLocalEphemeralUserConnectionData(
                                    local_ephemeral_user=ArkSIAVMLocalEphemeralUserConnectionMethodData(
                                        assign_groups=[
                                            'Administrators'
                                        ],
                                    ),
                                ),
                            },
                        },
                    ),
                )
            ],
        )
    )
    print('Finished Successfully')
```

## View Session Monitoring Sessions And Activities Per Session

```python
from ark_sdk_python.services.sm import ArkSMService
from ark_sdk_python.models.services.sm import ArkSMSessionsFilter, ArkSMGetSession, ArkSMGetSessionActivities
from ark_sdk_python.models.ark_profile import ArkProfileLoader
from ark_sdk_python.models.common import ArkProtocolType
from ark_sdk_python.auth import ArkISPAuth
from datetime import datetime, timedelta

if __name__ == "__main__":
    isp_auth = ArkISPAuth()
    isp_auth.authenticate(
        profile=ArkProfileLoader().load_default_profile()
    )
    sm: ArkSMService = ArkSMService(isp_auth)
    search_by = 'startTime ge {start_time_from} AND sessionDuration GE {min_duration} AND protocol IN {protocols}'
    search_by = search_by.format(
        start_time_from=(datetime.utcnow() - timedelta(days=30)).isoformat(timespec='seconds'),
        min_duration='00:00:01',
        protocols=','.join([ArkProtocolType.DB[0], ArkProtocolType.SSH[0], ArkProtocolType.RDP[0]]),
    )
    sessions_filter = ArkSMSessionsFilter(
        search=search_by,
    )
    print(f'session_count = {sm.count_sessions_by(sessions_filter)}')
    for s_page in sm.list_sessions_by(sessions_filter):
        for session in s_page.items:
            session = sm.session(ArkSMGetSession(session_id=session.session_id))
            get_session_activities = ArkSMGetSessionActivities(session_id=session.session_id)
            print(f'session = {session}, activities_count = {sm.count_session_activities(get_session_activities)}')
            session_activities = [activity for page in sm.list_session_activities(get_session_activities) for activity in page.items]
            print(session_activities)
```

## Get current tenant default suffix

```python
from ark_sdk_python.auth import ArkISPAuth
from ark_sdk_python.models.ark_profile import ArkProfileLoader
from ark_sdk_python.models.services.identity.directories import ArkIdentityListDirectoriesEntities
from ark_sdk_python.services.identity import ArkIdentityAPI

if __name__ == "__main__":
    isp_auth = ArkISPAuth()
    isp_auth.authenticate(ArkProfileLoader().load_default_profile())
    identity_api = ArkIdentityAPI(isp_auth)
    print(identity_api.identity_directories.tenant_default_suffix())
    for page in identity_api.identity_directories.list_directories_entities(ArkIdentityListDirectoriesEntities()):
        print([i.name for i in page.items])
```


## Add identity role and user

```python
from ark_sdk_python.models.auth import (
    ArkAuthMethod,
    ArkAuthProfile,
    ArkSecret,
    IdentityArkAuthMethodSettings,
)
from ark_sdk_python.auth import ArkISPAuth
from ark_sdk_python.services.identity import ArkIdentityAPI
from ark_sdk_python.models.services.identity.roles import ArkIdentityCreateRole
from ark_sdk_python.models.services.identity.users import ArkIdentityCreateUser

if __name__ == "__main__":
    isp_auth = ArkISPAuth()
    isp_auth.authenticate(
        auth_profile=ArkAuthProfile(
            username='CoolUser', auth_method=ArkAuthMethod.Identity, auth_method_settings=IdentityArkAuthMethodSettings()
        ),
        secret=ArkSecret(secret='CoolPassword'),
    )

    # Create an identity service to create some users and roles
    print('Creating identity roles and users')
    identity_api = ArkIdentityAPI(isp_auth)
    identity_api.identity_roles.create_role(ArkIdentityCreateRole(role_name='IT'))
    identity_api.identity_users.create_user(ArkIdentityCreateUser(username='it_user', password='CoolPassword', roles=['IT']))
```


## List PCloud Accounts

```python
import pprint

from ark_sdk_python.auth import ArkISPAuth
from ark_sdk_python.models.auth import ArkAuthMethod, ArkAuthProfile, ArkSecret, IdentityArkAuthMethodSettings
from ark_sdk_python.services.pcloud.accounts import ArkPCloudAccountsService

if __name__ == '__main__':
    isp_auth = ArkISPAuth(cache_authentication=False)
    isp_auth.authenticate(
        auth_profile=ArkAuthProfile(
            username='smarom@cyberark.cloud.84573',
            auth_method=ArkAuthMethod.Identity,
            auth_method_settings=IdentityArkAuthMethodSettings(),
        ),
        secret=ArkSecret(secret="CoolPassword"),
    )
    accounts_service = ArkPCloudAccountsService(isp_auth=isp_auth)
    for page in accounts_service.list_accounts():
        for item in page:
            pprint.pprint(item.model_dump())
```
