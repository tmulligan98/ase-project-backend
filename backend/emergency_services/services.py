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
        name="CHI at Temple Street",
        type=ServiceType.AMBULANCE,
        lat=53.35691,
        long=-6.26109,
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
        name="Eye and Ear Hospital",
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
        name="Tallaght University Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.29112,
        long=-6.37716,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="St James's Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.33944,
        long=-6.29602,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="St Vincent's University Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.31730,
        long=-6.21445,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="The Mater Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.35906,
        long=-6.26827,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Beaumont Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.39054,
        long=-6.22392,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Connolly Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.38849,
        long=-6.36889,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="CHI at Crumlin",
        type=ServiceType.AMBULANCE,
        lat=53.32666,
        long=-6.31658,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Beacon Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.27589,
        long=-6.21921,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Blackrock Health Blackrock Clinic",
        type=ServiceType.AMBULANCE,
        lat=53.30503,
        long=-6.18727,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Bon Secours Hospital Dublin",
        type=ServiceType.AMBULANCE,
        lat=53.37604,
        long=-6.26654,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Hermitage Clinic",
        type=ServiceType.AMBULANCE,
        lat=53.35939,
        long=-6.40469,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Highfield Healthcare",
        type=ServiceType.AMBULANCE,
        lat=53.37858,
        long=-6.24435,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Mount Carmel Community Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.30458,
        long=-6.26420,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="St John of God Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.28478,
        long=-6.19151,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Sports Surgery Clinic",
        type=ServiceType.AMBULANCE,
        lat=53.40424,
        long=-6.25344,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="St Patrick's University Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.34431,
        long=-6.29286,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="St Vincent's Private Hospital",
        type=ServiceType.AMBULANCE,
        lat=53.31549,
        long=-6.20843,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Kevin Street Garda Station",
        type=ServiceType.GARDA,
        lat=53.338982,
        long=-6.270248,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Ballyfermot Garda Station",
        type=ServiceType.GARDA,
        lat=53.34485,
        long=-6.35734,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Ballymun Garda Station",
        type=ServiceType.GARDA,
        lat=53.39443,
        long=-6.26327,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Blanchardstown Garda Station",
        type=ServiceType.GARDA,
        lat=53.39014,
        long=-6.38049,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Bridewell Garda Station",
        type=ServiceType.GARDA,
        lat=53.34719,
        long=-6.27359,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Cabinteely Garda Station",
        type=ServiceType.GARDA,
        lat=53.26091,
        long=-6.14981,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Cabra Garda Station",
        type=ServiceType.GARDA,
        lat=53.36507,
        long=-6.30659,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Clondalkin Garda Station",
        type=ServiceType.GARDA,
        lat=53.323146,
        long=-6.394958,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Clontarf Garda Station",
        type=ServiceType.GARDA,
        lat=53.363544,
        long=-6.220152,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Coolock Garda Station",
        type=ServiceType.GARDA,
        lat=53.390335,
        long=-6.201099,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Crumlin Garda Station",
        type=ServiceType.GARDA,
        lat=53.319567,
        long=-6.315017,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Dublin Airport Garda Station",
        type=ServiceType.GARDA,
        lat=53.429782,
        long=-6.24501,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Dundrum Garda Station",
        type=ServiceType.GARDA,
        lat=53.289544,
        long=-6.242572,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Finglas Garda Station",
        type=ServiceType.GARDA,
        lat=53.389651,
        long=-6.306919,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Fitzgibbon Street Garda Station",
        type=ServiceType.GARDA,
        lat=53.357735,
        long=-6.255359,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Irishtown Garda Station",
        type=ServiceType.GARDA,
        lat=53.338063,
        long=-6.22304,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Kilmainham Garda Station",
        type=ServiceType.GARDA,
        lat=53.341869,
        long=-6.304273,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Mountjoy Garda Station",
        type=ServiceType.GARDA,
        lat=53.360484,
        long=-6.266825,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Rathfarnham Garda Station",
        type=ServiceType.GARDA,
        lat=53.297388,
        long=-6.28815,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Rathmines Garda Station",
        type=ServiceType.GARDA,
        lat=53.321317,
        long=-6.267004,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Ronanstown Garda Station",
        type=ServiceType.GARDA,
        lat=53.337899,
        long=-6.406023,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Santry Garda Station",
        type=ServiceType.GARDA,
        lat=53.389728,
        long=-6.251635,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Shankill Garda Station",
        type=ServiceType.GARDA,
        lat=53.233524,
        long=-6.121017,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Stepaside Garda Station",
        type=ServiceType.GARDA,
        lat=53.253332,
        long=-6.214520,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Sundrive Road Garda Station",
        type=ServiceType.GARDA,
        lat=53.330191,
        long=-6.298731,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Tallaght Garda Station",
        type=ServiceType.GARDA,
        lat=53.286801,
        long=-6.367838,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Terenure Garda Station",
        type=ServiceType.GARDA,
        lat=53.309815,
        long=-6.288029,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Store Street Garda Station",
        type=ServiceType.GARDA,
        lat=53.350455,
        long=-6.252246,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Pearse Street Garda Station",
        type=ServiceType.GARDA,
        lat=53.345702,
        long=-6.256269,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Raheny Garda Station",
        type=ServiceType.GARDA,
        lat=53.378983,
        long=-6.177986,
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
        name="Dolphin's Barn Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.33198553083167,
        long=-6.28886875969066,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="North Strand Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.360273781628614,
        long=-6.235945013102858,
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
        lat=53.38520639753301,
        long=-6.3917930676090995,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Donnybrook Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.322582861657196,
        long=-6.233524113667585,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Dublin Fire Brigade Training Centre",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.37092994428396,
        long=-6.227518244675837,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Finglas Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.39057506761182,
        long=-6.299653021032384,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Kilbarrack Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.39118924721457,
        long=-6.164804882402514,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Rathfarnham Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.292475331705525,
        long=-6.261160628478722,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Tallaght Fire Station",
        type=ServiceType.FIRE_BRIGADE,
        lat=53.30764665015575,
        long=-6.380908519434323,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Cathal Brugha Barracks",
        type=ServiceType.ARMY,
        lat=53.32717172461035,
        long=-6.269010645901547,
        units=6,
        units_available=6,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="McKee Barracks",
        type=ServiceType.ARMY,
        lat=53.35757090815345,
        long=-6.299799975185834,
        units=10,
        units_available=10,
        units_busy=0,
    ),
    EmergencyServiceModel(
        name="Baldonnell",
        type=ServiceType.ARMY,
        lat=53.308449179536126,
        long=-6.440892096339786,
        units=10,
        units_available=10,
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
