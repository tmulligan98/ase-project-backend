from typing import Dict
import haversine as hs
from backend.database_wrapper.crud import (
    get_transport_services_db,
    add_ts_track_to_db,
    update_ts_db,
    update_es_db,
    add_track_to_db,
    get_emergency_services_db,
    update_disaster_status,
    get_emergency_service,
    get_transport_service,
    get_tracks_for_a_disaster,
)
from fastapi import APIRouter
import json
from backend.emergency_services.models import ServiceType

router = APIRouter()

MASS_EVACUATION_THRESHOLD = 6


class NearestServices:
    def __init__(self):
        self.data_to_return = {}

    @staticmethod
    def n_nearest_services(disaster: Dict, distributed_es: Dict):
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
            es_of_consideration = ["fire_brigade", "ambulance", "garda", "army"]
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
                        es_dict["id"],
                    )
                all_services[es] = x

            for (
                es_name,
                distances,
            ) in (
                all_services.items()
            ):  # get first, second and third nearest services of a disaster using haversine
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
                                "id": distance[6],
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
                                "id": distance[6],
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
                                "id": distance[6],
                            }
                        }
        return first_nearest_services, second_nearest_services, third_nearest_services

    @staticmethod
    def n_nearest_ts_services(disaster, distributed_ts):
        first_nearest_services = {}
        second_nearest_services = {}
        third_nearest_services = {}

        x = {}
        for ts_dict in distributed_ts["bus"]:  # type: ignore
            x[ts_dict["name"]] = (
                hs.haversine(
                    (disaster["lat"], disaster["long"]),
                    (ts_dict["lat"], ts_dict["long"]),
                ),
                ts_dict["lat"],
                ts_dict["long"],
                ts_dict["units"],
                ts_dict["units_available"],
                ts_dict["units_busy"],
                ts_dict["id"],
            )

        station_names_to_distances = {k: v[0] for k, v in x.items()}
        distances = [d[0] for d in x.values()]

        for (
            ts_name,
            distance,
        ) in (
            station_names_to_distances.items()
        ):  # get first, second and third nearest services of a disaster using haversine
            if distance == sorted(list(distances))[0]:
                first_nearest_services[ts_name] = {
                    ts_name: {
                        "distance": x[ts_name][0],
                        "lat": x[ts_name][1],
                        "long": x[ts_name][2],
                        "units": x[ts_name][3],
                        "units available": x[ts_name][4],
                        "units busy": x[ts_name][5],
                        "id": x[ts_name][6],
                    }
                }
            if distance == sorted(list(distances))[1]:
                second_nearest_services[ts_name] = {
                    ts_name: {
                        "distance": x[ts_name][0],
                        "lat": x[ts_name][1],
                        "long": x[ts_name][2],
                        "units": x[ts_name][3],
                        "units available": x[ts_name][4],
                        "units busy": x[ts_name][5],
                        "id": x[ts_name][6],
                    }
                }
            if distance == sorted(list(distances))[2]:
                third_nearest_services[ts_name] = {
                    ts_name: {
                        "distance": x[ts_name][0],
                        "lat": x[ts_name][1],
                        "long": x[ts_name][2],
                        "units": x[ts_name][3],
                        "units available": x[ts_name][4],
                        "units busy": x[ts_name][5],
                        "id": x[ts_name][6],
                    }
                }
        return first_nearest_services, second_nearest_services, third_nearest_services

    @staticmethod
    def fetch_updated_es(db):
        emergency_res = get_emergency_services_db(db, skip=0, limit=100)
        ers = []
        for er in emergency_res:
            ers.append(json.loads(er.json()))

        return ers

    @staticmethod
    def fetch_updated_ts(db):
        emergency_res = get_transport_services_db(db, skip=0, limit=100)
        ts = []
        for t in emergency_res:
            ts.append(json.loads(t.json()))

        return ts

    @staticmethod
    def distribute_services(emergency_services):
        es_garda = []
        es_fire_brigade = []
        es_ambulance = []
        es_army = []

        for es in emergency_services:
            if es["type"] == 0:
                es_garda.append(es)
            elif es["type"] == 1:
                es_fire_brigade.append(es)
            elif es["type"] == 2:
                es_ambulance.append(es)
            elif es["type"] == 3:
                es_army.append(es)

        distributed_es = {
            "fire_brigade": es_fire_brigade,
            "ambulance": es_ambulance,
            "garda": es_garda,
            "army": es_army,
        }
        return distributed_es

    @staticmethod
    def services_needed(disaster):
        no_services_needed = 0
        transport_services_required = 0
        if (
            disaster["scale"] <= 3
        ):  # assign services needed to deal with a disatser based on the scale of disaster
            no_services_needed = 2
        elif 3 < disaster["scale"] <= 6:
            no_services_needed = 3
        elif disaster["scale"] > 6:
            no_services_needed = 5
            transport_services_required = 3

        return no_services_needed, transport_services_required

    @staticmethod
    def allocate_services(
        first_nearest_services,
        second_nearest_services,
        third_nearest_services,
        no_services_needed,
        disaster,
        db,
    ):
        allocated_ambulance_station = []
        allocated_firebrigade_station = []
        allocated_garda_station = []
        allocated_army_station = []

        for x in [  # allocating services
            first_nearest_services,
            second_nearest_services,
            third_nearest_services,
        ]:
            if (
                not allocated_firebrigade_station
                or not allocated_ambulance_station
                or not allocated_garda_station
                or not allocated_army_station
            ):
                for service, info in x.items():
                    for name, details in info.items():
                        if (
                            service == "ambulance"
                            and details["units available"] != 0
                            and not allocated_ambulance_station
                        ):
                            if (
                                details["units available"] >= no_services_needed
                            ):  # see if the service can cater the no. of needed services
                                allocated_ambulance_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )

                                update_es_db(  # update emergency service table
                                    details["id"], no_services_needed, db=db
                                )
                                add_track_to_db(  # keep track of which services are busy with which disaster
                                    disaster["id"],
                                    details["id"],
                                    no_services_needed,
                                    db=db,
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
                                update_es_db(  # update emergency service table
                                    details["id"], no_services_needed, db=db
                                )
                                add_track_to_db(  # keep track of which services are busy with which disaster
                                    disaster["id"],
                                    details["id"],
                                    no_services_needed,
                                    db=db,
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
                                update_es_db(  # update emergency service table
                                    details["id"], no_services_needed, db=db
                                )
                                add_track_to_db(  # keep track of which services are busy with which disaster
                                    disaster["id"],
                                    details["id"],
                                    no_services_needed,
                                    db=db,
                                )

                        if (
                            service == "army"
                            and details["units available"] != 0
                            and not allocated_army_station
                        ):
                            if details["units available"] >= no_services_needed:
                                allocated_army_station.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )
                                update_es_db(  # update emergency service table
                                    details["id"], no_services_needed, db=db
                                )
                                add_track_to_db(  # keep track of which services are busy with which disaster
                                    disaster["id"],
                                    details["id"],
                                    no_services_needed,
                                    db=db,
                                )

        return (
            allocated_ambulance_station,
            allocated_garda_station,
            allocated_firebrigade_station,
            allocated_army_station,
        )

    @staticmethod
    def allocate_transport_services(
        first_nearest_services,
        second_nearest_services,
        third_nearest_services,
        no_services_needed,
        disaster,
        db,
    ):
        allocated_transport_service = []

        for x in [  # allocating services
            first_nearest_services,
            second_nearest_services,
            third_nearest_services,
        ]:
            if not allocated_transport_service:
                for service, info in x.items():
                    for name, details in info.items():

                        if details["units available"] != 0:
                            if details["units available"] >= no_services_needed:
                                allocated_transport_service.append(
                                    {
                                        "name": name,
                                        "distance": details["distance"],
                                        "lat": details["lat"],
                                        "long": details["long"],
                                    }
                                )
                                update_ts_db(  # update emergency service table
                                    details["id"], no_services_needed, db=db
                                )
                                add_ts_track_to_db(  # keep track of which services are busy with which disaster
                                    disaster["id"],
                                    details["id"],
                                    no_services_needed,
                                    db=db,
                                )

        return allocated_transport_service

    @staticmethod
    def update_already_addressed_status(d_id, status, db):
        update_disaster_status(d_id, status, db)

    def get_nearest_services(self, db, disasters):

        for disaster in disasters:
            if not disaster["already_addressed"] and disaster["verified"]:

                emergency_services = NearestServices.fetch_updated_es(db)
                transport_services = NearestServices.fetch_updated_ts(db)

                distributed_es = NearestServices.distribute_services(emergency_services)
                distributed_ts = {
                    "bus": transport_services,
                }

                (
                    first_nearest_services,
                    second_nearest_services,
                    third_nearest_services,
                ) = NearestServices.n_nearest_services(disaster, distributed_es)

                (
                    first_nearest_transport_services,
                    second_nearest_transport_services,
                    third_nearest_transport_services,
                ) = NearestServices.n_nearest_ts_services(disaster, distributed_ts)

                (
                    no_services_needed,
                    no_transport_services_needed,
                ) = NearestServices.services_needed(disaster)

                # Allocated ts
                (
                    allocated_transport_services
                ) = NearestServices.allocate_transport_services(
                    first_nearest_transport_services,
                    second_nearest_transport_services,
                    third_nearest_transport_services,
                    no_transport_services_needed,
                    disaster,
                    db,
                )

                # Allocated es
                (
                    allocated_ambulance_station,
                    allocated_garda_station,
                    allocated_firebrigade_station,
                    allocated_army_station,
                ) = NearestServices.allocate_services(
                    first_nearest_services,
                    second_nearest_services,
                    third_nearest_services,
                    no_services_needed,
                    disaster,
                    db,
                )

                self.data_to_return[disaster["id"]] = {
                    "ambulance": allocated_ambulance_station,
                    "police": allocated_garda_station,
                    "fire_brigade": allocated_firebrigade_station,
                    "transport_services": allocated_transport_services,
                    "army": allocated_army_station,
                }

                NearestServices.update_already_addressed_status(
                    disaster["id"], True, db
                )
            elif disaster["already_addressed"] and disaster["verified"]:
                tracks = get_tracks_for_a_disaster(db, disaster["id"])
                allocated_ambulance_station = []
                allocated_firebrigade_station = []
                allocated_garda_station = []
                allocated_transport_services = []
                allocated_army_station = []
                for row in tracks:

                    # If emergency service
                    if row.es_id is not None:
                        s = get_emergency_service(db, row.es_id)
                    # If transport service
                    elif row.ts_id is not None:
                        s = get_transport_service(db, row.ts_id)

                    # Assign service
                    service = {
                        "name": s.name,
                        "lat": s.lat,
                        "long": s.long,
                    }

                    if row.es_id is not None:
                        if s.type == ServiceType.GARDA:
                            allocated_garda_station.append(service)
                        elif s.type == ServiceType.FIRE_BRIGADE:
                            allocated_firebrigade_station.append(service)
                        elif s.type == ServiceType.AMBULANCE:
                            allocated_ambulance_station.append(service)
                        elif s.type == ServiceType.ARMY:
                            allocated_army_station.append(service)
                    else:
                        allocated_transport_services.append(service)

                self.data_to_return[disaster["id"]] = {
                    "ambulance": allocated_ambulance_station,
                    "police": allocated_garda_station,
                    "fire_brigade": allocated_firebrigade_station,
                    "transport_services": allocated_transport_services,
                    "army": allocated_army_station,
                }
        return self.data_to_return
