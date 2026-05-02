# PRD: sgBusLaoBu

## Overview
A Python Flask web app ("Bus Lao Bu" — Hokkien for "bus old lady/mother") that helps Singapore users find the nearest bus stop to their GPS location and see which buses will take them to a nearby MRT station. Uses official LTA DataMall bus stop, route, and service data stored in SQLite. Built as a school capstone project (IS214 or similar).

## Goals
- Detect or accept user's GPS coordinates (latitude, longitude)
- Find all bus stops within a configurable radius
- For each nearby bus stop, show which bus services connect to MRT stations and how many stops away
- Display bus company statistics (number of services per operator)
- Serve a mobile-friendly web interface

## Non-Goals
- Real-time arrival prediction (not using LTA real-time API)
- Trip planning across multiple bus changes
- MRT journey planning
- Native mobile app

## User Stories
- As a commuter, I want to find the nearest bus stop to my location and see which bus goes to an MRT station.
- As a user, I want to see how many stops away the nearest MRT interchange is for each bus option.
- As a curious person, I want to learn bus network statistics (how many services each operator runs).

## Tech Stack
- **Language**: Python 3.x
- **Framework**: Flask
- **Database**: SQLite (data loaded from JSON files at startup)
- **Libraries**: `flask`, `sqlite3` (stdlib), `math` (stdlib)
- **Data**: LTA DataMall JSON exports (bus_stops.json, bus_services.json, bus_routes.json)
- **Deployment**: Vercel (Python serverless)

## Architecture
```
sgBusLaoBu2021/
├── main.py           # Flask app + routes
├── functions.py      # BusStops, BusCompanies classes + helper functions
├── sqlcommands.py    # SQL query constants dict
├── database.yml      # Database config
├── vercel.json       # Vercel deployment config
├── api/              # Vercel API handlers
├── data/
│   ├── json/         # LTA JSON data (bus_stops, bus_services, bus_routes)
│   └── txt/          # coordinates log
└── fare_data/        # Fare reference files
```

**Key Classes:**
- `BusStops` — wraps SQLite queries for stop lookup + distance calculation
- `BusCompanies` — wraps bus service stats by operator (SMRT, SBST, TTS, GAS)

**Routes:**
- `GET /` → home page
- `POST/GET /getyourlocation` → location capture page with radius slider
- `POST /findabus` → finds buses from location to MRT
- `GET /learnbusfacts` → operator statistics page
- `GET /help` → help page
- `GET /coordinates` → log of past coordinates searched

## Features (detailed)

### Location + Radius Input
- `GET /getyourlocation`: renders page with a radius slider (default 0.2 km)
- User either grants GPS or enters coords manually
- Radius configurable via slider: 0.1–1.0 km

### Bus Stop Discovery
- POSTs user lat/lon + radius to `/findabus`
- `BusStops.getbusstopdistance()` queries SQLite for stops within radius km
- Returns stops sorted by walking distance (metres)

### MRT Connection Finder
- For each nearby bus stop: cross-references with `allmrtbusstops` (pre-loaded at startup)
- If a service/direction matches → finds stop sequence difference = number of stops to MRT
- Computes MRT line color for visual display (NSL red, EWL green, NEL purple, CCL orange, DTL blue, TEL brown)
- Returns structured dict per connection: walk distance, bus service, stops count, MRT station + line, board/alight stop descriptions

### Bus Facts Page
- Shows breakdown of services by bus operator category
- Operators: SMRT, SBST, TTS, GAS
- Data pre-computed at server startup from `bus_services.json`

### Coordinates Log
- Appends each user search location to `data/txt/coordinates.txt` (via `export_json`)
- Displays past searches at `/coordinates`

## Database Schema (SQLite)
Three tables loaded from JSON at startup (if not already populated):
- `busstops` — `BusStopCode`, `Description`, `RoadName`, `Latitude`, `Longitude`
- `busservices` — `ServiceNo`, `Operator`, `Category`, `Direction`
- `busroutes` — `ServiceNo`, `Direction`, `StopSequence`, `BusStopCode`, `Distance`

## Environment Variables
None required for local run. `vercel.json` configures serverless routes.

## Deployment / Run
```bash
pip install flask
python main.py
# open http://localhost:5000
```

**Vercel:**
```bash
vercel --prod
```

## Constraints & Notes
- **Static data**: bus routes are a snapshot of LTA data — not live; route changes won't be reflected without a data refresh
- **Haversine vs Euclidean**: distance uses a simplified formula (suitable for Singapore's small geographic area)
- **MRT bus stop matching**: matches based on `ServiceNo` + `Direction` — requires MRT interchange bus stops to be pre-tagged in the `allmrtbusstops` set
- **No authentication**: open access; coordinates log is public at `/coordinates`
- **Cache-Control headers**: all responses set no-cache to prevent stale data
