"""Test the integrity of the Intake (sub)catalog containing the PUDL SQLite DB.

Note that the SQLite catalogs are NOT ready for prime-time, and we have a lot of issues
to iron out. The nominal tests here are just some examples of tables that work or are
having trouble of some kind.

See https://github.com/catalyst-cooperative/pudl-catalog/issues/76

"""
import intake
import pytest

PUDL_CAT = intake.cat.pudl_cat


@pytest.mark.parametrize(
    "sqlite_cat,table",
    [
        pytest.param("pudl", "plants_steam_ferc1"),
        pytest.param("pudl", "fuel_ferc1"),
        pytest.param("pudl", "plant_in_service_ferc1"),
        pytest.param("pudl", "generators_eia860", marks=pytest.mark.xfail),
        pytest.param("pudl", "plants_eia860", marks=pytest.mark.xfail),
        pytest.param("pudl", "fuel_receipts_costs_eia923"),
        pytest.param("pudl", "plants_entity_eia"),
        pytest.param("pudl", "prime_movers_eia", marks=pytest.mark.xfail),
        pytest.param("pudl", "energy_sources_eia", marks=pytest.mark.xfail),
        pytest.param("ferc1", "f1_steam", marks=pytest.mark.xfail),
        pytest.param("ferc1", "f1_fuel", marks=pytest.mark.xfail),
        pytest.param("ferc1", "f1_plant_in_srvce", marks=pytest.mark.xfail),
    ],
)
def test_sqlite_catalogs(sqlite_cat: str, table: str):
    """Check that expected tables appear within the SQLite catalogs."""
    df = PUDL_CAT[sqlite_cat][table].read()
    assert not df.empty
    assert df.shape[0] > 1
    assert df.shape[1] > 1
