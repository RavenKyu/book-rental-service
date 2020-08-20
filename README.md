# book-rental-manager-api

## Usage
```bash
usage: book-rental-manager-api [-h] {init,server} ...

positional arguments:
  {init,server}
    init         Initialize database
    server       Run api server

optional arguments:
  -h, --help     show this help message and exit
```
### init
`WARNING:: It will delete all data.` 

### server
Execute it as a api server. 

## API
### Get all of memebers
```bash
$ curl --request GET 'http://localhost:5000/customers' 

[{"id": 2, "name": "\uc784\ub355\uaddc", "phone": "010-9508-0875"}, {"id": 3, "name": "\uae40\ub355\uaddc", "phone": "010-8857-5121"}]
```
