"""Dataminimering.

Verktøyene returnerer aldri rå API-svar. Hvert felt som slippes ut må stå
på en hvitliste, og direkte identifikatorer maskeres. Kundeservice trenger
å vite hvor saken står, ikke alt systemet vet om skyldneren.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

# Felter som aldri slippes ut, uansett hvor de dukker opp i svaret.
ALWAYS_DROP = frozenset(
    {
        "ssn",
        "socialsecuritynumber",
        "personnummer",
        "fodselsnummer",
        "fødselsnummer",
        "nationalid",
        "personalidentitynumber",
        "bankaccount",
        "bankaccountnumber",
        "iban",
        "cardnumber",
        "password",
        "token",
    }
)

_NO_FNR = re.compile(r"\b\d{11}\b")
_SE_PNR = re.compile(r"\b(?:19|20)?\d{6}[-+]?\d{4}\b")


def mask_identifiers(text: str) -> str:
    """Maskerer person- og fødselsnummer i fritekst.

    Fritekstfelter som saksnotater kan inneholde identifikatorer selv om
    feltnavnet er uskyldig.
    """
    text = _NO_FNR.sub("[maskert]", text)
    text = _SE_PNR.sub("[maskert]", text)
    return text


def pick(
    source: Mapping[str, Any] | None,
    allowed: Iterable[str],
    *,
    mask_text: bool = True,
) -> dict[str, Any]:
    """Plukker ut hvitlistede felter fra et API-svar.

    Feltnavn sammenlignes uten hensyn til store bokstaver og understrek, slik
    at hvitlisten tåler at APIet bruker camelCase eller snake_case.
    """
    if not source:
        return {}

    wanted = {_normalise(name): name for name in allowed}
    result: dict[str, Any] = {}

    for raw_key, value in source.items():
        key = _normalise(raw_key)
        if key in ALWAYS_DROP:
            continue
        if key not in wanted:
            continue
        if isinstance(value, str) and mask_text:
            value = mask_identifiers(value)
        result[wanted[key]] = value

    return result


def _normalise(name: str) -> str:
    return name.replace("_", "").replace("-", "").lower()
