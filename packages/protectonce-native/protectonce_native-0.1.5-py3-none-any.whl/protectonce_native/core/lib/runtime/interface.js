const login = require('../modules/login');
const rasp = require('../modules/rasp');
const httpServer = require('../modules/httpServer');
const startHeartbeatTimer = require('../modules/sync');

startHeartbeatTimer();

function stop() {
    // TODO: Implement this method and add cleanup if any
    return null;
}

function sync() {
    // TODO: Implement this method
    return null;
}

module.exports = {
    init: login,
    sync: sync,
    rasp: rasp,
    httpServer: httpServer,
    stop: stop
};
