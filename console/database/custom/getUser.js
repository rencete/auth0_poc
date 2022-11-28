function getByEmail(email, callback) {
    const mysql = require('mysql');
  
    const connection = mysql.createConnection({
        host: 'sql9.freemysqlhosting.net',
        user: 'sql9581100',
        password: 'cnNLWryTrV',
        database: 'sql9581100'
    });
  
    connection.connect();

    const query = 'SELECT first_name, last_name, email FROM users WHERE email = ?';
  
    connection.query(query, [ email ], function(err, results) {
      if (err || results.length === 0) return callback(err || null);
  
      const user = results[0];
      callback(null, {
        user_id: user.email,
        nickname: user.email,
        email: user.email
      });
    });
  }
  