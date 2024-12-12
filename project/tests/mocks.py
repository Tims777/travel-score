BASE_URL = (
    "https://gist.github.com",
    "Tims777",
    "c213bbfd354ae27628651937062b2acb",
    "raw",
    "aa06fc3a4db7d31320f36fc3a848e4c913de7b9e",
)

MOCKED_ICP_CYCLE = "/".join((*BASE_URL, "P_ICP-2021-Cycle.zip"))
MOCKED_INFORM_RISK = "/".join((*BASE_URL, "InformRisk-Workflow482.zip"))
MOCKED_NATURAL_EARTH = "/".join((*BASE_URL, "ne_110m_admin_0_countries.zip"))
PRECOMPUTED_PBF_ANALYSIS = "/".join((*BASE_URL, "pbf_analysis.zip"))

MOCK_ASSETS = {
    "icp_metrics_url": MOCKED_ICP_CYCLE,
    "inform_scores_url": MOCKED_INFORM_RISK,
    "world_url": MOCKED_NATURAL_EARTH,
}
