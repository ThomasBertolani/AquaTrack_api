# AquaTrack API

The AquaTrack API provides access to the river monitoring system, allowing you to query information about rivers, devices, and environmental sensor readings.

The data available includes:
- **Water Level**
- **TDS (Total Dissolved Solids)**
- **Turbidity**
- **pH**
- **Temperature**

## Usage

### 1. Get a List of Rivers

**Endpoint**: `/rivers`  
**Method**: `GET`

Fetch a list of all rivers in the system.

**Request**:
```http
GET /rivers
```
**Response**:
```json
[
  {
    "id": 1,
    "name": "River A"
  },
  {
    "id": 2,
    "name": "River B"
  }
]
```

### 2. Get Devices in a River

**Endpoint**: `/devices_in_river/{river_id}`  
**Method**: `GET`

Fetch a list of all devices installed in a specific river.

**Request**:
```http
GET /devices_in_river/1
```
**Response**:
```json
[
  {
    "device_id": 1
  },
  {
    "device_id": 2
  }
]
```

### 3. Get Sensor Readings for a Device

**Endpoint**: `/device_readings/{river_id}_{device_id}`  
**Method**: `GET`

Fetch sensor readings from a specific device in a river. You can filter by sensor column and date range.

#### Optional Query Parameters:

- **`column`**:  
  Specify a specific sensor column to retrieve. Choose from the following:
  - `water_level`
  - `tds` (Total Dissolved Solids)
  - `turbidity`
  - `ph`
  - `temperature`

  If not specified, the response will include all available sensor data (water level, TDS, turbidity, pH, temperature).

- **`start`**:  
  Filter readings starting from this date and time. Must be in ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`).

- **`end`**:  
  Filter readings until this date and time. Must be in ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`).

**Request without filters**:
```http
GET /device_readings/1_1
```
**Response**:
```json
[
  {
    "recorded_at": "2024-12-23T12:00:00",
    "water_level": 5.1,
    "tds": 395,
    "turbidity": 11,
    "ph": 7.3,
    "temperature": 18
  },
  {
    "recorded_at": "2024-12-24T12:00:00",
    "water_level": 5.3,
    "tds": 400,
    "turbidity": 12,
    "ph": 7.4,
    "temperature": 17
  },
  {
    "recorded_at": "2024-12-25T12:00:00",
    "water_level": 5.5,
    "tds": 410,
    "turbidity": 13,
    "ph": 7.5,
    "temperature": 16
  },
  {
    "recorded_at": "2024-12-26T12:00:00",
    "water_level": 5.6,
    "tds": 420,
    "turbidity": 14,
    "ph": 7.6,
    "temperature": 17
  }
]
```

**Request with filters**:
```http
GET /device_readings/1_1?column=temperature&start=2024-12-24T00:00:00&end=2024-12-26T00:00:00
```
**Response**:
```json
[
  {
    "recorded_at": "2024-12-24T12:00:00",
    "temperature": 17
  },
  {
    "recorded_at": "2024-12-25T12:00:00",
    "temperature": 16
  }
]
```

## API Accessibility

The AquaTrack API is reachable through the following URL:

`https://aquatrack-api-ksn9.onrender.com`

You can use this base URL to access all the available endpoints mentioned in the documentation.
