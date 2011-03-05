
var appstate = Object();
var db = false;

function getNow() {
    var date = new Date();
    return date.getTime();
}

function getDateString(timestamp) {
    var date = new Date();
    date.setTime(timestamp);
    return date.toLocaleDateString()+' '+date.toLocaleTimeString();
}

function getConnection() {
    return openDatabaseSync("SubstanceOfCodeTwimGo", "1.0", "KeyValueStorage", 10);
}

function executeSql(sql, params) {
    db = getConnection()
    var res = false;
    if(!params) params = [];
    db.transaction(function(tx) {
        res = tx.executeSql(sql,params);
    });
    return res;
}

function cleanStorage() {
    executeSql("Drop TABLE history");
}

function cleanTable(table) {
    executeSql("DELETE FROM "+table+" WHERE 1");
}

function insertHistoryEntry(service, term) {
    executeSql('INSERT OR REPLACE INTO history VALUES(?, ?, ?)', [service, term, getNow() ]);
}

function getHistoryEntries(service, limit) {
    db = getConnection()
    var sql = 'SELECT * FROM history WHERE'
    if(service != '') {
        sql += ' service = "'+service+'" ORDER BY tstamp DESC';
    } else {
        sql += ' 1 ';
    }
    if(limit) sql += ' LIMIT '+limit

    var rows = Array();
    var rs = executeSql(sql);
    for(var i = 0; i < rs.rows.length; i++) {
        rows.push(rs.rows.item(i))
    }
    return rows;
}

function getTableEntries(table) {
    var rs = executeSql('SELECT * FROM '+table,'');
    var r = ""
    for(var i = 0; i < rs.rows.length; i++) {
        r += rs.rows.item(i).service + ", " + rs.rows.item(i).cmd + ", " + getDateString(rs.rows.item(i).tstamp) + "\n"
    }
    var text = r
    console.log(text)
}

function initStorage() {
    console.log('initialise storage');
    db = getConnection()
//    clean_storage();
//    clean_table('history');
    executeSql('CREATE TABLE IF NOT EXISTS history(service TEXT, cmd TEXT, tstamp INTEGER)');
    executeSql('CREATE UNIQUE INDEX IF NOT EXISTS history_key ON history (service, cmd)');
//    getTableEntries('history')
}

function init() {
    initStorage();
}
