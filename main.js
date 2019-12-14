const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require('path');
const deploy_env = process.env.DEPLOY_ENV;
let pyProc = null;
let pyPort = null;
let appath = app.getAppPath();
console.log("DIRNAME", __dirname);
console.log("APP PATH", appath);


let mainWindow = null
const createWindow = () => {
    mainWindow = new BrowserWindow({
        width: 950, height: 700,
        minWidth: 950, minHeight: 700,
        maxWidth: 950, maxHeight: 700,
        center: true, 
        darkTheme: true,
        webPreferences: {
            nodeIntegration: true,
        },
    });
    mainWindow.setMenu(null);
    if (deploy_env && deploy_env == "DEV") { // Development environment
        console.log("------ DEVELOPMENT VERSION ------");
        mainWindow.loadURL("http://localhost:8080/");
    }
    else {
        console.log("------ PRODUCTION VERSION ------");
        // Production environment
        mainWindow.loadURL(require('url').format({
            pathname: path.join(__dirname, './dist/index.html'),
            protocol: 'file:',
            slashes: true
        }));
    }
    mainWindow.webContents.openDevTools({mode: 'detach'});
    mainWindow.focus();
    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

app.on('ready', () => {
    createPyProc();
    createWindow();
});
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin'){
        app.quit();
    }
})
app.on('activate', () => {
    if (mainWindow === null){
        createWindow();
    }
})

const selectPort = () => {
    pyPort = 42069;
    return pyPort;
}

const createPyProc = () => {
    let port = '' + selectPort();
    let script = path.join(__dirname, 'main.py');
    pyProc = require('child_process').spawn('python', [script, port]);
    if (pyProc != null) {
      console.log('child process success');
    }
}

const exitPyProc = () => {
    console.log(lmao)
    pyProc.kill();
    pyProc = null;
    pyPort = null;
}

app.on('will-quit', exitPyProc);
