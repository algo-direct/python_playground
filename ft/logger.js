
const moment = require('moment');
const path = require("path");
const iv_utils = require('./iv_utils');
const winston = require('winston');
// const { createLogger, format, transports } = require('winston');
// const { combine, timestamp, label, printf } = format;

const local_ts = () => {
    return iv_utils.dateTimeToString(new Date());
};

const myFormat = winston.format.printf(({ level, message, timestamp }) => {
    return `${timestamp} [${level}]: ${message}`;
});

module.exports = (name, log_level = 'debug') => {
    const logfile_name = `logs/${path.basename(name)}_${moment().format('YYYYMMDD_hhmmss')}.log`;
    return winston.createLogger({
        format: winston.format.combine(
            winston.format.timestamp({ format: local_ts }),
            myFormat
        ),
        level: log_level,
        transports: [
            new (winston.transports.Console)({ json: false }),
            new winston.transports.File({ filename: logfile_name, json: false })
        ],
        // exceptionHandlers: [
        //     new (winston.transports.Console)({ json: false, timestamp: true }),
        //     new winston.transports.File({ filename: __dirname + '/exceptions.log', json: false })
        // ],
        exitOnError: false
    });
};

// const pino = require('pino');

// module.exports = name => {
//     const logfile_name = `${path.basename(name)}_${moment().format('YYYYMMDD_hhmmss')}.log`;
//     return pino({
//         name: name,
//         level: process.env.LOG_LEVEL || 'debug',
//         redact: {
//             paths: ['password', 'token'],
//         },
//         //timestamp: pino.stdTimeFunctions.isoTime,
//     }
//         ,
//         pino.destination(logfile_name)
//     );
// }
