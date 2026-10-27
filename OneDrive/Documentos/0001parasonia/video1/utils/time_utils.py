# -*- coding: utf-8 -*-
"""
Utilitários de tempo e formatação para sincronização audiovisual.
"""

def seconds_to_timecode(seconds: float) -> str:
    """Converte segundos para formato HH:MM:SS.mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

def timecode_to_seconds(timecode: str) -> float:
    """Converte formato HH:MM:SS.mmm para segundos float"""
    parts = timecode.strip().split(":")
    if len(parts) == 3:
        h, m, s = parts
        return float(h) * 3600 + float(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return float(m) * 60 + float(s)
    return float(parts[0])
