import haversine as hs

import json


def get_nearest_services(disasters, emergency_services):
    data_to_return = {}

    # disasters = requests.get(
    #     "https://ase-backend-2.herokuapp.com/api/1/disasters/?skip=0&limit=100"
    # ).json()
    # emergency_services = requests.get(
    #     "https://ase-backend-2.herokuapp.com/api/1/emergency_services/?skip=0&limit=100"
    # ).json()

    # es_distances_from_disaster = []  # type: List[List]

    # x = requests.post("https://ase-backend-2.herokuapp.com/api/1/disasters-civ/", json={
    #   "lat": 23,
    #   "long": 23.5,
    #   "scale": 6,
    #   "disaster_type": 1,
    #   "radius": 10,
    # })

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
    disaster_id = 0
    for disaster in disasters:
        disaster_id += 1
        all_services = {}
        first_nearest_services = {}
        second_nearest_services = {}
        third_nearest_services = {}
        es_of_consideration = []

        if disaster["disaster_type"] == 0:  # fire
            es_of_consideration = ["fire_brigade", "ambulance", "garda"]
        if disaster["disaster_type"] == 1:  # flood
            es_of_consideration = ["ambulance", "garda"]
        if disaster["disaster_type"] == 2:  # road_incident
            es_of_consideration = ["ambulance", "garda"]
        if disaster["disaster_type"] == 3:  # public_disturbance
            es_of_consideration = ["fire_brigade", "ambulance", "garda"]
        if disaster["disaster_type"] == 4:  # bio_hazard
            es_of_consideration = ["fire_brigade", "ambulance", "garda"]
        if disaster["disaster_type"] == 5:  # meteor
            es_of_consideration = ["fire_brigade", "ambulance", "garda"]
        if disaster["disaster_type"] == 6:  # storm
            es_of_consideration = ["fire_brigade", "ambulance", "garda"]
        if disaster["disaster_type"] == 7:  # other
            es_of_consideration = ["fire_brigade", "ambulance", "garda"]

        if es_of_consideration:
            for es in es_of_consideration:  # type: ignore
                x = {}
                for es_dict in distributed_es[es]:  # type: ignore
                    x[es_dict["name"]] = (
                        hs.haversine(
                            (disaster["lat"], disaster["long"]),
                            (es_dict["lat"], es_dict["long"]),
                        ),
                        es_dict["lat"],
                        es_dict["long"],
                    )
                all_services[es] = x

            for es_name, distances in all_services.items():
                for name, distance in distances.items():
                    if (
                        distance
                        == sorted(list(distances.values()), key=lambda t: t[0])[0]
                    ):
                        first_nearest_services[es_name] = {
                            name: {
                                "distance": distance[0],
                                "lat": distance[1],
                                "long": distance[2],
                            }
                        }
                    if (
                        distance
                        == sorted(list(distances.values()), key=lambda t: t[0])[1]
                    ):
                        second_nearest_services[es_name] = {
                            name: {
                                "distance": distance[0],
                                "lat": distance[1],
                                "long": distance[2],
                            }
                        }
                    if (
                        distance
                        == sorted(list(distances.values()), key=lambda t: t[0])[2]
                    ):
                        third_nearest_services[es_name] = {
                            name: {
                                "distance": distance[0],
                                "lat": distance[1],
                                "long": distance[2],
                            }
                        }

            data_to_return[disaster_id] = {
                "first nearest": first_nearest_services,
                "second nearest": second_nearest_services,
                "third nearest": third_nearest_services,
            }

    json_object = json.dumps(data_to_return, indent=4)

    with open("return.json", "w") as outfile:
        outfile.write(json_object)

    return data_to_return
