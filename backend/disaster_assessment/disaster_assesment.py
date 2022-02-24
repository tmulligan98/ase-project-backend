# import requests
import requests
import haversine as hs


def get_nearest_services():
    # data_to_return = {}
    disasters = requests.get(
        "https://ase-backend-2.herokuapp.com/api/1/disasters/?skip=0&limit=100"
    ).json()
    emergency_services = requests.get(
        "https://ase-backend-2.herokuapp.com/api/1/emergency_services/?skip=0&limit=100"
    ).json()

    # es_distances_from_disaster = []  # type: List[List]

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

        if es_of_consideration:
            for es in es_of_consideration:  # type: ignore
                x = {}
                for es_dict in distributed_es[es]:  # type: ignore
                    x[es_dict["name"]] = hs.haversine(
                        (disaster["lat"], disaster["long"]),
                        (es_dict["lat"], es_dict["long"]),
                    )
                all_services[es] = x

            print(f"all services ==> {all_services}")

            for es_name, distances in all_services.items():
                for name, distance in distances.items():
                    if distance == sorted(list(distances.values()))[0]:
                        first_nearest_services[es_name] = {name: distance}
                    if distance == sorted(list(distances.values()))[1]:
                        second_nearest_services[es_name] = {name: distance}
                    if distance == sorted(list(distances.values()))[2]:
                        third_nearest_services[es_name] = {name: distance}

            print(f"first nearest ==>{first_nearest_services}")
            print(f"second nearest ==>{second_nearest_services}")
            print(f"third nearest ==>{third_nearest_services}")


get_nearest_services()
