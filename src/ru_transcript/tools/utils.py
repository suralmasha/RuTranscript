from .sounds import allophones

def is_strong_position(next_phon: str) -> bool:
    next_allophone = allophones.get(next_phon, {})

    return (
        next_allophone.get('phon') == 'V'
        or next_allophone.get('voice') == 'voiced'
        or next_allophone.get('class') == 'sonorous'
    )


def get_next_non_symbol(section: list[str], start_idx: int) -> str | None:
    for phon in section[start_idx + 1 :]:
        if allophones.get(phon, {}).get('phon') != 'symb':
            return phon

    return None


def get_voiced_pair(phon: str) -> str | None:
    phon_info = allophones.get(phon, {})

    direct_pair = phon_info.get('pair')
    if direct_pair and allophones.get(direct_pair, {}).get('voice') == 'voiced':
        return direct_pair

    for candidate, candidate_info in allophones.items():
        if candidate_info.get('pair') == phon and candidate_info.get('voice') == 'voiced':
            return candidate

    return None
