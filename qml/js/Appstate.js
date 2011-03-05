
var appstate = Object();
var db = false;

function get_now() {
    var date = new Date();
    return date.getTime();
}

function get_date_string(timestamp) {
    var date = new Date();
    date.setTime(timestamp);
    return date.toLocaleDateString()+' '+date.toLocaleTimeString();
}

function clean_storage() {
    if(db) {
        db.transaction(function(tx) {
            tx.executeSql("Drop TABLE history");
        });
    }
}

function clean_table(table) {
    if(db) {
        db.transaction(function(tx) {
            tx.executeSql("DELETE FROM "+table+" WHERE 1");
        });
    }
}

function insert_history_entry(service, term) {
    if(db) {
        db.transaction(function(tx) {
            tx.executeSql('INSERT INTO history VALUES(?, ?, ?)', [service, term, get_now() ]);
        })
    }
}

function get_table_entries(table) {
    if(db) {
        db.transaction(function(tx){
             // Show all added greetings
             var rs = tx.executeSql('SELECT * FROM '+table);

             var r = ""
             for(var i = 0; i < rs.rows.length; i++) {
                 r += rs.rows.item(i).service + ", " + rs.rows.item(i).cmd + ", " + get_date_string(rs.rows.item(i).tstamp) + "\n"
             }
             var text = r
             console.log(text)
            }
        );
    }
}

function init_storage() {
    console.log('initialise storage');
    db = openDatabaseSync("AskZiggyQmlDB1", "1.0", "The Example QML SQL!", 1000000);
    db.transaction(
        function(tx) {
            // Create the database if it doesn't already exist
            tx.executeSql('CREATE TABLE IF NOT EXISTS history(service TEXT, cmd TEXT, tstamp INTEGER)');
        }
    )
}

//    clean_storage();
//    clean_table('history');
//    insert_history_entry('gnews','nokia #de');
//    get_table_entries('history');

function init() {
    init_storage();
}
