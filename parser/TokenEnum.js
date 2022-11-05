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
    'MUL',
    'DIV_REAL',
    'ADD_ASSIGN',
    'SUB_ASSIGN',
    'MUL_ASSIGN',
    'DIV_ASSIGN',
    'MOD_ASSIGN',

    'EQUAL',
    'LESS',
    'MORE',
    'NOT_EQUAL',
    'LESS_EQUAL',
    'MORE_EQUAL',

    'O_SHL',
    'O_SHR'
]);

module.exports = {
    Type,
    Token
}
