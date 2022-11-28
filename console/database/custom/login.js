function login(email, password, callback) {
    const mysql = require('mysql');
    const crypto = require('crypto');

    const iterations = 1000;
    const hashFn = 'sha256';

    function readNetworkByteOrder(buffer, offset) {
        return ((buffer[offset + 3]) << 24)
            | ((buffer[offset + 2]) << 16)
            | ((buffer[offset + 1]) << 8)
            | ((buffer[offset + 0]));
    }

    function getSaltAndSubkey(hashedPassword) {
        let decodedBuffer = null;

        if (hashedPassword) {
            decodedBuffer = Buffer.from(hashedPassword, 'base64');
        }

        let key = decodedBuffer[0];
        let saltLength = readNetworkByteOrder(decodedBuffer, 9);

        if (saltLength < 128 / 8) {
            return false;
        }

        let salt = Buffer.alloc(saltLength);

        // take the salt from the stored hash in the database.
        decodedBuffer.copy(salt, 0, 13, 13 + saltLength);

        let subkeyLength = decodedBuffer.length - 13 - saltLength;

        //console.log(subkeyLength)

        if (subkeyLength < 128 / 8) {
            return false;
        }

        let expectedSubkey = Buffer.alloc(subkeyLength);

        decodedBuffer.copy(expectedSubkey, 0, 13 + saltLength, 13 + saltLength + expectedSubkey.length);

        return [subkeyLength, salt, expectedSubkey];
    }

    const connection = mysql.createConnection({
        host: 'sql9.freemysqlhosting.net',
        user: 'sql9581100',
        password: 'cnNLWryTrV',
        database: 'sql9581100'
    });

    connection.connect();

    const query = 'SELECT first_name, last_name, email, password_hash FROM users WHERE email = ?';

    connection.query(query, [email], function (err, results) {
        if (err) return callback(err);
        if (results.length === 0) return callback(new WrongUsernameOrPasswordError(email));
        const user = results[0];

        const [subkeyLength, salt, subkey] = getSaltAndSubkey(user.password_hash);
        crypto.pbkdf2(password, salt, iterations, subkeyLength, hashFn, function (err, derivedKey) {
            if (err || !derivedKey) return callback(err || new WrongUsernameOrPasswordError(email));

            if (derivedKey.toString('base64') !== subkey.toString('base64')) return callback(err || new WrongUsernameOrPasswordError(email));

            callback(null, {
                user_id: user.email,
                nickname: user.email,
                email: user.email
            });
        });
    });
}