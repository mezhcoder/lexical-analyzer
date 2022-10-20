const fs = require('fs');
const analysis = require('./analyzer');

const tests = {}
for (const nameFile of fs.readdirSync("tests")) {
    const numberTest = nameFile
        .replace('in', '')
        .replace('out', '')
        .replace('.', '')
    if (!tests.hasOwnProperty(numberTest)) {
        tests[numberTest] = {
            'pathFileTestIn': `tests/${numberTest}.in`,
            'pathFileTestOut': `tests/${numberTest}.out`
        }
    }
}

for (const [key, value] of Object.entries(tests)) {
    const testIn = fs.readFileSync(value.pathFileTestIn, 'utf-8');
    const testOut = fs.readFileSync(value.pathFileTestOut, 'utf-8');
    const result = analysis(testIn);
    if (result === testOut) {
        console.log(`✅ ${key} Test success`);
    } else {
        console.log(`❌ ${key} Test error`);
    }
}
