const Enum = require('enum');

const Type = new Enum([
    'EOF',
    'CHAR',
    'ERROR',
    'OPERATOR',
    'STRING'
]);


const Token = new Enum([
    'EOF',
    'SEMICOLOM',
    'ASSIGN',
    'ADD',
    'SUB',
    'LESS',
    'MORE',
]);

module.exports = {
    Type,
    Token
}
