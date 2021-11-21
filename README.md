# Stock Market API Service

Expose an API service to get stock market information. 

Here are some examples of stock symbols
- Facebook (FB)
- Apple (AAPL)
- Microsoft (MSFT)
- Google (GOOGL)
- Amazon (AMZN)

The system makes use of a web service called Alpha Vantage, this will provide stock market information.

**Deploy**

1. To deploy the solution clone this repo in a local service or a local VM.
2. Download and install docker and docker compose:
  https://docs.docker.com/engine/install/ubuntu/
  https://docs.docker.com/compose/install/
3. Access the folder and create inside a .env file containing at least the following ENVVAR, ie:
```
SECRET_KEY=4!nbt6_qz&kokoke_nqm$ey1-@s-nrld-x0x#md_gum4x7mfc
```
4. Build the yaml:
```
docker-compose build
```
5. Deploy it:
```
docker-compose up
```
6. Verify the IP address of the stock-api-vantage_web_1:
```
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' stock-api-vantage_web_1
```
7. Replace the IP address in nginx/conf/default.conf in:
```
upstream web {
                 ## Can be connect with "gru_lipigas-api-tier" network
            # aiservice-backend
            server {stock-api-vantage_web_1 IP address}:8000;
                }
```
5. Restart the containers:
```
docker-compose stop
docker-compose up
```
Information retrieved in the response of the service as json format contains:
- Open price
- Higher price
- Lower price
- Variation between last 2 closing price values.

**Requests**
To signup:
```
POST /user/signup/
request:
{
	"name": "testname",
	"last": "testlast",
	"username":"usernametest",
	"mail":"mail4@mail.com",
	"password":"password"
	
}
```
To login and get and access token:
If user is created you will received a 200 HTTP status, else a 400 Bad Request
```
GET /user/login/
request:
{
	"name": "testname",
	"last": "testlast",
	"username":"usernametest",
	"mail":"mail4@mail.com",
	"password":"password"
	
}
response:
{
  "Authorization": "a7c5358fef520e4ebf06a7f7c448e7305385ce64"
}
```
This token is used as a header in the request to retrieve  Stock data:
```
GET /user/ticker/
request:
{
	"ticker": "FB",
	"last": "last",
	"username":"username2",
	"mail":"mail@mail.com",
	"password":"password"
	
}
response:
{
  "1. open": "342.2000",
  "2. high": "352.1000",
  "3. low": "339.9000",
  "4. close": "345.3000",
  "5. volume": "26488541",
  "close deviation": "6.6100"
}
```
To check an example of the app, please go to the following URL:
```
http://35.199.92.21
```
Add the corresponding endpoints and parameters to access the app.
