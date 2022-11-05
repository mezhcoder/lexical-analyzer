function* bufferIter(buffer) {
    for (const char of buffer) {
        yield char;
    }
}

function peekable(iterator) {
    let state = iterator.next();

    const _i = (function* () {
        while (!state.done) {
            const current = state.value;
            state = iterator.next();
            yield current;
        }
        return state.value;
    })()

    _i.peek = () => state;
    return _i;
}

class BufferReader {
    constructor(buffer) {
        this._dataIter = peekable(bufferIter(buffer));
        this._buffer = [];
        this._cursor = {
            i: 0,
            j: 1
        }
    }

    addCursorIndexFromLine() {
        this._cursor.i++;
    }

    addCursorLineFromColumn() {
        this._cursor.j++;
    }

    getBuffer() {
        return this._buffer
    }

    getCursor() {
        return this._cursor;
    }

    peekChar() {
        return this._dataIter.peek().value;
    }

    nextChar() {
        let char = undefined;
        while (true) {
            char = this._dataIter.next().value;
            if (char === '\n' || char === '\r') {
                this.addCursorLineFromColumn();
            } else {
                return char;
            }
        }
    }

    addCharIntoBuffer(char) {
        this._buffer.push(char);
    }

    clearBuffer() {
        this._buffer = [];
    }
}

module.exports = {
    BufferReader
}
