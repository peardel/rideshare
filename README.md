# Rideshare

Generates ride-shares based on an excel input, and visualizes them on a map.

## Requirements:
- Python3
- pip

## Installation and Running
```
git clone https://github.com/peardel/rideshare.git
pip install -r requirements.txt
```
Then run `main.py`. This may take some time to download position data for postcodes due to rate throttling, however it will finish in ~20s.

## Excel Format

- Postcode
- Want to get a lift (YES/NO)
- Want to offer a lift (YES/NO)
- Free seats
- Times of arrival and departure Mon-Fri

## Notes
- New datasets can be generated in tests.py
- The number of rows to be read must be set in line 23 of original_dataset_handler.py, where it is 100 by default (101 including the header)
