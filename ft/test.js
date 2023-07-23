

var fs = require('fs');

const iv_utils = require('./iv_utils');

const md_file_name = `ft_md_${iv_utils.dateTimeToString(new Date())}.txt`;
console.log(`md_file_name:`, md_file_name)
const md_file_stream = fs.createWriteStream(md_file_name, {
    flags: 'a'
})


md_file_stream.write("1");
md_file_stream.write("\n");
md_file_stream.write("2");
md_file_stream.write("\n");

md_file_stream.end();
console.log('fff')