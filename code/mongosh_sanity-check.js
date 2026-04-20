// mongosh_sanity-check.js
// MongoDB Sanity Checks
// Author: Stefan Regalia
//
//  Verifying that the temperature_anomalies collection was loaded correctly
//
// To run:
// source .env && mongosh "$MONGO_DB_URI" --file code/mongosh_sanity-check.js

// Total document count (expected 23,267)
print("\n=== Total Document Count ===")
printjson(db.temperature_anomalies.countDocuments())

// Document count per country (expected 10 countries)
print("\n=== Document Count Per Country ===")
printjson(db.temperature_anomalies.aggregate([
    {$group: {_id: "$country", count: {$sum: 1}}},
    {$sort: {_id: 1}}
]).toArray())

// Year range (expected 1750 to 2020)
print("\n=== Year Range ===")
printjson(db.temperature_anomalies.aggregate([
    {$group: {
        _id: null,
        min_year: {$min: "$year"},
        max_year: {$max: "$year"}
    }}
]).toArray())

// Verifying sample document structure looks good
print("\n=== Sample Document ===")
printjson(db.temperature_anomalies.findOne({country: "united-states"}))

// Index verification (expect unique index on (country, year, month))
print("\n=== Indexes ===")
printjson(db.temperature_anomalies.getIndexes())

// Null check (verify nulls exist in smoothed columns for early records)
print("\n=== Null Count in annual_anomaly_c ===")
printjson(db.temperature_anomalies.countDocuments({annual_anomaly_c: null}))

// Verifying baseline field is consistent across all documents
print("\n=== Distinct Baseline Values ===")
printjson(db.temperature_anomalies.distinct("baseline"))

// Verifying source field is consistent across all documents
print("\n=== Distinct Source Values ===")
printjson(db.temperature_anomalies.distinct("source"))