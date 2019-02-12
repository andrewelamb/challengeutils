import synapseclient

def set_evaluation_permissions(syn, evaluation, principalid=None, permission_level="view"):
    """
    Convenience function to set ACL on an entity for a user or team based on
    permission levels (view, download...)

    Args:
        evaluation: An Evaluation or Evaluation id
        principalid: Identifier of a user or group (defaults to PUBLIC users)
        permission_level: Can be "view","submit","score",or "admin"
    """
    view = ["READ"]
    submit = ['READ','SUBMIT']
    score = ['READ','UPDATE_SUBMISSION','READ_PRIVATE_SUBMISSION']
    admin = ['DELETE_SUBMISSION','DELETE','SUBMIT','UPDATE','CREATE','READ','UPDATE_SUBMISSION','READ_PRIVATE_SUBMISSION','CHANGE_PERMISSIONS']
    permission_level_mapping = {'view':view,
                                'submit':submit,
                                'score':score,
                                'admin':admin}
    assert permission_level in permission_level_mapping.keys()
    assert principalid is not None
    evaluation = syn.getEvaluation(evaluation)
    syn.setPermissions(evaluation, principalId=principalid, accessType=permission_level_mapping[permission_level])

def set_entity_permissions(syn, entity, principalid=None, permission_level="view"):
    """
    Convenience function to set ACL on an entity for a user or team based on
    permission levels (view, download...)

    Args:
        entity: An Entity or Synapse ID to lookup
        principalid: Identifier of a user or group (defaults to PUBLIC users)
        permission_level: Can be "view","download","edit","edit_and_delete", "admin" or None. If None is specified, the permissions are removed from the principalid.
    """
    view = ["READ"]
    download = ['READ','DOWNLOAD']
    edit = ['DOWNLOAD', 'UPDATE', 'READ', 'CREATE']
    edit_and_delete = ['DOWNLOAD', 'UPDATE', 'READ', 'CREATE','DELETE']
    admin = ['DELETE','CHANGE_SETTINGS','MODERATE','CREATE','READ','DOWNLOAD','UPDATE','CHANGE_PERMISSIONS']
    permission_level_mapping = {'view':view,
                                'download':download,
                                'edit':edit,
                                'edit_and_delete':edit_and_delete,
                                'admin':admin,
                                'delete':[]}
    if permission_level not in permission_level_mapping.keys():
        raise ValueError("permission_level must be one of these: {0}".format(', '.join(permission_level_mapping.keys())))

    if principalid is None:
        raise ValueError("principalid must not be None")

    entityid = synapseclient.utils.id_of(entity)
    syn.setPermissions(entityid, principalId=principalid, accessType=permission_level_mapping[permission_level])
