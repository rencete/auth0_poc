def is_mfa(userinfo):
    result = False
    if userinfo.get('amr') and 'mfa' in userinfo.get('amr'):
        result = True
    return result