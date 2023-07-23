
const logger = require('./logger')(__filename);
const process_util = require('./process_util')(logger);

logger.info('started')
setTimeout(() => { process.exit(0); }, 20000);
