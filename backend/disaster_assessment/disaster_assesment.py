import haversine as hs


def get_nearest_services(disasters, emergency_services):
    data_to_return = {}
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

            ambulances = []
            garda = []
            fire_brigade = []
            for service, info in first_nearest_services.items():
                for name, details in info.items():
                    if service == "ambulance":
                        ambulances.append({**{"name": name}, **details})
                    if service == "garda":
                        garda.append({**{"name": name}, **details})
                    if service == "fire_brigade":
                        fire_brigade.append({**{"name": name}, **details})

            for service, info in second_nearest_services.items():
                for name, details in info.items():
                    if service == "ambulance":
                        ambulances.append({**{"name": name}, **details})
                    if service == "garda":
                        garda.append({**{"name": name}, **details})
                    if service == "fire_brigade":
                        fire_brigade.append({**{"name": name}, **details})

            for service, info in third_nearest_services.items():
                for name, details in info.items():
                    if service == "ambulance":
                        ambulances.append({**{"name": name}, **details})
                    if service == "garda":
                        garda.append({**{"name": name}, **details})
                    if service == "fire_brigade":
                        fire_brigade.append({**{"name": name}, **details})

            data_to_return[disaster["id"]] = {
                "ambulance": ambulances,
                "police": garda,
                "fire_brigade": fire_brigade,
            }

    return data_to_return
