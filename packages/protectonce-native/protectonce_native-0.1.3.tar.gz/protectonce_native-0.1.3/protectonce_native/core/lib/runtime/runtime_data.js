const RuntimeAction = {
    RUNTIME_ACTION_NONE: 'none',
    RUNTIME_ACTION_ALERT: 'alert',
    RUNTIME_ACTION_BLOCK: 'block'
};

class RuntimeData {
    constructor(runtimeData) {
        this.args = runtimeData.args || [];
        this.context = runtimeData.context || '';
        this.action = RuntimeAction.RUNTIME_ACTION_NONE;
        this.message = runtimeData.message || '';
        this.result = runtimeData.result || null;
        this.modifyArgs = runtimeData.modifyArgs || {};
        this.callStack = runtimeData.callStack || [];
    }

    setBlock() {
        this.action = RuntimeAction.RUNTIME_ACTION_BLOCK;
    }

    setAlert() {
        this.action = RuntimeAction.RUNTIME_ACTION_ALERT;
    }
}

class RASPData extends RuntimeData {
    constructor(raspData) {
        super(raspData);
        this.confidence = 0;
        this.sessionId = raspData.poSessionId || '';
    }
}

class SQLData extends RASPData {
    constructor(sqlData) {
        super(sqlData);
        this.query = sqlData.query;
    }

    get params() {
        return {
            'query': this.query,
            'stack': this.callStack
        };
    }
}

class FileData extends RASPData {
    constructor(fileData) {
        super(fileData);
        this.path = fileData.path;
        this.realpath = fileData.realpath;
        this.filename = fileData.filename;
        this.source = fileData.source;
        this.dest = fileData.dest;
        this.stack = fileData.stack;
        this.url = fileData.url;
        this.mode = fileData.mode;
    }

    get params() {
        return {
            'path': this.path,
            'realpath': this.realpath,
            'stack': this.callStack
        };
    }
}

class CommandData extends RASPData {
    constructor(commandData) {
        super(commandData)
        this.command = commandData.command;
        this.stack = commandData.stack;
    }

    get params() {
        return {
            'command': this.command,
            'stack': this.stack,
            'callStack': this.callStack
        };
    }
}

class XmlData extends RASPData {
    constructor(xmlData) {
        super(xmlData)
        this.entity = xmlData.entity;
    }

    get params() {
        return {
            'entity': this.entity,
            'callStack': this.callStack
        };
    }
}

module.exports = {
    RuntimeData: RuntimeData,
    SQLData: SQLData,
    FileData: FileData,
    CommandData: CommandData,
    XmlData: XmlData
};
