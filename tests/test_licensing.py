from pathlib import Path
from datetime import datetime, timedelta
import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from winforge.licensing.models import ValidationState, LicenseType
from winforge.licensing.fingerprint import FingerprintProvider, FingerprintMatcher, FingerprintRecord
from winforge.licensing.verifier import LicenseVerifier
from winforge.licensing.policy import LicensePolicyManager
from tools.license_creator import sign_license_payload
from tools.key_generator import generate_rsa_keypair


def setup_test_keypair(tmp_path: Path):
    """Generates temporary RSA-2048 keypair for unit testing."""
    priv_path, pub_path = generate_rsa_keypair(tmp_path)
    with open(priv_path, "rb") as f:
        priv_pem = f.read()
    with open(pub_path, "rb") as f:
        pub_pem = f.read()
    return priv_pem, pub_pem


def test_fingerprint_collection_and_profiles():
    provider = FingerprintProvider()

    # Profile A: Baseline Machine
    prof_a_raw = {
        "MOTHERBOARD_UUID": "MB_UUID_1001",
        "CPU_PROCESSOR_ID": "CPU_ID_2002",
        "PRIMARY_DISK_SERIAL": "DISK_SER_3003",
        "PRIMARY_NIC_MAC": "00:11:22:33:44:55"
    }
    rec_a = provider.collect_fingerprint(salt="TEST_SALT", mock_signals=prof_a_raw)
    comp_hash_a = rec_a.composite_hash()
    assert comp_hash_a != ""

    matcher = FingerprintMatcher()

    # Profile A: Same Machine -> Match score 100%
    res_a = matcher.compare(rec_a, comp_hash_a, target_record=rec_a)
    assert res_a["match_score"] == 100.0
    assert res_a["activation_decision"] is True

    # Profile B: SSD Changed -> Match score 85%
    prof_b_raw = dict(prof_a_raw, PRIMARY_DISK_SERIAL="DISK_SER_NEW_SWAP")
    rec_b = provider.collect_fingerprint(salt="TEST_SALT", mock_signals=prof_b_raw)
    res_b = matcher.compare(rec_b, comp_hash_a, target_record=rec_a)
    assert res_b["match_score"] == 85.0
    assert res_b["activation_decision"] is True

    # Profile C: NIC Changed -> Match score 85%
    prof_c_raw = dict(prof_a_raw, PRIMARY_NIC_MAC="99:88:77:66:55:44")
    rec_c = provider.collect_fingerprint(salt="TEST_SALT", mock_signals=prof_c_raw)
    res_c = matcher.compare(rec_c, comp_hash_a, target_record=rec_a)
    assert res_c["match_score"] == 85.0
    assert res_c["activation_decision"] is True

    # Profile D: Motherboard Changed -> Match score 60% (< 75% threshold)
    prof_d_raw = dict(prof_a_raw, MOTHERBOARD_UUID="MB_UUID_REPLACED_999")
    rec_d = provider.collect_fingerprint(salt="TEST_SALT", mock_signals=prof_d_raw)
    res_d = matcher.compare(rec_d, comp_hash_a, target_record=rec_a)
    assert res_d["match_score"] == 60.0
    assert res_d["activation_decision"] is False


def test_rsa_pss_signature_verification_and_tampering(tmp_path: Path):
    priv_pem, pub_pem = setup_test_keypair(tmp_path)
    verifier = LicenseVerifier(public_key_pem=pub_pem)
    provider = FingerprintProvider()

    rec_a = provider.collect_fingerprint(salt="WINFORGE_SALT")
    fp_hash = rec_a.composite_hash()

    # Generate valid license payload
    payload = sign_license_payload(
        private_key_pem=priv_pem,
        license_id="LIC-TEST-001",
        customer_id="CUST-TEST",
        license_type="TECHNICIAN",
        target_fingerprint_hash=fp_hash,
        valid_days=30,
        unlimited=True
    )

    # 1. Test Valid Signature
    val_res = verifier.verify_license_payload(payload, current_record=rec_a)
    assert val_res.state == ValidationState.VALID
    assert val_res.capabilities.tier == LicenseType.TECHNICIAN
    assert val_res.capabilities.technician_mode_allowed is True

    # 2. Test Tampered Signature Rejection
    tampered = dict(payload, customer_id="TAMPERED_HACKER_ID")
    val_tampered = verifier.verify_license_payload(tampered, current_record=rec_a)
    assert val_tampered.state == ValidationState.INVALID_SIGNATURE
    assert val_tampered.capabilities.tier == LicenseType.FREE_EDITION


def test_expired_license_rejection(tmp_path: Path):
    priv_pem, pub_pem = setup_test_keypair(tmp_path)
    verifier = LicenseVerifier(public_key_pem=pub_pem)
    provider = FingerprintProvider()

    rec_a = provider.collect_fingerprint(salt="WINFORGE_SALT")
    fp_hash = rec_a.composite_hash()

    payload = sign_license_payload(
        private_key_pem=priv_pem,
        license_id="LIC-TEST-EXPIRED",
        customer_id="CUST-EXPIRED",
        license_type="PERSONAL",
        target_fingerprint_hash=fp_hash,
        valid_days=-1,  # Expired yesterday
        unlimited=False
    )

    val_res = verifier.verify_license_payload(payload, current_record=rec_a)
    assert val_res.state == ValidationState.EXPIRED
    assert val_res.capabilities.tier == LicenseType.FREE_EDITION


def test_missing_license_fallback(tmp_path: Path):
    policy_mgr = LicensePolicyManager()
    missing_path = tmp_path / "non_existent_license.json"
    res = policy_mgr.get_active_license(license_file_path=missing_path)

    assert res.state == ValidationState.VALID
    assert res.capabilities.tier == LicenseType.FREE_EDITION
    assert res.capabilities.technician_mode_allowed is False
