import haversine as hs
from backend.database_wrapper.crud import update_es_db, add_track_to_db
from fastapi import APIRouter
from backend.database_wrapper import get_db

router = APIRouter()


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

            for x in [
                first_nearest_services,
                second_nearest_services,
                third_nearest_services,
            ]:
                if (
                    not allocated_firebrigade_station
                    or not allocated_ambulance_station
                    or not allocated_garda_station
                ):
                    for service, info in x.items():
                        for name, details in info.items():
                            if (
                                service == "ambulance"
                                and details["units available"] != 0
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

                                    update_es_db(
                                        details["id"], no_services_needed, db=get_db()
                                    )
                                    add_track_to_db(
                                        disaster["id"],
                                        details["id"],
                                        no_services_needed,
                                        db=get_db(),
                                    )

                                    # update es table update_es(id, units_allocated=no_services_needed)
                                    # requests.put(
                                    #     "http://127.0.0.1:8000/api/1/update_emergency_service",
                                    #     json={
                                    #         "es_id": disaster["id"],
                                    #         "units_allocated": no_services_needed,
                                    #     },
                                    # )
                                    # requests.post(
                                    #     "http://127.0.0.1:8000/api/1/keep_track",
                                    #     json={
                                    #         "disaster_id": disaster["id"],
                                    #         "es_id": details["id"],
                                    #         "units_busy": no_services_needed,
                                    #     },
                                    # )
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
                                    # update database entries

                            if (
                                service == "fire_brigade"
                                and details["units available"] != 0
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
                                    # update database entries

            data_to_return[disaster["id"]] = {
                "ambulance": allocated_ambulance_station,
                "police": allocated_garda_station,
                "fire_brigade": allocated_firebrigade_station,
            }

    return data_to_return
