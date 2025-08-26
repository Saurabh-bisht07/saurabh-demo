import math

EARTH_RADIUS_KM = 6371.0

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
	lat1_rad = math.radians(lat1)
	lon1_rad = math.radians(lon1)
	lat2_rad = math.radians(lat2)
	lon2_rad = math.radians(lon2)
	dlat = lat2_rad - lat1_rad
	dlon = lon2_rad - lon1_rad
	a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
	return EARTH_RADIUS_KM * c

# Simple ABO/Rh compatibility for blood donation
_ABO_COMPAT = {
	"O": {"O", "A", "B", "AB"},
	"A": {"A", "AB"},
	"B": {"B", "AB"},
	"AB": {"AB"},
}

def is_abo_compatible(donor_bg: str, recipient_bg: str) -> bool:
	return recipient_bg in _ABO_COMPAT.get(donor_bg, set())

def is_rh_compatible(donor_rh: str, recipient_rh: str) -> bool:
	# Rh- can donate to - and +; Rh+ can donate only to +
	if donor_rh == "-":
		return True
	return recipient_rh == "+"

def is_blood_compatible(donor_bg: str, donor_rh: str, recipient_bg: str, recipient_rh: str) -> bool:
	return is_abo_compatible(donor_bg, recipient_bg) and is_rh_compatible(donor_rh, recipient_rh)