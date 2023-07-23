
const { spawn } = require('child_process');

const child1 = spawn('node', ['ft_key_receiver.js']);

child1.stdout.on('data', (data) => {
  console.log(`child1 stdout:\n${data}`);
});

child1.stderr.on('data', (data) => {
  console.error(`child1 stderr:\n${data}`);
});

child1.on('exit', function (code, signal) {
  console.log('child1 process exited with ' +
              `code ${code} and signal ${signal}`);
});

const child2 = spawn('node', ['totp.js']);

child2.stdout.on('data', (data) => {
  console.log(`child2 stdout:\n${data}`);
});

child2.stderr.on('data', (data) => {
  console.error(`child2 stderr:\n${data}`);
});

child2.on('exit', function (code, signal) {
  console.log('child2 process exited with ' +
              `code ${code} and signal ${signal}`);
});
