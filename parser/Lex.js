const _ = require('lodash-contrib');

const { BufferReader } = require("./BufferReader");
const { Type, Token } = require('./TokenEnum');

class LexicalAnalyzer {
    constructor(bufferReader) {
        this.bufferReader = bufferReader;
        this.token = Token.ERROR;
        this.type = Type.ERROR;
    }

    processingString() {

    }

    //реализовать возможность ходить назад и вперед курсором по буфферу
    processingChar() {
        let charIndexes = '';
        if (this.bufferReader.peekChar() === '#') {
            console.log('ошибка');
        }
        while (_.isNumeric(this.bufferReader.peekChar())) {
            charIndexes += this.bufferReader.nextChar();
        }
        if (charIndexes.length === 0) {
            console.log('ошибка');
        }
        this.bufferReader.addCharIntoBuffer(charIndexes);
        this.token += String.fromCharCode(charIndexes);
    }

    nextLexem() {
        this.token = Token.ERROR;
        this.type = Type.ERROR;

        const currentChar = this.bufferReader.nextChar();
        this.bufferReader.addCharIntoBuffer(currentChar);
        switch (currentChar) {
            case '#':
                this.token = "";
                do {
                    if (this.bufferReader.peekChar() === '#')
                        this.bufferReader.addCharIntoBuffer(this.bufferReader.nextChar());
                    this.processingChar();
                } while (this.bufferReader.peekChar() === '#');
                const countCharGrid = this.bufferReader.getBuffer().join('').match(/#/g).length;
                this.type =  (countCharGrid > 1) ? Type.STRING : Type.CHAR;
                break;
            case '\'':
                break
            case ';':
                this.type = Type.OPERATOR;
                this.token = Token.SEMICOLOM.key;
                break;
            case undefined:
                this.type = Type.EOF;
                this.token = Token.EOF.key;
        }
        this.bufferReader.addCursorIndexFromLine();
        this.bufferReader.clearBuffer();
        return {
            cursor: this.bufferReader.getCursor(),
            type: this.type,
            token: this.token
        }
    }
}

function getLexemes(line) {
    const bufferReader = new BufferReader(line);
    const lexicalAnalyzer = new LexicalAnalyzer(bufferReader);

    const result = [];
    let lexem = undefined;
    do {
        lexem = lexicalAnalyzer.nextLexem(bufferReader);
        const lexemFormatStr = `${lexem.cursor.j}    ${lexem.cursor.i}    ${lexem.type.key}    ${lexem.token}`;
        result.push(lexemFormatStr);
    } while (lexem.type !== Type.EOF);
    return result.join('');
}

module.exports = {
    getLexemes
}
