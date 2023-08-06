const _ = require('lodash');

const Rule = require('./rule');
const Constants = require('../utils/constants');

class RulesManager {
    constructor() {
        this._rules = {};
        this._hash = '';
        this._appDeleted = false;
    }

    get rules() {
        return Object.values(this._rules);
    }

    get hash() {
        return this._hash;
    }

    get shouldMonitor() {
        return this._agentMonitoring === 'enabled';
    }

    getRule(id) {
        if (!this.shouldMonitor || this.isAppDeleted()) {
            return null;
        }

        const rule = this._rules[id];
        if (rule && rule.isEnabled) {
            return rule;
        }

        return null;
    }

    get runtimeRules() {
        // TODO: Optimise the runtime rules
        const runtimeRules = [];
        this.rules.forEach(rule => {
            runtimeRules.push(rule.runtimeRule);
        });
        return runtimeRules;
    }

    set rules(rules) {
        if (!_.isArray(rules) || rules.length === 0) {
            // Do not update rules if no rules are returned from backend
            return;
        }

        // TODO: Need to have optimized rules storage once backend starts sending rules diff
        this._rules = {};
        for (let rule of rules) {
            const ruleObj = new Rule(rule);
            this._rules[rule.id] = ruleObj;
        }
    }

    handleIncomingRules(rulesData) {
        if (_.isObject(rulesData) && rulesData['statusCode'] === Constants.APP_DELETE_STATUS_CODE) {
            this._appDeleted = true;
            return;
        }

        const rulesJson = JSON.parse(rulesData.data);
        const agentRule = rulesJson.agentRule || rulesJson.rulesSet;

        if (typeof agentRule === 'undefined' || !_.isObject(agentRule)) {
            return;
        }
        this._hash = agentRule.hash || '';
        this.rules = agentRule.hooks || [];
        this._agentMonitoring = agentRule.agentMonitoring || 'enabled';
    }

    isAppDeleted() {
        return this._appDeleted;
    }
}

module.exports = new RulesManager();
