const appUrl = 'localhost:8000';
const redirectUrl = `http://${appUrl}/authenticate/answer_security_question`;
const providerUrl = `http://${appUrl}/providers/security_question`;
const promptTtl = 1000 * 60 * 60; // security answer is valid for 1 hour (session length)

exports.onExecutePostLogin = async (event, api) => {
  if (event.user.user_metadata?.security_answer) {
    // A security question/answer has already been defined and can therefore be checked

    // Check if there is a valid security question session (ie. security question/answer given correctly in last X minutes)
    const securityQuestionMethod = event.authentication?.methods.find((record) => validateSecurityQuestionRecord(record, providerUrl, promptTtl));
    if (!securityQuestionMethod) {
      // No valid security question/answer session, proceed to ask user
      const token = api.redirect.encodeToken({
        secret: event.secrets.HS256_SHARED_SECRET,
        payload: {
          aud: event.client.client_id,
          attempts: 0,
        }
      });

      api.redirect.sendUserTo(redirectUrl, {
        query: { token: token }
      });
    }
  }

  // no security question/answer yet, just proceed to login
};


exports.onContinuePostLogin = async (event, api) => {
  // NOTE: using cache to store number of attempts is not a good idea
  //       the cache seems to be inconsistent when retrieving/clearing data stored
  const maxAttempts = 3
  // const cacheKey = 'securityAnswerAttempts'

  // Note: payload will include the whole token, including mandatory claims
  const payload = api.redirect.validateToken({
    secret: event.secrets.HS256_SHARED_SECRET,
    tokenParameterName: 'token'
  });

  // check if the hash is the same as what is stored
  if (payload.answer_hash !== event.user.user_metadata?.security_answer) {
    // answer did not match, ask the user to try again if not yet exceeding max tries

    // retrieve number of attempts
    // const cache_data = api.cache.get(cacheKey);
    // const numAttempts = parseInt((cache_data?.value) || 0) + 1;
    const numAttempts = payload.attempts || 1

    if (numAttempts < maxAttempts) {
      // max attempts not yet reached, prompt user to try again

      // api.cache.set(cacheKey, numAttempts.toString());

      // redirect back to form
      const token = api.redirect.encodeToken({
        secret: event.secrets.HS256_SHARED_SECRET,
        payload: {
          aud: event.client.client_id,
          attempts: numAttempts,
        }
      });

      api.redirect.sendUserTo(redirectUrl, {
        query: { token: token }
      });
      return
    }

    // api.cache.delete(cacheKey);
    api.access.deny("Security answer failed.");
    return
  }

  // hash is the same

  // delete/clean-up cache first
  // api.cache.delete(cacheKey);

  // set custom provider
  api.authentication.recordMethod(providerUrl);

  // continue to login
};


function validateSecurityQuestionRecord(record, url, ttl) {
  if (!record) {
    // No record means it isn't valid.
    return false;
  }

  // NOTE: example shows record.url, but this is not correct
  //       actual field is "name" and not "url"
  if (record.name !== url) {
    // This isn't a record of our custom method.
    return false;
  }

  // Timestamps are rendered as ISO8601 strings.
  const timestamp = new Date(record.timestamp);

  // The record is valid if it was recorded recently enough.
  return timestamp.valueOf() >= Date.now() - ttl;
}