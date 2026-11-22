def _clamp(x):
    return max(0.0, min(100.0, float(x)))

def lotus_score(water, surface, dirt):
    score = 0.4 * _clamp(water) + 0.4 * _clamp(surface) + 0.2 * (100 - _clamp(dirt))
    label = "Conceptual surface suitability"
    return score, label

def gecko_index(contact, surface_compatibility, condition):
    return 0.45 * _clamp(contact) + 0.35 * _clamp(surface_compatibility) + 0.20 * _clamp(condition)

def drag_index(shape, speed):
    speed = _clamp(speed)
    base = {"Blunt": 80, "Rounded": 55, "Streamlined": 30}.get(shape, 60)
    return round(base * (0.5 + speed / 100.0), 1)
