DROP TABLE IF EXISTS ip_addresses;
DROP TABLE IF EXISTS threat_actors;

CREATE TABLE ip_addresses (
    ip TEXT PRIMARY KEY CHECK(ip GLOB '[0-9]*.[0-9]*.[0-9]*.[0-9]*'),
    country TEXT,
    city TEXT
);

CREATE TABLE threat_actors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    threat_actor_name TEXT,
    FOREIGN KEY (ip) REFERENCES ip_addresses (ip)
);