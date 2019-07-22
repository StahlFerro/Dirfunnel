console.log("interface.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');

let dirtable_body = document.getElementById('dirtable_body');

window.addEventListener("load", load_directory_table);

function load_directory_table() {
    client.invoke("get_directories", (error, res) => {
        console.log('invoker called!')
        if (error) {
            console.log(error);
        }
        else {
            table_filler(res);
        }
    });
}


function table_filler(res) {
    res.forEach(function(r) {
        console.log('r', r);
        var tr = document.createElement('TR');
        var td_name = document.createElement('TD');
        var td_path = document.createElement('TD');
        td_name.innerHTML = r.name;
        td_path.innerHTML = r.path;
        tr.appendChild(td_name);
        tr.appendChild(td_path);
        dirtable_body.appendChild(tr);
    });
}
