const _ = require('lodash');

const openRASP = require('./openRASP');
const ProtectOnceContext = require('../context');
const RegExpManager = require('../../utils/regex_manager');
const Report = require('../../reports/report');
const ReportsCache = require('../../reports/reports_cache');
const RulesManager = require('../../rules/rules_manager');
const { RuntimeData, CommandData, XmlData, SsrfData, SsrfRedirectData } = require('../../runtime/runtime_data');
const { SQLData } = require('../../runtime/runtime_data');
const { FileData } = require('../../runtime/runtime_data');




function checkRegexp(data) {
    const runtimeData = new RuntimeData(data);
    const rule = RulesManager.getRule(runtimeData.context);

    if (!rule) {
        return runtimeData;
    }

    const regExpressions = rule.regExps;
    let match = false;
    const args = runtimeData.args;
    for (let regExpId of regExpressions) {
        const regExp = RegExpManager.getRegExp(regExpId);

        // TODO: Use args from the rule instead of scanning all args
        for (let arg of args) {
            // FIXME: What about arguments which are other than string
            if (!_.isString(arg)) {
                continue;
            }

            if (arg.search(regExp) >= 0) {
                match = true;
                break;
            }
        }

        if (match === true) {
            break;
        }
    }

    if (match) {
        let reportType = Report.ReportType.REPORT_TYPE_ALERT;
        runtimeData.message = 'ProtectOnce has detected an attack';

        if (rule.shouldBlock === true) {
            runtimeData.setBlock();
            reportType = Report.ReportType.REPORT_TYPE_BLOCK;
            runtimeData.message = 'ProtectOnce has blocked an attack'
        } else {
            runtimeData.setAlert();
        }

        const report = new Report.Report(reportType, runtimeData.message);
        ReportsCache.cache(report);
    }

    return runtimeData;
}

function detectSQLi(data) {
    const sqlData = new SQLData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        return sqlData;
    }

    const context = ProtectOnceContext.get(sqlData.sessionId);
    const result = openRASP.detectSQLi(sqlData.query, sqlData.callStack, context);
    if (!result) {
        return sqlData;
    }

    let reportType = Report.ReportType.REPORT_TYPE_ALERT;
    if (rule.shouldBlock === true) {
        sqlData.setBlock();
        reportType = Report.ReportType.REPORT_TYPE_BLOCK;
    } else {
        sqlData.setAlert();
    }
    const report = new Report.Report(rule.id, result.name, result.severity, context.sourceIP, result.message, result.name, context.path);
    ReportsCache.cache(report);

    return sqlData;
}

function executeLFI(lfiType, data, fileData) {

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        return fileData;
    }
    const context = ProtectOnceContext.get(fileData.sessionId);
    const result = openRASP.detectLFI(lfiType, fileData.source, fileData.dest, fileData.path, fileData.realpath, fileData.filename, fileData.stack, fileData.url, context);
    if (!result) {
        return fileData;
    }
    let reportType = Report.ReportType.REPORT_TYPE_ALERT;
    if (rule.shouldBlock === true) {
        fileData.setBlock();
        reportType = Report.ReportType.REPORT_TYPE_BLOCK;
    } else {
        fileData.setAlert();
    }
    const report = new Report.Report(rule.id, result.name, result.severity, context.sourceIP, result.message, result.name, context.path);
    ReportsCache.cache(report);
    return fileData;

}

function detectOpenFileLFI(data) {
    const fileData = new FileData(data.data);
    if (fileData.mode && fileData.mode.toLowerCase() === 'read') {
        return executeLFI('readFile', data, fileData);
    } else if (fileData.mode && fileData.mode.toLowerCase() === 'write') {
        return executeLFI('writeFile', data, fileData);
    }
}


function detectUploadFileLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('fileUpload', data, fileData);
}

function detectDeleteFileLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('deleteFile', data, fileData);
}

function detectRenameFileLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('rename', data, fileData);
}


function detectListDirectoryLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('directory', data, fileData);
}

function detectIncludeLFI(data) {
    const fileData = new FileData(data.data);
    return executeLFI('include', data, fileData);
}

function detectShellShock(data) {
    const commandData = new CommandData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        return commandData;
    }

    const context = ProtectOnceContext.get(commandData.sessionId);
    const result = openRASP.detectShellShock(commandData.command, commandData.stack, context);
    if (!result) {
        return commandData;
    }

    let reportType = Report.ReportType.REPORT_TYPE_ALERT;
    if (rule.shouldBlock === true) {
        commandData.setBlock();
        reportType = Report.ReportType.REPORT_TYPE_BLOCK;
    } else {
        commandData.setAlert();
    }
    const report = new Report.Report(rule.id, result.name, result.severity, context.sourceIP, result.message, result.name, context.path);
    ReportsCache.cache(report);

    return commandData;
}

function detectSsrf(data) {
    const ssrfData = new SsrfData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        return ssrfData;
    }

    const context = ProtectOnceContext.get(ssrfData.sessionId);
    const result = openRASP.detectSsrf(ssrfData.url, ssrfData.hostname, ssrfData.ip, ssrfData.origin_ip, ssrfData.origin_hostname, context);
    if (!result) {
        return ssrfData;
    }

    let reportType = Report.ReportType.REPORT_TYPE_ALERT;
    if (rule.shouldBlock === true) {
        ssrfData.setBlock();
        reportType = Report.ReportType.REPORT_TYPE_BLOCK;
    } else {
        ssrfData.setAlert();
    }
    const report = new Report.Report(rule.id, result.name, result.severity, context.sourceIP, result.message, result.name, context.path);
    ReportsCache.cache(report);

    return ssrfData;
}


function detectXxe(data) {
    const xmlData = new XmlData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        return xmlData;
    }

    const context = ProtectOnceContext.get(xmlData.sessionId);
    const result = openRASP.detectXxe(xmlData.entity, context);
    if (!result) {
        return xmlData;
    }

    let reportType = Report.ReportType.REPORT_TYPE_ALERT;
    if (rule.shouldBlock === true) {
        xmlData.setBlock();
        reportType = Report.ReportType.REPORT_TYPE_BLOCK;
    } else {
        xmlData.setAlert();
    }
    const report = new Report.Report(rule.id, result.name, result.severity, context.sourceIP, result.message, result.name, context.path);
    ReportsCache.cache(report);

    return xmlData;
}


function detectSsrfRedirect(data) {
    const ssrfRedirectData = new SsrfRedirectData(data.data);

    const rule = RulesManager.getRule(data.context);
    if (!rule) {
        return ssrfRedirectData;
    }

    const context = ProtectOnceContext.get(ssrfRedirectData.sessionId);
    const result = openRASP.detectSsrfRedirect(ssrfRedirectData.hostname, ssrfRedirectData.ip, ssrfRedirectData.url, ssrfRedirectData.url2, ssrfRedirectData.hostname2,
        ssrfRedirectData.ip2, ssrfRedirectData.port2, context);
    if (!result) {
        return ssrfRedirectData;
    }

    let reportType = Report.ReportType.REPORT_TYPE_ALERT;
    if (rule.shouldBlock === true) {
        ssrfRedirectData.setBlock();
        reportType = Report.ReportType.REPORT_TYPE_BLOCK;
    } else {
        ssrfRedirectData.setAlert();
    }
    const report = new Report.Report(rule.id, result.name, result.severity, context.sourceIP, result.message, result.name, context.path);
    ReportsCache.cache(report);

    return ssrfRedirectData;
}

module.exports = {
    checkRegexp: checkRegexp,
    detectSQLi: detectSQLi,
    detectOpenFileLFI: detectOpenFileLFI,
    detectUploadFileLFI: detectUploadFileLFI,
    detectDeleteFileLFI: detectDeleteFileLFI,
    detectRenameFileLFI: detectRenameFileLFI,
    detectListDirectoryLFI: detectListDirectoryLFI,
    detectIncludeLFI: detectIncludeLFI,
    detectShellShock: detectShellShock,
    detectSsrf: detectSsrf,
    detectXxe: detectXxe,
    detectSsrfRedirect: detectSsrfRedirect
}
