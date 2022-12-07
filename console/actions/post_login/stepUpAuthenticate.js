exports.onExecutePostLogin = async (event, api) => {
    if (event.request.query.acr_values && event.request.query.acr_values === 'http://schemas.openid.net/pape/policies/2007/06/multi-factor') {
        api.multifactor.enable('any', { allowRememberBrowser: false });
    };
};