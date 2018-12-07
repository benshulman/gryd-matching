# gryd-matching
Python code for matching GRYD and LAPD events by date and location.

Gecoords queries the Google API to geocode addresses into GPS coordinates.

Initialmatch pairs events by proximity in date and location.

We mark these initial matches as valid if there was exactly one LAPD event that happened on the same day and within 500 meters of the corresponding the GRYD event. Other matches are marked for further comparison.
