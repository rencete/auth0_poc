exports.onExecutePreUserRegistration = async (event, api) => {
  const PROFILE_STATES = {
    NEW: "NEW",
    BASIC: "BASIC",
    UPDATED: "UPDATED",
    MIGRATED: "MIGRATED"
  };

  api.user.setAppMetadata("profile_state", PROFILE_STATES.NEW);
};
