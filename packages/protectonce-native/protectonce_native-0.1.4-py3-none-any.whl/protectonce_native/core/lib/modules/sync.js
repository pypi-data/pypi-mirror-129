const Config = require('../utils/config');
const Constants = require('../utils/constants');
const ReportCache = require('../reports/reports_cache');
const RestAPI = require('../backend/restAPI');
const RulesManager = require('../rules/rules_manager');

let intervalId = null;

function stopHeartBeatTimer(statusCode) {
    if (intervalId === null || statusCode !== Constants.APP_DELETE_STATUS_CODE) {
        return;
    }

    clearInterval(intervalId);
    intervalId = null;
}

function syncRules() {
    return new Promise((resolve, reject) => {
        const heartbeatInfo = {};
        heartbeatInfo[Constants.HEARTBEAT_HASH_KEY] = RulesManager.hash;
        heartbeatInfo[Constants.HEARTBEAT_REPORT_KEY] = ReportCache.flush();

        if (RulesManager.isAppDeleted()) {
            stopHeartBeatTimer(Constants.APP_DELETE_STATUS_CODE);
            resolve([]);
            return;
        }

        const restApi = new RestAPI(Constants.REST_API_HEART_BEAT, heartbeatInfo);
        restApi.post().then((rulesData) => {
            RulesManager.handleIncomingRules(rulesData);
            resolve(RulesManager.runtimeRules);
            stopHeartBeatTimer(rulesData.statusCode);
        }).catch((e) => {
            console.log(`syncRules failed with error: ${e}`);
            reject(e);
        })
    });
}


function startHeartbeatTimer() {
    // Send heartbeat every n seconds as defined by Config.syncInterval
    intervalId = setInterval(syncRules, Config.syncInterval);
    intervalId.unref();
}

module.exports = startHeartbeatTimer;
