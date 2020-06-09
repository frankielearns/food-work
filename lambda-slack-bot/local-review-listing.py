import requests, json
import pprint
import os
from urllib import parse as urlparse
def google(queryname):
    google_api_key = os.environ["google_api_key"]
    google_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    query = queryname
    r = requests.get(google_url + 'query=' + query +
                            '&key=' + google_api_key)

    x = r.json()
    y = x['results']

    # keep looping upto length of y
    for i in range(len(y)):
        placeid = y[i]['place_id']

    def get_place_details(place_id):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        google_params = {
            'placeid': place_id,
            'fields': 'rating',
            'key': google_api_key
        }
        res = requests.get(endpoint_url, params = google_params)
        place_details =  json.loads(res.content)
        return place_details

    details = get_place_details(placeid)
    return details['result']['rating']

def yelp():
    yelp_api_key= os.environ["yelp_api_key"]
    headers = {'Authorization': 'Bearer {0}'.format(yelp_api_key)}
    url='https://api.yelp.com/v3/businesses/search'
    #params = {'term':'food','location':'Toronto', 'attributes':'hot_and_new'}
    params = {'term':'food','location':'Toronto','limit':'10', 'offset':'10'}
    req = requests.get(url, params=params, headers=headers)
    parsed = json.loads(req.text)
    return parsed


def review(passed_list):
    businesses = passed_list["businesses"]
    restaurants = []
    for business in businesses:
        address = business["location"]["display_address"]
        name = business["name"]
        google_search = name + ' ' + ' '.join([str(elem) for elem in address])
        restaurants.append("Name: {0}".format(business["name"]))
        restaurants.append("Rating: {0}".format(business["rating"]))
        restaurants.append("Google Rating: {0}".format(google(google_search)))
        restaurants.append("Picture: {0}\n".format(business["image_url"]))
    listToStr = '\n'.join([str(elem) for elem in restaurants])
    print(listToStr)

def main():
    yelp_list = yelp()
    review(yelp_list)

if __name__ == '__main__':
    main()
