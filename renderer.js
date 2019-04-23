const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

let dirlist_table = document.querySelector('#dirlist_table')
let rowcount = document.querySelector('#rowcount')

dirlist_table.addEventListener('load', () => {
    client.invoke("list_directories", (error, res) => {
        if (error) {
            console.error(error)
        } else {
            rowcount.innerHTML = res.length
            for (var i = 0; i < res.length; i++) {
                console.log(i)
                var name = res[i].name.toString();
                var path = res[i].path.toString();
                var row = `<tr><td>${name}</td><td>${path}</td></tr>`;
                dirlist_table.innerHTML += row;
            }
        }
    })
})

dirlist_table.dispatchEvent(new Event('load'))

//formula.addEventListener('input', () => {
//  console.log(formula.value)
//  client.invoke("calc", formula.value, (error, res) => {
//    if(error) {
//      console.error(error)
//    } else {
//      result.textContent = res
//    }
//  })
//})

//formula.dispatchEvent(new Event('input'))


