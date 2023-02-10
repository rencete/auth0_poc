function login(email, password, callback) {
    const { Client } = require('pg');
    const crypto = require('crypto');

    const iterations = 100000;
    const hashFn = 'sha256';

    const connString = `postgres://${configuration.dbuser}:${configuration.dbpasswd}@${configuration.dbserver}/${configuration.dbdatabase}`;
    const client = new Client({
        connectionString: connString,
    });

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

    client.connect(function (err) {
        if (err) return callback(err);

        const query = 'SELECT id, nickname, email, password FROM users WHERE email = $1';

        client.query(query, [email], function (err, result) {

            if (err || result.rows.length === 0) return callback(err || new WrongUsernameOrPasswordError(email));

            const user = result.rows[0];
            const [subkeyLength, salt, subkey] = getSaltAndSubkey(user.password);

            crypto.pbkdf2(password, salt, iterations, subkeyLength, hashFn, function (err, derivedKey) {
                if (err || !derivedKey) return callback(err || new WrongUsernameOrPasswordError(email));
    
                if (derivedKey.toString('base64') !== subkey.toString('base64')) return callback(err || new WrongUsernameOrPasswordError(email));
    
                callback(null, {
                    user_id: "customdb_" + user.id,
                    nickname: user.nickname,
                    email: user.email
                });
            });
        });
    });
}