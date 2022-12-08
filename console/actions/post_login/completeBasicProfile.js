const PROFILE_STATES = {
  NEW: "NEW",
  BASIC: "BASIC",
  UPDATED: "UPDATED",
  MIGRATED: "MIGRATED"
};

exports.onExecutePostLogin = async (event, api) => {
  if (event.user.app_metadata && event.user.app_metadata.profile_state && event.user.app_metadata.profile_state === PROFILE_STATES.NEW) {
    const token = api.redirect.encodeToken({
      secret: event.secrets.HS256_SHARED_SECRET,
      payload: {
        aud: event.secrets.AUDIENCE,
      }
    });

    api.redirect.sendUserTo(event.secrets.BASIC_PROFILE_URL, {
      query: { token: token }
    });
  }
};

exports.onContinuePostLogin = async (event, api) => {
  // Note: payload will include the whole token, including mandatory claims
  const payload = api.redirect.validateToken({
    secret: event.secrets.HS256_SHARED_SECRET,
    tokenParameterName: 'token'
  });

  if (event.user.app_metadata && event.user.app_metadata.profile_state && event.user.app_metadata.profile_state === PROFILE_STATES.NEW) {
    api.user.setAppMetadata('profile_state', PROFILE_STATES.BASIC)
  };
};
