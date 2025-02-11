# Backend Calculator for shopping cart purchases

This is a simple woltapp for the Wolt Software Engineer Internship (2025) position that I made. 

## Setup
In order to get it started, you'll need the following software

- Python 3.8 (or later version)
- Pip (Needed to download the following)
- [Flask 3.0](https://pypi.org/project/Flask/)
- [Haversine](https://pypi.org/project/haversine/) 
- [requests](https://pypi.org/project/requests/)

If you want to try the automatic tests, you will also need

- [Pytest](https://pypi.org/project/pytest/)

The code itself has lots of comments about how each part functions. But simply it uses Flask as a gateway between the users GET requests and the GET requests to the wolt database API. I used Flask mainly because it was easy to use and I am personally really comfortable using it. If the application was scaled to a higher application then it might not be the best use of case.


To get the application running, you'll needed to have installed all the required software. I also used this in a Linux/Ubuntu run case, but it shouldn't be too hard on Mac and Windows. Also using python virtual environment is recommended.

When all is ready, got to the main repository and type the following on your terminal:
 ```
export FLASK_APP=backend.py
flask run --port 8000
 ```

Now open a second terminal and you'll have access to the application through the gateway. If you want to try a custom test then using something like:

 ```
curl "http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
 ```
should output the following:
```js
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
 ```

**NOTE**

Remember to use double quotes within the localhost url message. The application doesn't recognize the other parameters after '&'.

Noted: The application will accept distances to venues if they are at the maximum distance given in within the 'distance_ranges'

## Test file
If you don't want to do custom tests then doing then by pytests automatic test is totally fine. (Check above for the pytest link) 

How to use:

Simply open the repository that has py_testing.py and backend.py in it and input
 ```
    pytest
 ```
It checks 3 separate test cases:

    - application gives a correct endpoint when the input is valid
    - application gives a correct json when the input is valid
    - application gives a correct endpoint when the input is not valid
    
You can customize these however you like, if you want to try different things

That's mostly the important stuff. I'd be glad to discuss about the application further with you :D
