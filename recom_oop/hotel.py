import json, logging

class HotelTable(object):
    def __init__(self):
        self._id = None
        self._name = None
        self._address1 = None
        self._address2 = None
        self._city = None
        self._state_province = None
        self._postal_code = None
        self._country_code = None
        self._latitude = None
        self._longitude = None
        self._airport_code = None
        self._property_category = None
        self._currency_code = None
        self._star_rating = None
        self._location = None
        self._checkin_time = None
        self._checkout_time = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def address1(self):
        return self._address1

    @property
    def address2(self):
        return self._address2

    @property
    def city(self):
        return self._city

    @property
    def state_province(self):
        return self._state_province

    @property
    def postal_code(self):
        return self._postal_code

    @property
    def country_code(self):
        return self._country_code

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def airport_code(self):
        return self._airport_code

    @property
    def property_category(self):
        return self._property_category

    @property
    def currency_code(self):
        return self._currency_code

    @property
    def star_rating(self):
        return self._star_rating

    @property
    def location(self):
        return self._location

    @property
    def checkin_time(self):
        return self._checkin_time

    @property
    def checkout_time(self):
        return self._checkout_time

    @id.setter
    def id(self, id):
        self._id = id

    @name.setter
    def name(self, name):
        self._name = name

    @address1.setter
    def address1(self, address):
        self._address1 = address

    @address2.setter
    def address2(self, address):
        self._address2 = address

    @city.setter
    def city(self, city):
        self._city = city

    @state_province.setter
    def state_province(self, state_province):
        self._state_province = state_province

    @postal_code.setter
    def postal_code(self, postal_code):
        self._postal_code = postal_code

    @country_code.setter
    def country_code(self, country_code):
        self._country_code = country_code

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = latitude

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude

    @airport_code.setter
    def airport_code(self, airport_code):
        self._airport_code = airport_code

    @property_category.setter
    def property_category(self, property_category):
        self._property_category = property_category

    @currency_code.setter
    def currency_code(self, currency_code):
        self._currency_code = currency_code

    @star_rating.setter
    def star_rating(self, star_rating):
        self._star_rating = star_rating

    @location.setter
    def location(self, location):
        self._location = location

    @checkin_time.setter
    def checkin_time(self, checkin_time):
        self._checkin_time = checkin_time

    @checkout_time.setter
    def checkout_time(self, checkout_time):
        self._checkout_time = checkout_time

    def parse_json(self, text):
        resp = json.loads(text)
        if '@hotelId' not in resp['HotelInformationResponse']:
            logging.warn('message: {}'.format(
                resp['HotelInformationResponse']['EanWsError']['presentationMessage']))
            if 'verboseMessage' in resp['HotelInformationResponse']['EanWsError']:
                logging.warn('message: {}'.format(
                    resp['HotelInformationResponse']['EanWsError']['verboseMessage']))
            return None

        self._id = resp['HotelInformationResponse']['@hotelId']
        self._name = resp['HotelInformationResponse']['HotelSummary']['name']
        self._address1 = resp['HotelInformationResponse']['HotelSummary']['address1']
        if 'address2' in resp['HotelInformationResponse']['HotelSummary']:
            self._address2 = resp['HotelInformationResponse']['HotelSummary']['address2']
        self._city = resp['HotelInformationResponse']['HotelSummary']['city']
        if 'stateProvinceCode' in resp['HotelInformationResponse']['HotelSummary']:
            self._state_province = resp['HotelInformationResponse']['HotelSummary']['stateProvinceCode']
        if 'postalCode' in resp['HotelInformationResponse']['HotelSummary']:
            self._postal_code = resp['HotelInformationResponse']['HotelSummary']['postalCode']
        if 'countryCode' in resp['HotelInformationResponse']['HotelSummary']:
            self._country_code = resp['HotelInformationResponse']['HotelSummary']['countryCode']
        if 'latitude' in resp['HotelInformationResponse']['HotelSummary']:
            self._latitude = resp['HotelInformationResponse']['HotelSummary']['latitude']
        if 'longitude' in resp['HotelInformationResponse']['HotelSummary']:
            self._longitude = resp['HotelInformationResponse']['HotelSummary']['longitude']
        if 'airportCode' in resp['HotelInformationResponse']['HotelSummary']:
            self._airport_code = resp['HotelInformationResponse']['HotelSummary']['airportCode']
        if 'propertyCategory' in resp['HotelInformationResponse']['HotelSummary']:
            self._property_category = resp['HotelInformationResponse']['HotelSummary']['propertyCategory']
        if 'rateCurrencyCode' in resp['HotelInformationResponse']['HotelSummary']:
            self._currency_code = resp['HotelInformationResponse']['HotelSummary']['rateCurrencyCode']
        if 'hotelRating' in resp['HotelInformationResponse']['HotelSummary']:
            self._star_rating = resp['HotelInformationResponse']['HotelSummary']['hotelRating']
        if 'locationDescription' in resp['HotelInformationResponse']['HotelSummary']:
            self._location = resp['HotelInformationResponse']['HotelSummary']['locationDescription']
        if 'checkInTime' in resp['HotelInformationResponse']['HotelDetails']:
            self._checkin_time = resp['HotelInformationResponse']['HotelDetails']['checkInTime']
        if 'checkOutTime' in resp['HotelInformationResponse']['HotelDetails']:
            self._checkout_time = resp['HotelInformationResponse']['HotelDetails']['checkOutTime']


    def __str__(self):
        return """
    id: {}
    name: {}
    city: {}
    country: {}
    """.format(self._id, self._name, self._city, self._country_code)
