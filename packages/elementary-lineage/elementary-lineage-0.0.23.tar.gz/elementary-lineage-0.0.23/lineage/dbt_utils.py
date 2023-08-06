from typing import Dict, Any
import dbt.config
from dbt.context.base import generate_base_context
from dbt.exceptions import DbtConfigError
from dbt.adapters.bigquery.connections import BigQueryConnectionManager
import google.cloud.bigquery
import google.cloud.exceptions
from google.api_core import client_info
from lineage.exceptions import ConfigError
from lineage.utils import get_logger

logger = get_logger(__name__)


def extract_profile_data(profiles_raw: Dict[str, Any], profile_name: str, target_name: str) -> Dict[str, Any]:
    profile_data = dict()
    try:
        selected_profile = profiles_raw[profile_name]
        profile_data = selected_profile['outputs'][target_name]
    except KeyError as exc:
        logger.debug(f"Failed extracting profile data: {profiles_raw}, {profile_name}, {target_name}, {exc}")

    return profile_data


def extract_credentials_and_data_from_profiles(profiles_dir: str, profile_name: str):
    try:
        profiles_raw = dbt.config.profile.read_profile(profiles_dir)
        empty_profile_renderer = dbt.config.renderer.ProfileRenderer(generate_base_context({}))
        dbt_profile = dbt.config.Profile.from_raw_profiles(profiles_raw, profile_name, empty_profile_renderer)
        profile_data = extract_profile_data(profiles_raw, profile_name, dbt_profile.target_name)
        return dbt_profile.credentials, profile_data
    except DbtConfigError as exc:
        logger.debug(f"Failed parsing selected profile - {profiles_dir}, {profile_name}, {exc}")
        raise ConfigError(f"Failed parsing selected profile - {profiles_dir}, {profile_name}")


def get_bigquery_client(profile_credentials):
    if profile_credentials.impersonate_service_account:
        creds = \
            BigQueryConnectionManager.get_impersonated_bigquery_credentials(profile_credentials)
    else:
        creds = BigQueryConnectionManager.get_bigquery_credentials(profile_credentials)

    database = profile_credentials.database
    location = getattr(profile_credentials, 'location', None)

    info = client_info.ClientInfo(user_agent=f'elementary')
    return google.cloud.bigquery.Client(
        database,
        creds,
        location=location,
        client_info=info,
    )
