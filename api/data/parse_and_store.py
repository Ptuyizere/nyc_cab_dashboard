import re
import sys
import csv
import math
import sqlite3
from datetime import datetime

# Data extremes to weed out anomalies

# We ignore trips that have a speed higher than the speed limit in nyc
MAX_REASONABLE_SPEED = 80.0
# Consider trip round if start and end fall within 0.2 km
ROUND_TRIP_THRESHOLD = 0.2
# Approximate coordinates to determine if trip location was in NYC 
MIN_LATITUDE = 40.4774
MAX_LATITUDE = 40.9176
MIN_LONGITUDE = -74.2591
MAX_LONGITUDE = -73.7004

# Helper functions to clean and prepare data

def parse_datetime(value: str):
    """Convert string to datetime object"""
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None

def distance(lat1, lon1, lat2, lon2):
    """Compute the trip's distance given lat and lon"""
    R = 6371.0
    try:
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon2, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat2)*math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    except Exception:
        return None

def if_in_nyc(lat, lon):
    """Check if coordinates are within NYC"""
    return MIN_LATITUDE <= lat <= MAX_LATITUDE and MIN_LONGITUDE <= lon <= MAX_LONGITUDE

def extract_number_id(raw_id: str):
    """Extracts number id from string value in csv that looks like this 'id2875421'"""
    if raw_id is None:
        return None
    s = str(raw_id)
    m = re.search(r'(\d+)', s)
    if not m:
        return None, None
    digits = m.group(1)
    try:
        intval = int(digits)
    except Exception:
        return digits, None
    return digits, intval

def merge(left, right):
    """Merge two sorted lists into one sorted list"""
    i, j = 0, 0
    merged = []
    while i < len(left) and j < len(right):
        left_id = left[i][0]
        right_id = right[j][0]
        if left_id is None:
            if right_id is None:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        elif right_id is None:
            merged.append(left[i])
            i += 1
        else:
            if left_id <= right_id:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged

def merge_sort(list_to_sort):
    """Recursive merge sort"""
    n = len(list_to_sort)
    if n <= 1:
        # Automatically sorted
        return list_to_sort[:]
    mid = n // 2
    left = merge_sort(list_to_sort[:mid])
    right = merge_sort(list_to_sort[mid:])
    return merge(left, right)

def load_and_extract(input_csv, excluded_csv):
    """Read CSV, extract numeric IDs and write excluded rows to exlcuded_csv"""
    
    results = []
    seen_original_ids = set()

    excl_file = open(excluded_csv, "w", encoding="utf-8")
    excl_writer = csv.writer(excl_file)
    excl_writer.writerow(["raw_id", "reason", "sample_fields"])

    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_id = row.get("id")
            
            # Check if ID is there
            if raw_id is None or str(raw_id).strip() == "":
                excl_writer.writerow(["", "missing_id", f"{row.get('pickup_datetime')}"])
                continue
            raw_id_str = str(raw_id).strip()

            # Check for duplicate ID
            if raw_id_str in seen_original_ids:
                excl_writer.writerow([raw_id_str, "duplicate_id", f"{row.get('pickup_datetime')}"])
                continue
            seen_original_ids.add(raw_id_str)

            # Extract numeric portion from ID
            digits_str, intval = extract_number_id(raw_id_str)
            if digits_str is None or intval is None:
                excl_writer.writerow([raw_id_str, "invalid_id_format", f"{row.get('pickup_datetime')}"])
                continue

            # Key fields validation

            pickup_time = row.get("pickup_datetime")
            dropoff_time = row.get("dropoff_datetime")
            trip_dur = row.get("trip_duration")
            pickup_long = row.get("pickup_longitude")
            pickup_lat = row.get("pickup_latitude")
            dropoff_long = row.get("dropoff_longitude")
            dropoff_lat = row.get("dropoff_latitude")

            if not (pickup_time and dropoff_time):
                excl_writer.writerow([raw_id_str, "missing_datetime", f"pickup={pickup_time}, dropoff={dropoff_time}"])
                continue

            # validate numeric fields
            try:
                pickup_long = float(pickup_long)
                pickup_lat = float(pickup_lat)
                dropoff_long = float(dropoff_long)
                dropoff_lat = float(dropoff_lat)
            except Exception:
                excl_writer.writerow([raw_id_str, "invalid_coordinates",
                                      f"pickup_long={pickup_long}, pickup_lat={pickup_lat},"
                                      f"dropoff_long={dropoff_long}, dropoff_lat={dropoff_lat}"])
                continue

            # Validate the trip duration
            try:
                dur = int(trip_dur)
                if dur <= 0:
                    raise ValueError("non-positive trip duration value")
            except Exception:
                excl_writer.writerow([raw_id_str, "invalid_trip_duration", f"trip_duration={trip_dur}"])
                continue

            # Validate the trip distance
            dist_km = distance(pickup_lat, pickup_long, dropoff_lat, dropoff_long)
            if not dist_km:
                excl_writer.writerow([raw_id_str, "distance_calc_error",
                                      f"pickup_long={pickup_long}, pickup_lat={pickup_lat}",
                                      f"dropoff_long={dropoff_long}, dropoff_lat={dropoff_lat}"])
                continue

            # Validate the trip speed
            hours = dur / 3600.0
            if hours > 0:
                speed = dist_km / hours
            else:
                speed = 0

            if speed > MAX_REASONABLE_SPEED or speed == 0:
                excl_writer.writerow([raw_id_str, "unrealistic_speed", f"trip_speed={speed}"])
                continue

            # Validate the location (if outside NYC)
            if if_in_nyc(pickup_lat, pickup_long) and if_in_nyc(dropoff_lat, dropoff_long):
                outside_nyc = 0
            else:
                outside_nyc = 1
                excl_writer.writerow([raw_id_str, "outside_of_nyc",
                                      f"pickup_long={pickup_long}, pickup_lat={pickup_lat}",
                                      f"dropoff_long={dropoff_long}, dropoff_lat={dropoff_lat}"])

            # Other derived features added to the row
            if dist_km < ROUND_TRIP_THRESHOLD:
                is_round_trip = 1
            else:
                is_round_trip = 0

            # If all checks pass, we keep the row and also add derived columns
            row.update({"trip_distance_km": dist_km, "speed_kmph": speed, "is_round_trip": is_round_trip, "outside_nyc": outside_nyc})
            results.append((intval, raw_id_str, row))
    
    excl_file.close()
    return results



def store_sorted_to_db(sorted_list, db_path):
    """Stores the sorted entries into SQLite"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS trips")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            numeric_id INTEGER PRIMARY KEY,
            original_id TEXT,
            vendor_id TEXT,
            pickup_datetime TEXT,
            dropoff_datetime TEXT,
            passenger_count INTEGER,
            pickup_longitude REAL,
            pickup_latitude REAL,
            dropoff_longitude REAL,
            dropoff_latitude REAL,
            store_and_fwd_flag TEXT,
            trip_duration INTEGER,
            trip_distance_km REAL,
            speed_kmph REAL,
            is_round_trip INTEGER
        )
    """)
    conn.commit()
    insert_sql = """
        INSERT INTO trips (
            numeric_id, original_id, vendor_id, pickup_datetime, dropoff_datetime, passenger_count,
            pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, store_and_fwd_flag,
            trip_duration, trip_distance_km, speed_kmph, is_round_trip
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    count = 0
    for numeric_id, original_id, row in sorted_list:
        cursor.execute(
            insert_sql,
            (numeric_id,
            original_id,
            row.get("vendor_id"),
            row.get("pickup_datetime"),
            row.get("dropoff_datetime"),
            row.get("passenger_count"),
            row.get("pickup_longitude"),
            row.get("pickup_latitude"),
            row.get("dropoff_longitude"),
            row.get("dropoff_latitude"),
            row.get("store_and_fwd_flag"),
            row.get("trip_duration"),
            round(row.get("trip_distance_km"), 2),
            round(row.get("speed_kmph"), 2),
            row.get("is_round_trip"))
        )
        count += 1
        if count % 1000 == 0:
            conn.commit()
    conn.commit()
    conn.close()

def main(argv):
    if len(argv) != 4:
        print("Usage: python parse_and_store.py <input.csv> <output_db> <excluded.csv>")
        return
    input_csv = argv[1]
    db_path = argv[2]
    excluded_csv = argv[3]

    print("Loading and extracting numeric IDs...")
    extracted = load_and_extract(input_csv, excluded_csv)
    print(f"Extracted and validated {len(extracted)} rows")

    print("Sorting...")
    sorted_list = merge_sort(extracted)
    print("Sorting completed. Storing into database...")

    store_sorted_to_db(sorted_list, db_path)
    print (f"Stored {len(sorted_list)} rows into {db_path}")
            

if __name__ == "__main__":
    main(sys.argv)