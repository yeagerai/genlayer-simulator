import pkg from 'ncp';
const { ncp } = pkg;
import path from 'node:path';

ncp.limit = 16;

ncp(path.resolve('../examples'), path.resolve('src/assets/examples'), 
        function (err) {
    if (err) {
        return console.error(err);
    }
    console.log('Contract Examples copied');
});
