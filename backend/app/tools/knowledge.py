import json
import os
from groq import Groq

# Astrology knowledge base — curated reference notes
KNOWLEDGE_BASE = [
    {
        "topic": "Sun Signs",
        "content": """The Sun represents ego, identity, and life purpose. 
        Aries: bold, pioneering, impulsive. Taurus: stable, sensual, stubborn. 
        Gemini: curious, communicative, dual. Cancer: nurturing, emotional, protective.
        Leo: creative, dramatic, generous. Virgo: analytical, practical, perfectionist.
        Libra: harmonious, diplomatic, indecisive. Scorpio: intense, transformative, secretive.
        Sagittarius: adventurous, philosophical, blunt. Capricorn: ambitious, disciplined, cold.
        Aquarius: innovative, humanitarian, detached. Pisces: intuitive, compassionate, dreamy."""
    },
    {
        "topic": "Moon Signs",
        "content": """The Moon governs emotions, instincts, and subconscious patterns.
        Moon in fire signs (Aries, Leo, Sagittarius): emotional expression is bold and dramatic.
        Moon in earth signs (Taurus, Virgo, Capricorn): emotions are stable and grounded.
        Moon in air signs (Gemini, Libra, Aquarius): emotions are processed intellectually.
        Moon in water signs (Cancer, Scorpio, Pisces): emotions are deep and intuitive."""
    },
    {
        "topic": "Rising Signs / Ascendant",
        "content": """The Ascendant is the mask we wear, how others first perceive us.
        It changes every 2 hours, making birth time crucial for accuracy.
        Aries rising: appears bold and direct. Taurus rising: appears calm and reliable.
        Gemini rising: appears curious and talkative. Cancer rising: appears nurturing.
        Leo rising: appears confident and charismatic. Virgo rising: appears analytical.
        Libra rising: appears charming and balanced. Scorpio rising: appears intense.
        Sagittarius rising: appears optimistic. Capricorn rising: appears serious.
        Aquarius rising: appears unique. Pisces rising: appears dreamy and ethereal."""
    },
    {
        "topic": "Planetary Aspects",
        "content": """Aspects describe relationships between planets.
        Conjunction (0°): planets merge energy — powerful, intense.
        Sextile (60°): harmonious opportunity, easy flow of energy.
        Square (90°): tension and challenge, motivates action and growth.
        Trine (120°): natural talent, flowing energy, gifts that come easily.
        Opposition (180°): polarity, need for balance between two forces."""
    },
    {
        "topic": "Houses",
        "content": """The 12 houses represent life areas.
        1st: self, appearance, beginnings. 2nd: money, possessions, values.
        3rd: communication, siblings, short trips. 4th: home, family, roots.
        5th: creativity, romance, children, play. 6th: health, daily work, service.
        7th: partnerships, marriage, open enemies. 8th: transformation, death, shared resources.
        9th: philosophy, higher education, travel. 10th: career, public image, authority.
        11th: friends, groups, hopes and dreams. 12th: spirituality, hidden enemies, isolation."""
    },
    {
        "topic": "Mercury Retrograde",
        "content": """Mercury retrograde occurs 3-4 times per year for about 3 weeks.
        During this period: communication may be unclear, technology may malfunction,
        travel plans may be disrupted, and past issues may resurface.
        Best practices: review rather than start new projects, back up data,
        double-check communications, reconnect with old friends."""
    },
    {
        "topic": "Saturn Return",
        "content": """Saturn returns to its natal position approximately every 29.5 years.
        First return (ages 27-30): major life restructuring, responsibility, maturity.
        Second return (ages 57-60): wisdom, legacy, life review.
        Saturn return often brings challenges that ultimately lead to growth and authenticity."""
    },
    {
        "topic": "Career and 10th House",
        "content": """The 10th house and Midheaven indicate career and public life.
        Planets in the 10th house strongly influence career path.
        Sun in 10th: leadership roles, public recognition.
        Saturn in 10th: slow but steady career growth, authority.
        Jupiter in 10th: expansion, luck in career, teaching.
        Mars in 10th: competitive, entrepreneurial, military or sports."""
    },
    {
        "topic": "Relationships and 7th House",
        "content": """The 7th house governs partnerships and marriage.
        The sign on the 7th house cusp (Descendant) describes ideal partners.
        Venus placement shows how we love and what we attract.
        Mars placement shows what we desire and pursue.
        Synastry compares two charts to assess compatibility."""
    },
    {
        "topic": "Safety and Ethics",
        "content": """Astrology is a tool for self-reflection and guidance only.
        It should never be used to make medical, legal, or financial decisions.
        Free will always supersedes astrological influences.
        Readings are meant to empower, not create fear or dependency.
        Always encourage users to consult qualified professionals for serious life decisions."""
    }
]

def knowledge_lookup(query: str) -> dict:
    """
    RAG tool — searches curated astrology knowledge base
    and returns relevant context grounded in real reference material.
    """
    try:
        if not query or len(query.strip()) < 3:
            return {
                "success": False,
                "error": "Query too short"
            }

        query_lower = query.lower()

        # Simple keyword matching — find relevant knowledge
        relevant = []
        keywords_map = {
            "sun": ["Sun Signs", "Career and 10th House"],
            "moon": ["Moon Signs"],
            "rising": ["Rising Signs / Ascendant"],
            "ascendant": ["Rising Signs / Ascendant"],
            "aspect": ["Planetary Aspects"],
            "house": ["Houses", "Career and 10th House", "Relationships and 7th House"],
            "career": ["Career and 10th House", "Houses"],
            "relationship": ["Relationships and 7th House"],
            "love": ["Relationships and 7th House"],
            "mercury": ["Mercury Retrograde"],
            "retrograde": ["Mercury Retrograde"],
            "saturn": ["Saturn Return"],
            "return": ["Saturn Return"],
            "safe": ["Safety and Ethics"],
            "medical": ["Safety and Ethics"],
            "financial": ["Safety and Ethics"],
            "legal": ["Safety and Ethics"],
        }

        matched_topics = set()
        for keyword, topics in keywords_map.items():
            if keyword in query_lower:
                matched_topics.update(topics)

        # Get matching knowledge entries
        for entry in KNOWLEDGE_BASE:
            if entry["topic"] in matched_topics:
                relevant.append(entry)

        # If no keyword match, return general overview
        if not relevant:
            relevant = KNOWLEDGE_BASE[:3]

        context = "\n\n".join([
            f"**{e['topic']}**\n{e['content']}"
            for e in relevant
        ])

        return {
            "success": True,
            "query": query,
            "context": context,
            "topics_found": [e["topic"] for e in relevant],
            "source": "Aradhana curated astrology knowledge base"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }