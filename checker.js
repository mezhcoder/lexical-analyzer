const fs = require('fs');
const { getLexemes } = require('./parser/Lex')

const tests = {}
for (const nameFile of fs.readdirSync("tests")) {
    const numberTest = nameFile
        .replace('.in', '')
        .replace('.out', '')
    if (!tests.hasOwnProperty(numberTest)) {
        tests[numberTest] = {
            'pathFileTestIn': `tests/${numberTest}.in`,
            'pathFileTestOut': `tests/${numberTest}.out`
        }
    }
}
let successTest = 0;
for (const [key, value] of Object.entries(tests)) {
    const testIn = fs.readFileSync(value.pathFileTestIn, 'utf-8');
    const testOut = fs.readFileSync(value.pathFileTestOut, 'utf-8');
    const result = getLexemes(testIn);
    if (result === testOut) {
        console.log(`🟢 ${key} success`);
        successTest++;
    } else {
        console.log(`🔴 ${key} error`);
    }
}
console.log(`Total tests: ${successTest}/${Object.keys(tests).length}`)
