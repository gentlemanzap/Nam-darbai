import csv

def celsius_converter(f_temp):
    """Convert Fahrenheit to Celsius and round to 2 decimal places."""
    fahrenheit = float(f_temp)
    celsius = (fahrenheit - 32) * 5 / 9
    return round(celsius, 2)




def parse_and_clean(line):
    """Validate a weather log record and return its fields, or None if corrupted."""

    # Split the line into fields
    fields = line.strip().split("|")

    # Check that there are exactly five fields
    if len(fields) != 5:
        return None

    # Remove spaces around each field
    fields = [field.strip() for field in fields]

    timestamp, station_id, temperature, humidity, status = fields

    # Reject missing values
    if not all(fields):
        return None

    # Reject non-numeric temperature or humidity
    try:
        float(temperature)
        float(humidity)
    except ValueError:
        return None

    # Reject sensors that are not active
    if status != "ACTIVE":
        return None

    return fields



def main():
    corrupted_count = 0
    cleaned_count = 0

    with open("environmental_raw.txt", "r", encoding="utf-8") as infile, \
         open("environmental_clean.csv", "w", newline="", encoding="utf-8") as outfile:

        writer = csv.writer(outfile)
        writer.writerow([
            "Timestamp",
            "StationID",
            "Temp(C)",
            "Humidity(%)",
            "Sensor_Status"
        ])

        for line in infile:
            # Skip the header row
            if line.strip().startswith("Timestamp"):
                continue

            cleaned_row = parse_and_clean(line)

            if cleaned_row is None:
                corrupted_count += 1
                continue

            # Convert Fahrenheit to Celsius
            cleaned_row[2] = celsius_converter(cleaned_row[2])

            writer.writerow(cleaned_row)
            cleaned_count += 1

    print("Weather log cleaning complete!")
    print(f"Valid rows written: {cleaned_count}")
    print(f"Corrupted rows skipped: {corrupted_count}")
    print("Output file: environmental_clean.csv")


if __name__ == "__main__":
    main()
