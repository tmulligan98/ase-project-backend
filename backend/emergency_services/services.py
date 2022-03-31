from .models import EmergencyServiceModel, ServiceType, TransportServiceModel


EMERGENCY_SERVICES = [
    EmergencyServiceModel(
        name="Rotunda Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.353,
        long=-6.26351,
        units=12,
        units_available=12,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Mater Private Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.35808,
        long=-6.26446,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Temple Street Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.356915045655334,
        long=-6.261492759885292,
        units=15,
        units_available=15,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="National Maternity Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.34013,
        long=-6.2456,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Eye and Ear Hostpital",
        type=ServiceType.AMBULANCE,
        lat=53.33259626317416,
        long=-6.256061878919393,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="The Meath Primary Care Centre",
        type=ServiceType.AMBULANCE,
        lat=53.33585,
        long=-6.27019,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Main Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.33932,
        long=-6.29596,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Coombe Women & Infants Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.33461,
        long=-6.28833,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Kevin Street Garda Sation",
        type=ServiceType.GARDA,
        lat=53.33954610143664,
        long=-6.26760370818894,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Harcourt Square Garda Station",
        type=ServiceType.GARDA,
        lat=53.33424,
        long=-6.26375,
        units=20,
        units_available=20,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Store Street Garda Station",
        type=ServiceType.GARDA,
        lat=53.35051251814404,
        long=-6.252324274656007,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Pearse Street Garda Station",
        type=ServiceType.GARDA,
        lat=53.34577194438715,
        long=-6.256204230480236,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="DonnyBrook Garda Station",
        type=ServiceType.GARDA,
        lat=53.32156,
        long=-6.23615,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Fire Brigade HQ",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.346259552984044,
        long=-6.253118230748194,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="North Strand Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.36039726282362,
        long=-6.2396093774148245,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Phibsborough Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.35834420442677,
        long=-6.273821993325792,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Blanchardstown Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.38465,
        long=-6.39612,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Donnybrook fire station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.3219,
        long=-6.23743,
        units=6,
        units_available=6,
        units_busy=0,
    ),
]

TRANSPORT_SERVICES = [
    TransportServiceModel(
        name="Busáras",
        lat=53.349764834055144,
        long=-6.252164915261029,
        units=20,
        units_available=20,
        units_busy=0,
    ),
    TransportServiceModel(
        name="Dublin Bus Garage Ringsend",
        lat=53.34187548718383,
        long=-6.232750850392618,
        units=20,
        units_available=20,
        units_busy=0,
    ),
    TransportServiceModel(
        name="Dublin Bus Garage Summerhill",
        lat=53.356047854547164,
        long=-6.254982613313899,
        units=25,
        units_available=25,
        units_busy=0,
    ),
]
