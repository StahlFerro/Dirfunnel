console.log("interface.js loaded!");
const remote = require('electron').remote;
const dialog = remote.dialog;
const session = remote.getCurrentWebContents().session;
const { client } = require('./Client.js');

let directory_table = document.getElementById('directory_table');

window.addEventListener("load", load_directory_table);

function load_directory_table() {
    client.invoke("get_directories", (error, res) => {
        console.log('invoker called!')
        if (error) {
            console.log(error);
        }
        else {
            for (const [name, path] of res){
                console.log(`${name} -> ${path}`);
            }
        }
    });
}
