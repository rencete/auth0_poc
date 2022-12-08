exports.onExecutePostLogin = async (event, api) => {
    const PROFILE_STATES = {
      NEW: "NEW",
      BASIC: "BASIC",
      UPDATED: "UPDATED",
      MIGRATED: "MIGRATED"
    };

    if (event.user.app_metadata) {
        if (!event.user.app_metadata.profile_state) {
            api.user.setAppMetadata("profile_state", PROFILE_STATES.MIGRATED);
            api.idToken.setCustomClaim("profile_state", PROFILE_STATES.MIGRATED);
        } else {
            api.idToken.setCustomClaim("profile_state", event.user.app_metadata.profile_state);
        }        
    };

    if (event.user.user_metadata) {
        api.idToken.setCustomClaim("user_metadata", event.user.user_metadata);
    };
};