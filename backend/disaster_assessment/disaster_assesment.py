# import requests
from typing import List

import haversine as hs

emergency_services = [
    {
        "name": "Rotunda Hospital",
        "type": 2,
        "lat": 53.353,
        "long": -6.26351,
        "number_fire_engines": 0,
        "number_ambulances": 6,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 24,
    },
    {
        "name": "Mater Private Hospital",
        "type": 2,
        "lat": 53.35808,
        "long": -6.26446,
        "number_fire_engines": 0,
        "number_ambulances": 12,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 48,
    },
    {
        "name": "Temple Street Hospital",
        "type": 2,
        "lat": 53.356915045655334,
        "long": -6.261492759885292,
        "number_fire_engines": 0,
        "number_ambulances": 4,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 16,
    },
    {
        "name": "National Maternity Hospital",
        "type": 2,
        "lat": 53.34013,
        "long": -6.2456,
        "number_fire_engines": 0,
        "number_ambulances": 4,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 16,
    },
    {
        "name": "Eye and Ear Hostpital",
        "type": 2,
        "lat": 53.33259626317416,
        "long": -6.256061878919393,
        "number_fire_engines": 0,
        "number_ambulances": 3,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 12,
    },
    {
        "name": "The Meath Primary Care Centre",
        "type": 2,
        "lat": 53.33585,
        "long": -6.27019,
        "number_fire_engines": 0,
        "number_ambulances": 2,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 8,
    },
    {
        "name": "Main Hospital",
        "type": 2,
        "lat": 53.33932,
        "long": -6.29596,
        "number_fire_engines": 0,
        "number_ambulances": 6,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 20,
    },
    {
        "name": "Coombe Women & Infants Hospital",
        "type": 2,
        "lat": 53.33461,
        "long": -6.28833,
        "number_fire_engines": 0,
        "number_ambulances": 4,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 12,
    },
    {
        "name": "Kevin Street Garda Sation",
        "type": 0,
        "lat": 53.33954610143664,
        "long": -6.26760370818894,
        "number_fire_engines": 0,
        "number_ambulances": 0,
        "number_armed_units": 12,
        "number_squad_car": 4,
        "number_armoured_car": 1,
        "number_personnel": 20,
    },
    {
        "name": "Harcourt Square Garda Station",
        "type": 0,
        "lat": 53.33424,
        "long": -6.26375,
        "number_fire_engines": 0,
        "number_ambulances": 0,
        "number_armed_units": 12,
        "number_squad_car": 4,
        "number_armoured_car": 1,
        "number_personnel": 30,
    },
    {
        "name": "Store Street Garda Station",
        "type": 0,
        "lat": 53.35051251814404,
        "long": -6.252324274656007,
        "number_fire_engines": 0,
        "number_ambulances": 0,
        "number_armed_units": 15,
        "number_squad_car": 6,
        "number_armoured_car": 2,
        "number_personnel": 30,
    },
    {
        "name": "Pearse Street Garda Station",
        "type": 0,
        "lat": 53.34577194438715,
        "long": -6.256204230480236,
        "number_fire_engines": 0,
        "number_ambulances": 0,
        "number_armed_units": 20,
        "number_squad_car": 10,
        "number_armoured_car": 4,
        "number_personnel": 50,
    },
    {
        "name": "DonnyBrook Garda Station",
        "type": 0,
        "lat": 53.32156,
        "long": -6.23615,
        "number_fire_engines": 0,
        "number_ambulances": 0,
        "number_armed_units": 20,
        "number_squad_car": 10,
        "number_armoured_car": 4,
        "number_personnel": 40,
    },
    {
        "name": "Fire Brigade HQ",
        "type": 1,
        "lat": 53.346259552984044,
        "long": -6.253118230748194,
        "number_fire_engines": 5,
        "number_ambulances": 2,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 30,
    },
    {
        "name": "North Strand Fire Station",
        "type": 1,
        "lat": 53.36039726282362,
        "long": -6.2396093774148245,
        "number_fire_engines": 4,
        "number_ambulances": 3,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 30,
    },
    {
        "name": "Phibsborough Fire Station",
        "type": 1,
        "lat": 53.35834420442677,
        "long": -6.273821993325792,
        "number_fire_engines": 4,
        "number_ambulances": 3,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 30,
    },
    {
        "name": "Blanchardstown Fire Station",
        "type": 1,
        "lat": 53.38465,
        "long": -6.39612,
        "number_fire_engines": 6,
        "number_ambulances": 0,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 40,
    },
    {
        "name": "Donnybrook fire station",
        "type": 1,
        "lat": 53.3219,
        "long": -6.23743,
        "number_fire_engines": 5,
        "number_ambulances": 0,
        "number_armed_units": 0,
        "number_squad_car": 0,
        "number_armoured_car": 0,
        "number_personnel": 25,
    },
]

disasters = [
    {
        "lat": 53.339035203326596,
        "long": -6.351814270019532,
        "scale": 8,
        "disaster_type": 3,
        "radius": 900,
    },
    {
        "lat": 53.36300426345212,
        "long": -6.3453769631451005,
        "scale": 8,
        "disaster_type": 0,
        "radius": 900,
    },
    {
        "lat": 53.3488605680999,
        "long": -6.285209655761719,
        "scale": 8,
        "disaster_type": 5,
        "radius": 300,
    },
    {
        "lat": 53.35347154733865,
        "long": -6.3015174865722665,
        "scale": 7,
        "disaster_type": 5,
        "radius": 300,
    },
    {
        "lat": 53.359208958306304,
        "long": -6.2917327880859375,
        "scale": 8,
        "disaster_type": 4,
        "radius": 300,
    },
    {
        "lat": 53.338355920065034,
        "long": -6.3063240103656435,
        "scale": 8,
        "disaster_type": 1,
        "radius": 300,
    },
    {
        "lat": 53.33288711939785,
        "long": -6.2740516662597665,
        "scale": 7,
        "disaster_type": 0,
        "radius": 300,
    },
    {
        "lat": 53.32612320343734,
        "long": -6.301860809326173,
        "scale": 7,
        "disaster_type": 2,
        "radius": 300,
    },
    {
        "lat": 53.3703229942309,
        "long": -6.2273597717285165,
        "scale": 7,
        "disaster_type": 6,
        "radius": 300,
    },
    {
        "lat": 53.365048029884846,
        "long": -6.313705444335938,
        "scale": 7,
        "disaster_type": 7,
        "radius": 100,
    },
    {
        "lat": 53.36013097017263,
        "long": -6.2754249572753915,
        "scale": 8,
        "disaster_type": 3,
        "radius": 300,
    },
]

# disaster_request = requests.get(
#     "http://127.0.0.1:8000/api/1/disasters/?skip=0&limit=100"
# )
# emergency_services_request = requests.get('http://127.0.0.1:8000/api/1/emergency_services/?skip=0&limit=100')
print(disasters)
# for disaster in disaster_request.json():
#     print(disaster, type(disaster))
# print(emergency_services_request.content)

es_distances_from_disaster = []  # type: List[List]

es_garda = []
es_fire_brigade = []
es_ambulance = []

for es in emergency_services:
    if es["type"] == 0:
        es_garda.append(es)
    elif es["type"] == 1:
        es_fire_brigade.append(es)
    elif es["type"] == 2:
        es_ambulance.append(es)

distributed_es = {
    "fire_brigade": es_fire_brigade,
    "ambulance": es_ambulance,
    "garda": es_garda,
}

for disaster in disasters:
    all_services = {}
    nearest_services = {}

    es_of_consideration = []

    if disaster["disaster_type"] == 0:  # fire
        es_of_consideration = ["fire_brigade", "ambulance", "garda"]
    if disaster["disaster_type"] == 1:  # flood
        es_of_consideration = ["ambulance", "garda"]
    if disaster["disaster_type"] == 2:  # road_incident
        es_of_consideration = ["ambulance", "garda"]
    if disaster["disaster_type"] == 3:  # public_disturbance
        es_of_consideration = ["fire_brigade", "ambulance", "garda"]

    if es_of_consideration:
        for es in es_of_consideration:  # type: ignore
            x = {}
            for es_dict in distributed_es[es]:  # type: ignore
                x[es_dict["name"]] = hs.haversine(
                    (disaster["lat"], disaster["long"]),
                    (es_dict["lat"], es_dict["long"]),
                )
            all_services[es] = x

        print(all_services)

        for es_name, distances in all_services.items():
            for name, distance in distances.items():
                if distance == min(list(distances.values())):
                    nearest_services[es_name] = {name: distance}

        print(f"we want ==>{nearest_services}")
