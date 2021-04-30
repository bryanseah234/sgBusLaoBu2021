'''
a dictionary containing key value pairs of sql commands, key is variable name, value is sql command as a string
'''

commands = {
    "createbusroutestable" : '''
        CREATE TABLE IF NOT EXISTS Bus_Routes
            (
                ServiceNo INTEGER,
                Direction INTEGER,
                StopSequence INTEGER,
                BusStopCode INTEGER,
                WD_FirstBus INTEGER,
                WD_LastBus INTEGER,
                SAT_FirstBus INTEGER,
                SAT_LastBus INTEGER,
                SUN_FirstBus INTEGER,
                SUN_LastBus INTEGER,
                PRIMARY KEY (ServiceNo,Direction,Stopsequence)
                FOREIGN KEY(BusStopCode) REFERENCES Bus_Stops(BusStopCode)
                FOREIGN KEY(ServiceNo) REFERENCES Bus_Services(ServiceNo)
            )
        ''', 
    
    "insertbusroutes" : '''
    INSERT INTO Bus_Routes
    (ServiceNo , Direction , StopSequence , BusStopCode , WD_FirstBus , WD_LastBus , SAT_FirstBus , SAT_LastBus , SUN_FirstBus , SUN_LastBus)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', 
    
    "createbusservicestable" : '''
    CREATE TABLE IF NOT EXISTS Bus_Services
    (
        ServiceNo INTEGER,
        Direction INTEGER,
        AM_Peak_Freq TEXT,
        AM_Offpeak_Freq TEXT,
        PM_Peak_Freq TEXT,
        PM_Offpeak_Freq TEXT,
        PRIMARY KEY (ServiceNo,Direction)
    )
    ''', 
    
    "insertbusservices" : '''
    INSERT INTO Bus_Services
    (ServiceNo , Direction , AM_Peak_Freq , AM_Offpeak_Freq , PM_Peak_Freq , PM_Offpeak_Freq)
    VALUES (?, ?, ?, ?, ?, ?)
    ''' , 
    
    "createbusstopstable" : '''
    CREATE TABLE IF NOT EXISTS Bus_Stops
    (
        BusStopCode INTEGER,
        Description TEXT,
        Latitude REAL,
        Longitude REAL,
        PRIMARY KEY (BusStopCode)
    )
    ''' , 
    
    "insertbusstops" : '''
    INSERT INTO Bus_Stops
    (BusStopCode , Description , Latitude , Longitude)
    VALUES (?, ?, ?, ?)
    ''',


    "selectfromdatabase" : '''
    SELECT * 
    FROM Bus_Stops 
    INNER JOIN Bus_Routes 
    ON Bus_Stops.BusStopCode = Bus_Routes.BusStopCode
    ''',

    "findstopsequence" : '''
    SELECT * 
    FROM Bus_Routes
    WHERE Bus_Routes.ServiceNo = ?
    AND Bus_Routes.Direction = ?
    AND Bus_Routes.BusStopCode = ?
    ''',    
    }