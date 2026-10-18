import re
import structlog
from typing import Dict, List, Optional

logger = structlog.get_logger()

class EducationParser:
    """
    Education qualification and degree tier parser.
    Identifies degree levels (Bachelor, Master, PhD, Associate) and tier institutions.
    """
    
    TIER_1_UNIVERSITIES = [
        "mit", "stanford", "harvard", "berkeley", "oxford", "cambridge", 
        "cmu", "carnegie mellon", "caltech", "princeton", "yale", "columbia"
    ]
    
    @classmethod
    def parse_education(cls, text: str) -> Dict[str, any]:
        if not text:
            return {
                "degree_level": "Unknown",
                "is_tier_one": False,
                "score": 50.0
            }
            
        lower_text = text.lower()
        
        degree_level = "Bachelor"
        if any(term in lower_text for term in ["ph.d", "phd", "doctorate"]):
            degree_level = "PhD"
            score = 100.0
        elif any(term in lower_text for term in ["master", "m.s.", "msc", "mba", "m.tech"]):
            degree_level = "Master"
            score = 85.0
        elif any(term in lower_text for term in ["bachelor", "b.s.", "bsc", "b.tech", "b.e.", "degree"]):
            degree_level = "Bachelor"
            score = 70.0
        elif any(term in lower_text for term in ["associate", "diploma"]):
            degree_level = "Associate"
            score = 55.0
        else:
            score = 60.0
            
        is_tier_one = any(uni in lower_text for uni in cls.TIER_1_UNIVERSITIES)
        if is_tier_one:
            score = min(100.0, score + 15.0)
            
        logger.info("education_parsed", degree_level=degree_level, is_tier_one=is_tier_one, score=score)
        return {
            "degree_level": degree_level,
            "is_tier_one": is_tier_one,
            "score": round(score, 2)
        }
