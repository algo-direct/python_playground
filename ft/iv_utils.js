const pad1zero = (n) => {
    if (n < 10) {
        return '0' + n;
    }
    return n.toString();
};

const pad2zero = (n) => {
    if (n < 10) {
        return '00' + n;
    }
    if (n < 100) {
        return '0' + n;
    }
    return n.toString();
};

const dateTimeToString = (d) => {
    return `${d.getFullYear()}${pad1zero(d.getMonth() + 1)}${pad1zero(d.getDate())}_${pad1zero(d.getHours())}${pad1zero(d.getMinutes())}${pad1zero(d.getSeconds())}.${pad2zero(d.getUTCMilliseconds())}`;
};

module.exports = {
    pad1zero, pad2zero, dateTimeToString
}
