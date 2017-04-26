# Last.fm Listening History Downloader
Download all of your Last.fm music listening history including plays not included in your recent tracks

## Why use this downloader
Other scripts created for saving your listening history search through all of the tracks in your recent history, but there can be tracks that do not appear there. This can mean losing thousands of scrobbles depending on how many tracks are not tagged with a listening date. 

For me, other downloaders lost around 20,000 tracks from my listening history due to the tracks not appearing in my recents. While the Last.fm API makes it very difficult to correctly save all of the tracks that do not appear in recent tracks, I was able to recover more than 19,000 of those plays with this downloader.

## How it works
The following steps are taken in order to get the most accurate listening history:
1. Create a list of all of the tracks in the given user's recent tracks
2. Create a list of all of the artists in a user's library
3. Traverse the list of artists to find all tracks by an artist that have listening dates
4. Search for the total play count that the user has for the current track
5. Save additional plays for the track equal to the difference between the number of plays with listening dates and the number of total plays
6. Check the current artist's total play count by the user
7. If the play counts for all of the currently saved tracks do not add up to the total play count for the artist, search through the top 100 tracks by the artist in an attempt to find more lost plays
8. Use recent listening history for any artist that is not returned from the API
9. Save all tracks to a .csv file

## Running the downloader
To run the downloader, simply download a copy of this repository and run `downloader.py` using Python 3.

From there, enter your Last.fm username, whether or not you imported tracks from another source to your library (if no, the downloader will simply pull all recent listening history and do nothing else), and a location to save your history.

Make sure that your account does not have a track currently playing, as that can change the data returned by the API.

## Running the tests
From the top directory, run:

`python3 -m lastfmhistory.tests.test_api_wrapper`

`python3 -m lastfmhistory.tests.test_csv_writer`
