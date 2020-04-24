# Defang API
Defang API runs a local server or Docker that can assist in defanging URLs to make them safe to 
post in various apps or tp log in case logs. 

Capabilities:
- Defang URL
- Refang URL
- Base64 Decode
- Base64 Encode

The defang functionality is ran using a a modified version of the defang package from Johan Nestaas. 
I currently a pull request in to incorporate the changes I have made to it to better support more 
protocols and defanging options.

Original: https://bitbucket.org/johannestaas/defang/src/master/

Mine: https://bitbucket.org/zpriddy/defang/src/master/

Pull Request: https://bitbucket.org/johannestaas/defang/pull-requests/4/add-better-support-for-defanging/diff


## Installing and Running

----
### Using PIP (Easy)
#### Install
Run : `pip install defang-api`

#### Running
Run: `defang-server`

By default this will run on `localhost` on port `5000` but that can be changed at runtime:

`defang-server --port=8080 --host-0.0.0.0`

---
### Using Docker (Advanced)
#### Install
Requirements: 
  - Docker Installed
    - `brew install docker`
  - Docker Compose installed
    - `brew install docker-compose`
    
Clone the repo: `git clone https://github.com/zpriddy/defang_api.git`

#### Running

Run: `cd defang_api`

Run: `docker-compose up`

----
## Using Defang API

When you launch the server by default it will run on `localhost:5000`. 
There is full [Swagger](https://swagger.io/) documentation if you point your browser at 
`http://localhost:5000`. This will give you full details on all of the available options for each 
endpoint of the API as well as the ability to test each of the endpoints.

By default the API will return its results in JSON but if `accept` header is set to `text/plain` 
then it will return the results in plain text.

## Examples
If you run:
```bash
curl -X GET "http://localhost:5000/api/defang?url=http%3A%2F%2Fexample.com" -H "accept: text/plain"
```
You will get back
```
hXXp://example[.]com
```
___
```bash
curl -X GET "http://localhost:5000/api/defang?url=http%3A%2F%2Fexample.com" -H "accept: application/json"
```
Will give you back JSON:
```
{
  "error": [],
  "output": "hXXp://example[.]com"
}
```
----
If you have a list of URLS:
```bash
curl -X POST "http://localhost:5000/api/defang" -H "accept: application/json" -H "Content-Type: "\
"application/json" -d "{ \"colons\": false, \"dots\": false, \"url\": [ \"https://example.com\", \"https://foo.bar\" ]}"
```
Will give you:
```
{
  "error": [],
  "output": [
    "hXXps://example[.]com",
    "hXXps://foo[.]bar"
  ]
}
```
But if you set the accept to `text/plain` you will get:
```
hXXps://example[.]com,hXXps://foo[.]bar
```
## Notes
The simple `GET` method endpoints are limited on the scope of options that there are in passing 
data in. For this reason I recommend using the `POST` method endpoints