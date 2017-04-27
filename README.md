# Housing
Coding Challenge

## Design

There are 2 main files: `housing_server.py` and `housing_data.py`.

### `housing_server.py`
On startup, we load data from `housing_data.py` (more on that below). It's setup as a gRPC server, taking in `EstimatePriceRequest`s and returning `EstimatePriceResponse`s.


### `housing_data.py`
On initialization, the CSV is downloaded if missing and loaded into memory into a dictionary of dictionaries like below:

``` 
{
	'borough1': {
		date(2000, 1, 1): Decimal('29.0'),
		date(2000, 2, 1): Decimal('30.0'),
		...
	},
	'borough2': {
		date(2000, 1, 1): Decimal('9.012'),
		date(2000, 2, 1): Decimal('12.2'),
		...
	},
	...
}
				
```

While using up more memory and time in the beginning, this allows constant time lookups and very low latency.


## Using 

### Installing

```
virtualenv venv
source venv/bin/activate
pip install -r requirements_lock.txt
```


### Running
Start the server: `python housing_server.py`

Run the example client: `python housing_client_example.py`


### Dependencies
Modify the `requirements.txt`file to add or update new deps.
After modifying, run:

```
pip install -r requirements.txt --upgrade && pip freeze > requirements_lock.txt
```

That will save everything into the `requirements.txt` file but won't be very
user-readable. Think of this as the difference between Gemfile and Gemfile.lock
for anyone with Ruby experience.
