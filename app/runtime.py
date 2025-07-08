"""
Runtime helper functions for lead enrichment.
"""
import json
import importlib.resources
from typing import Dict, List, Any, Optional
from geopy.distance import geodesic


# Load JSON data once at import time
def _load_json_data(filename: str) -> Any:
    """Load JSON data from app/dist/ directory."""
    try:
        with importlib.resources.files('app.dist').joinpath(filename).open('r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {filename}: {e}")
        return {}


# Load all intelligence files
STATE_LANGUAGE_MAP = _load_json_data('state_language_map.json')
CAMPUS_COVERAGE = _load_json_data('campus_coverage.json.gz')
BRAND_REGISTRY = _load_json_data('brand_registry.json')
PITCH_TEMPLATES = _load_json_data('pitch_templates.json')
BOT_LANGUAGE_SUPPORT = _load_json_data('bot_language_support.json')


def choose_tts_languages(ideal_lang: str) -> List[str]:
    """
    Choose TTS languages based on bot support.
    Always ends with English as fallback.
    """
    languages = []
    
    # Check if ideal language is enabled
    if ideal_lang in BOT_LANGUAGE_SUPPORT:
        lang_config = BOT_LANGUAGE_SUPPORT[ideal_lang]
        if lang_config.get('enabled', 0) == 1:
            languages.append(ideal_lang)
        else:
            # Use fallback language
            fallback = lang_config.get('fallback_to', 'English')
            if fallback not in languages:
                languages.append(fallback)
    else:
        # Default to English if language not found
        languages.append('English')
    
    # Always add English at the end if not already present
    if 'English' not in languages:
        languages.append('English')
    
    return languages


def _find_nearby_campuses(city: str, state: str, max_distance: float = 30.0) -> List[Dict[str, Any]]:
    """
    Find campuses within max_distance km of the given city using real coordinates.
    """
    nearby_campuses = []
    
    # Get city coordinates (simplified - in real implementation, you'd have a city coordinates database)
    # For now, we'll use the first campus in the same state as a reference point
    city_coords = None
    for campus in CAMPUS_COVERAGE:
        if campus.get('city', '').lower() == city.lower():
            city_coords = (campus.get('latitude'), campus.get('longitude'))
            break
    
    # If we don't have exact city coordinates, use state-based filtering
    if not city_coords:
        for campus in CAMPUS_COVERAGE:
            if campus.get('state') == state:
                # Add all campuses in the same state as potential matches
                campus_copy = campus.copy()
                campus_copy['distance_km'] = 0  # Assume same state = within range
                nearby_campuses.append(campus_copy)
    else:
        # Calculate actual distances using coordinates
        for campus in CAMPUS_COVERAGE:
            if campus.get('state') == state:
                campus_coords = (campus.get('latitude'), campus.get('longitude'))
                if campus_coords[0] and campus_coords[1]:  # Check if coordinates exist
                    try:
                        distance = geodesic(city_coords, campus_coords).kilometers
                        if distance <= max_distance:
                            campus_copy = campus.copy()
                            campus_copy['distance_km'] = distance
                            nearby_campuses.append(campus_copy)
                    except Exception:
                        # Fallback: add campus if coordinates calculation fails
                        campus_copy = campus.copy()
                        campus_copy['distance_km'] = 0
                        nearby_campuses.append(campus_copy)
    
    # Sort by distance (closest first)
    nearby_campuses.sort(key=lambda x: x.get('distance_km', float('inf')))
    
    return nearby_campuses


def _get_highest_brand_campus(campuses: List[Dict[str, Any]]) -> Optional[str]:
    """
    Get the brand with highest priority from nearby campuses.
    For now, return the first brand found.
    """
    if campuses:
        return campuses[0].get('brand')
    return None


def _get_college_info(college_code: str) -> Optional[Dict[str, Any]]:
    """
    Get college information from the brand registry.
    """
    colleges = BRAND_REGISTRY.get('colleges', {})
    return colleges.get(college_code)


def _get_brand_category_info(category: str) -> Optional[Dict[str, Any]]:
    """
    Get brand category information from the brand registry.
    """
    categories = BRAND_REGISTRY.get('brand_categories', {})
    return categories.get(category)


def _build_caller_logic(caller_logic_template: str, college_info: Dict[str, Any], city: str) -> str:
    """
    Build the caller logic string based on the template and college information.
    """
    logic = caller_logic_template
    
    # Replace placeholders
    logic = logic.replace('{{college_name}}', college_info.get('name', ''))
    logic = logic.replace('{{college_short}}', college_info.get('short', ''))
    logic = logic.replace('{{city}}', city)
    
    return logic


def build_pitch(lead: Dict[str, str]) -> Dict[str, str]:
    """
    Build pitch text and caller name based on lead data.
    Priority: college > city > nurture fallback
    """
    college = lead.get('college', '').strip()
    city = lead.get('city', '').strip()
    state = lead.get('state', '').strip()
    course = lead.get('course', '').strip()
    
    # Case A: College is present
    if college:
        college_info = _get_college_info(college)
        if college_info:
            category = college_info.get('category', 'medium')
            category_info = _get_brand_category_info(category)
            
            if category_info:
                caller_name = college_info.get('caller_name', 'Sunstone Advisor')
                template = category_info.get('template', 'Hi, I\'m calling about {course}.')
                
                # Build pitch text based on category
                if category == 'high':
                    # Use college name
                    pitch_text = template.format(college_name=college_info.get('name', college), course=course)
                elif category == 'medium':
                    # Use city + college short
                    pitch_text = template.format(city=city, college_short=college_info.get('short', college), course=course)
                else:  # low
                    # Use city + Sunstone
                    pitch_text = template.format(city=city, course=course)
            else:
                # Fallback for unknown category
                caller_name = college_info.get('caller_name', 'Sunstone Advisor')
                pitch_text = f"Hi, I'm calling from {college_info.get('name', college)} about {course} programs."
        else:
            # Fallback for unknown college
            caller_name = 'Sunstone Advisor'
            pitch_text = f"Hi, I'm calling from {college} about {course} programs."
    
    # Case B: City is present (but no college)
    elif city:
        nearby_campuses = _find_nearby_campuses(city, state)
        brand = _get_highest_brand_campus(nearby_campuses)
        
        if brand:
            college_info = _get_college_info(brand)
            if college_info:
                category = college_info.get('category', 'medium')
                category_info = _get_brand_category_info(category)
                
                if category_info:
                    caller_name = college_info.get('caller_name', 'Sunstone Advisor')
                    template = category_info.get('template', 'Hi, I\'m calling about {course}.')
                    
                    # Build pitch text based on category
                    if category == 'high':
                        pitch_text = template.format(college_name=college_info.get('name', brand), course=course)
                    elif category == 'medium':
                        pitch_text = template.format(city=city, college_short=college_info.get('short', brand), course=course)
                    else:  # low
                        pitch_text = template.format(city=city, course=course)
                else:
                    caller_name = college_info.get('caller_name', 'Sunstone Advisor')
                    pitch_text = f"Hi, I'm calling from {college_info.get('name', brand)} about {course} programs."
            else:
                # Fallback for unknown brand
                caller_name = 'Sunstone Advisor'
                pitch_text = f"Hi, I'm calling about educational opportunities in {city} for {course}."
        else:
            # Fallback for city with no nearby campuses
            caller_name = 'Sunstone Advisor'
            pitch_text = f"Hi, I'm calling about educational opportunities in {city} for {course}."
    
    # Case C: Nurture fallback (no college, no city)
    else:
        nurture_info = _get_college_info('nurture')
        if nurture_info:
            category = nurture_info.get('category', 'low')
            category_info = _get_brand_category_info(category)
            
            if category_info:
                caller_name = nurture_info.get('caller_name', 'Sunstone Advisor')
                location = city if city else state
                # For nurture fallback, we need to handle the case where city might be empty
                if category == 'low' and not city:
                    # Use state instead of city for low category when no city
                    pitch_text = f"Hi, I'm calling from Sunstone in {state}. I noticed you're interested in {course}. Would you like to know more about our programs?"
                else:
                    template = category_info.get('template', 'Hi, I\'m calling from Sunstone in {location}. I noticed you\'re interested in {course}. Would you like to know more about our programs?')
                    pitch_text = template.format(location=location, course=course)
            else:
                caller_name = nurture_info.get('caller_name', 'Sunstone Advisor')
                location = city if city else state
                pitch_text = f"Hi, I'm calling from Sunstone about educational opportunities in {location}. Are you interested in pursuing {course}?"
        else:
            # Ultimate fallback
            caller_name = 'Sunstone Advisor'
            location = city if city else state
            pitch_text = f"Hi, I'm calling from Sunstone about educational opportunities in {location}. Are you interested in pursuing {course}?"
    
    return {
        'caller_name': caller_name,
        'pitch_text': pitch_text
    }


def enrich_lead(lead: Dict[str, str]) -> Dict[str, Any]:
    """
    Enrich lead data with caller name, pitch text, and TTS languages.
    """
    # Validate required field
    if not lead.get('state'):
        raise ValueError("State is required")
    
    # Get language from lead or derive from state
    language = lead.get('language', '')
    if not language and lead.get('state') in STATE_LANGUAGE_MAP:
        # Get the first (primary) language from the array
        state_languages = STATE_LANGUAGE_MAP[lead['state']]
        language = state_languages[0] if state_languages else 'English'
    
    # Build pitch
    pitch_data = build_pitch(lead)
    
    # Choose TTS languages
    tts_languages = choose_tts_languages(language)
    
    # Return enriched lead
    enriched_lead = lead.copy()
    enriched_lead.update(pitch_data)
    enriched_lead['tts_languages'] = tts_languages
    
    return enriched_lead
