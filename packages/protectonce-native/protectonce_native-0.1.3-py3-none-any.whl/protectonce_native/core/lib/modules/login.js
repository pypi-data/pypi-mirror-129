const RestAPI = require('../backend/restAPI');
const Constants = require('../utils/constants');
const Config = require('../utils/config');
const RulesManager = require('../rules/rules_manager');

function login(runtimeInfo) {
    return new Promise((resolve, reject) => {
        Config.runtimeInfo = runtimeInfo;
        const restApi = new RestAPI(Constants.REST_API_LOGIN, Config.info);

        if (RulesManager.isAppDeleted()) {
            resolve([]);
            return;
        }

        restApi.post().then((rulesData) => {
            RulesManager.handleIncomingRules(rulesData);
            resolve(RulesManager.runtimeRules);
        }).catch((e) => {
            console.log(`Login failed with error: ${e}`);
            reject(e);
        })
    });
}

module.exports = login;
