const _ = require('lodash');

require('./init')();

const Severity = {
    OPEN_RASP_SEVERITY_MINOR: 'minor',
    OPEN_RASP_SEVERITY_MAJOR: 'major',
    OPEN_RASP_SEVERITY_CRITICAL: 'critical'
};

function _toRASPQueryParams(queryParams) {
    Object.keys(queryParams).forEach(key => {
        if (_.isString(queryParams[key])) {
            // open rasp expects each parameter to be an array of strings
            queryParams[key] = [queryParams[key]];
        }
    })
    return queryParams;
}

function _toOpenRASPContext(context) {
    // TODO: Add json data as well
    const server = {
        os: process.platform
    }
    return {
        'header': context['headers'] || {},
        'parameter': _toRASPQueryParams(context['queryParams'] || {}),
        'server': server,
        'appBasePath': context['appBasePath'],
        'get_all_parameter': context['get_all_parameter'],
        'url': context['url'],
        'json': context['json'] || {}
    }
}


// FIXME: Need to move this to backend. Agent should report confidence instead
function _getSeverity(result) {
    const confidence = result['confidence'] || 0;
    if (confidence <= 60) {
        return Severity.OPEN_RASP_SEVERITY_MINOR;
    }

    if (confidence <= 90) {
        return Severity.OPEN_RASP_SEVERITY_MAJOR;
    }

    return Severity.OPEN_RASP_SEVERITY_CRITICAL;
}

/* expects context of the form:
 *  {
 *      "headers": {<key value pair of headers>},
 *      "queryParams": {<key value pair of query parameters>},
 *  }
*/
function detectSQLi(query, callStack, context) {
    const results = RASP.check('sql', {
        query: query,
        stack: callStack || []
    }, _toOpenRASPContext(context));

    if (results.length === 0) {
        return null;
    }

    return {
        'name': results[0].algorithm || '',
        'message': results[0].message || '',
        'severity': _getSeverity(results[0])
    }
}

function detectLFI(type, source, dest, path, realpath, filename, stack, url, context) {
    const results = RASP.check(type, {
        path: path,
        realpath: realpath,
        filename: filename,
        source: source,
        dest: dest,
        stack: stack,
        url: url
    }, _toOpenRASPContext(context));

    if (results.length === 0) {
        return null;
    }

    return {
        'name': results[0].algorithm || '',
        'message': results[0].message || '',
        'severity': _getSeverity(results[0])
    }
}

function detectShellShock(command, stack, context) {
    const results = RASP.check('command', {
        command: command,
        stack: stack
    }, _toOpenRASPContext(context));

    if (results.length === 0) {
        return null;
    }

    return {
        'name': results[0].algorithm || '',
        'message': results[0].message || '',
        'severity': _getSeverity(results[0])
    }
}

function detectSsrf(url, hostname, ip, origin_ip, origin_hostname, context) {
    const results = RASP.check('ssrf', {
        url: url,
        hostname: hostname,
        ip: ip,
        origin_ip: origin_ip,
        origin_hostname: origin_hostname
    }, _toOpenRASPContext(context));

    if (results.length === 0) {
        return null;
    }

    return {
        'name': results[0].algorithm || '',
        'message': results[0].message || '',
        'severity': _getSeverity(results[0])
    }
}

function detectXxe(entity, context) {
    const results = RASP.check('xxe', {
        entity: entity
    }, _toOpenRASPContext(context));

    if (results.length === 0) {
        return null;
    }

    return {
        'name': results[0].algorithm || '',
        'message': results[0].message || '',
        'severity': _getSeverity(results[0])
    }
}

module.exports = {
    detectSQLi: detectSQLi,
    detectLFI: detectLFI,
    detectShellShock: detectShellShock,
    detectSsrf: detectSsrf,
    detectXxe: detectXxe
};
