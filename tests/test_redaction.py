from banqsoft_mcp.redaction import ALWAYS_DROP, mask_identifiers, pick


def test_pick_keeps_only_whitelisted_fields():
    raw = {"caseNumber": "1473", "status": "Open", "internalNote": "hemmelig"}
    assert pick(raw, ("caseNumber", "status")) == {
        "caseNumber": "1473",
        "status": "Open",
    }


def test_pick_matches_field_names_across_naming_styles():
    raw = {"case_number": "1473", "REMAINING-AMOUNT": 250}
    result = pick(raw, ("caseNumber", "remainingAmount"))
    assert result == {"caseNumber": "1473", "remainingAmount": 250}


def test_pick_drops_sensitive_fields_even_when_whitelisted():
    raw = {"caseNumber": "1473", "ssn": "01011012345"}
    result = pick(raw, ("caseNumber", "ssn"))
    assert "ssn" not in result
    assert result == {"caseNumber": "1473"}


def test_always_drop_covers_bank_and_identity_fields():
    for field in ("iban", "personnummer", "bankAccountNumber".lower()):
        assert field in ALWAYS_DROP


def test_mask_norwegian_birth_number_in_free_text():
    assert mask_identifiers("Skyldner 01011012345 ringte") == "Skyldner [maskert] ringte"


def test_mask_swedish_personal_number_in_free_text():
    assert "[maskert]" in mask_identifiers("Gäller 19850101-1234 enligt avtal")


def test_pick_masks_identifiers_inside_whitelisted_text():
    raw = {"lastEventText": "Snakket med 01011012345 om nedbetaling"}
    result = pick(raw, ("lastEventText",))
    assert "01011012345" not in result["lastEventText"]


def test_pick_handles_missing_source():
    assert pick(None, ("caseNumber",)) == {}
