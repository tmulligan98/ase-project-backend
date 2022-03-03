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
                        es_dict["units"],
                        es_dict["units_available"],
                        es_dict["units_busy"],
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
                                "units": distance[3],
                                "units available": distance[4],
                                "units busy": distance[5],
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
                                "units": distance[3],
                                "units available": distance[4],
                                "units busy": distance[5],
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
                                "units": distance[3],
                                "units available": distance[4],
                                "units busy": distance[5],
                            }
                        }

            no_services_needed = 0

            if disaster["scale"] <= 3:
                no_services_needed = 2
            elif disaster["scale"] > 3 and disaster["scale"] <= 6:
                no_services_needed = 3
            elif disaster["scale"] > 6:
                no_services_needed = 5

            allocated_ambulance_station = []
            allocated_firebrigade_station = []
            allocated_garda_station = []

            for service, info in first_nearest_services.items():
                for name, details in info.items():
                    if service == "ambulance" and details["units available"] != 0:
                        if details["units available"] >= no_services_needed:
                            allocated_ambulance_station.append(
                                {
                                    "name": name,
                                    "distance": details["distance"],
                                    "lat": details["lat"],
                                    "long": details["long"],
                                }
                            )
                    if service == "garda" and details["units available"] != 0:
                        if details["units available"] >= no_services_needed:
                            allocated_garda_station.append(
                                {
                                    "name": name,
                                    "distance": details["distance"],
                                    "lat": details["lat"],
                                    "long": details["long"],
                                }
                            )

                    if service == "fire_brigade" and details["units available"] != 0:
                        if details["units available"] >= no_services_needed:
                            allocated_firebrigade_station.append(
                                {
                                    "name": name,
                                    "distance": details["distance"],
                                    "lat": details["lat"],
                                    "long": details["long"],
                                }
                            )

            if (
                not allocated_firebrigade_station
                or not allocated_ambulance_station
                or not allocated_garda_station
            ):
                for service, info in second_nearest_services.items():
                    for name, details in info.items():
                        if (
                            service == "ambulance"
                            and details["units available"] != 0
                            and not allocated_ambulance_station
                        ):
                            if details["units available"] >= no_services_needed:
                                allocated_ambulance_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )

                        if (
                            service == "garda"
                            and details["units available"] != 0
                            and not allocated_garda_station
                        ):
                            if details["units available"] >= no_services_needed:
                                allocated_garda_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )

                        if (
                            service == "fire_brigade"
                            and details["units available"] != 0
                            and not allocated_firebrigade_station
                        ):
                            if details["units available"] >= no_services_needed:
                                allocated_firebrigade_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )

            if (
                not allocated_firebrigade_station
                or not allocated_ambulance_station
                or not allocated_garda_station
            ):
                for service, info in third_nearest_services.items():
                    for name, details in info.items():
                        if (
                            service == "ambulance"
                            and details["units available"] != 0
                            and not allocated_ambulance_station
                        ):
                            if details["units available"] >= no_services_needed:
                                allocated_ambulance_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )

                        if (
                            service == "garda"
                            and details["units available"] != 0
                            and not allocated_garda_station
                        ):
                            if details["units available"] >= no_services_needed:
                                allocated_garda_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )

                        if (
                            service == "fire_brigade"
                            and details["units available"] != 0
                            and not allocated_firebrigade_station
                        ):
                            if details["units available"] >= no_services_needed:
                                allocated_firebrigade_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )

            data_to_return[disaster["id"]] = {
                "ambulance": allocated_ambulance_station,
                "police": allocated_garda_station,
                "fire_brigade": allocated_firebrigade_station,
            }

    return data_to_return


disasters = [
    {
        "lat": 53.35872554821418,
        "long": -6.309242248535156,
        "scale": 9,
        "disaster_type": 4,
        "radius": 300,
        "id": "1",
    }
]
emergency_services = [
    {
        "name": "Rotunda Hospital",
        "type": 2,
        "lat": 53.353,
        "long": -6.26351,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Mater Private Hospital",
        "type": 2,
        "lat": 53.35808,
        "long": -6.26446,
        "units": 3,
        "units_available": 120,
        "units_busy": 0,
    },
    {
        "name": "Temple Street Hospital",
        "type": 2,
        "lat": 53.356915045655334,
        "long": -6.261492759885292,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "National Maternity Hospital",
        "type": 2,
        "lat": 53.34013,
        "long": -6.2456,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Eye and Ear Hostpital",
        "type": 2,
        "lat": 53.33259626317416,
        "long": -6.256061878919393,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "The Meath Primary Care Centre",
        "type": 2,
        "lat": 53.33585,
        "long": -6.27019,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Main Hospital",
        "type": 2,
        "lat": 53.33932,
        "long": -6.29596,
        "units": 2,
        "units_available": 2,
        "units_busy": 0,
    },
    {
        "name": "Coombe Women & Infants Hospital",
        "type": 2,
        "lat": 53.33461,
        "long": -6.28833,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Kevin Street Garda Sation",
        "type": 0,
        "lat": 53.33954610143664,
        "long": -6.26760370818894,
        "units": 1,
        "units_available": 12,
        "units_busy": 0,
    },
    {
        "name": "Harcourt Square Garda Station",
        "type": 0,
        "lat": 53.33424,
        "long": -6.26375,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Store Street Garda Station",
        "type": 0,
        "lat": 53.35051251814404,
        "long": -6.252324274656007,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Pearse Street Garda Station",
        "type": 0,
        "lat": 53.34577194438715,
        "long": -6.256204230480236,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "DonnyBrook Garda Station",
        "type": 0,
        "lat": 53.32156,
        "long": -6.23615,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Fire Brigade HQ",
        "type": 1,
        "lat": 53.346259552984044,
        "long": -6.253118230748194,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "North Strand Fire Station",
        "type": 1,
        "lat": 53.36039726282362,
        "long": -6.2396093774148245,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Phibsborough Fire Station",
        "type": 1,
        "lat": 53.35834420442677,
        "long": -6.273821993325792,
        "units": 2,
        "units_available": 22,
        "units_busy": 0,
    },
    {
        "name": "Blanchardstown Fire Station",
        "type": 1,
        "lat": 53.38465,
        "long": -6.39612,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
    {
        "name": "Donnybrook fire station",
        "type": 1,
        "lat": 53.3219,
        "long": -6.23743,
        "units": 6,
        "units_available": 6,
        "units_busy": 0,
    },
]
get_nearest_services(disasters, emergency_services)
