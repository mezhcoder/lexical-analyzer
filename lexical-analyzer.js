const {getLexemes} = require("./parser/Lex");
if (process.argv.length > 2) {
    const line = process.argv[2]
    const result = getLexemes(line);
    console.log(result);
    process.exit(0);
}

console.log("Use: node lexical-analyzer.js <line>")