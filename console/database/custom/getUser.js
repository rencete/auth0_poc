function loginByEmail(email, callback) {  
  const postgres = require('pg');

  const connString = `postgres://${configuration.dbuser}:${configuration.dbpasswd}@${configuration.dbserver}/${configuration.dbdatabase}`;
  postgres.connect(connString, function (err, client, done) {
    if (err) return callback(err);

    const query = 'SELECT id, nickname, email FROM users WHERE email = $1';
    client.query(query, [email], function (err, result) {
      done();

      if (err || result.rows.length === 0) return callback(err);

      const user = result.rows[0];

      return callback(null, {
        user_id: "customdb_" + user.id,
        nickname: user.nickname,
        email: user.email
      });
    });
  });
}