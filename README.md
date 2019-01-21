# gryd-matching
Python code for matching events in the GRYD study and LAPD data sets by date and location.

The getcoords script queries the Google API to geocode addresses into GPS coordinates.

The initial-match script pairs events by proximity in date and location.

I considered these initial matches as valid if there was exactly one LAPD event that happened on the same day and within 500 meters of the corresponding the GRYD event. Other matches are marked for further comparison. To validate this assumption, I randomly sampled 10% of these initial matches and rechecked them manualy. 
