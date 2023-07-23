// import process from 'node:process';

module.exports = (logger) => {

  // process.on('beforeExit', (code) => {
  //   logger.info('Process beforeExit event with code: ', code);
  // });

  process.on('exit', (code) => {
    console.log(`About to exit with code: ${code}`);
  });

  // process.on('SIGINT', () => {
  //   logger.info('Received SIGINT.');
  //   process.exit();
  // });

  // process.on('SIGTERM', () => {
  //   logger.info('Received SIGTERM.');
  //   process.exit();
  // });
}
