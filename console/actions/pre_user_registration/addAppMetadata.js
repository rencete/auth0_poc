exports.onExecutePreUserRegistration = async (event, api) => {
  const PROFILE_STATES = {
    NEW: "NEW",
    UPDATED: "UPDATED",
    MIGRATED: "MIGRATED"
  };

  api.user.setAppMetadata("profile_state", PROFILE_STATES.NEW);
};
