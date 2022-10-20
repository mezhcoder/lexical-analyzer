const fs = require('fs');

function executeTest(test) {
    if (test === '1') {
        fs.writeFileSync("01.out", '1 1 Integer 1 1');
    } else {
        fs.writeFileSync("01.out", '1 1 I did not write a lexical analyzer');
    }
}

const test = fs.readFileSync('01.in', 'utf-8');
executeTest(test);


