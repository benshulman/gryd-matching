# GRYD Matching

Python scripts for matching events in the GRYD study and LAPD data sets by date and location. The LA Mayor's Office of Gang Reduction and Youth Development collected crime records, and I needed to match these with the LAPDs crime records. I matched geo-coded crime locations, and then matched crimes by proximity in time and space.

## Structure

- getcoords.py queries the Google API to geocode addresses into GPS coordinates.

- initial-match.py pairs events by proximity in date and location.

I considered these initial matches as valid if there was exactly one LAPD event that happened on the same day and within 500 meters of the corresponding the GRYD event. Other matches are marked for further comparison. To validate this assumption, I randomly sampled 10% of these initial matches and rechecked them manually. 
