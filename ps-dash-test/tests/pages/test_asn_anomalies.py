import sys
sys.path.append("/Users/yanaholoborodko/Desktop/aaas_testing_2.0/ps-dash") 
import os
os.environ["TEST_MODE"] = "True"
from src.pages.asn_anomalies import update_store, update_graphs, generate_plotly_heatmap_with_anomalies
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from dash import html, dcc
from src.model.queries import query_ASN_anomalies


@pytest.mark.parametrize("pathname, expected_output", [
    # Case 1: Normal case with two parameters
    ("ps-dash.uc.ssl-hep.org/anomalous_paths/src_netsite=VANDERBILT&dest_netsite=NCP-LCG2",
     {"src_netsite": "VANDERBILT", "dest_netsite": "NCP-LCG2"}),

    # Case 2: Single parameter, no graph on ps-dash
    ("ps-dash.uc.ssl-hep.org/anomalous_paths/src_netsite=VANDERBILT",
     {"src_netsite": "VANDERBILT"}),

    # Case 3: Multiple parameters, same result as in case 1
    ("ps-dash.uc.ssl-hep.org/anomalous_paths/src_netsite=VANDERBILT&dest_netsite=NCP-LCG2&test_param=123",
     {"src_netsite": "VANDERBILT", "dest_netsite": "NCP-LCG2", "test_param": "123"}),

    # Case 4: Path with no parameters, 404 page not found
    ("ps-dash.uc.ssl-hep.org/anomalous_paths/", {}),

    # Case 5: Trailing slash after parameters, same result as in case 1
    ("ps-dash.uc.ssl-hep.org/anomalous_paths/src_netsite=VANDERBILT&dest_netsite=NCP-LCG2/",
     {"src_netsite": "VANDERBILT", "dest_netsite": "NCP-LCG2"}),

])
def test_update_store(pathname, expected_output):
    assert update_store(pathname) == expected_output

import pandas as pd
mock_data_empty = pd.DataFrame()
mock_data_no_asn_list = pd.DataFrame({
    'src_netsite': ['PRAGUELCG2-LHCONE'] * 3,
    'dest_netsite': ['IEPSAS-KOSICE'] * 3,
    'ipv6': [False, False, False],
    'paths': [
        [{'last_appearance_path': '2025-02-13T19:05:34.826Z'}],
        [{'last_appearance_path': '2025-02-13T19:06:03.464Z'}],
        [{'last_appearance_path': '2025-02-17T14:35:36.146Z'}]
    ],
    'last_appearance_path': [
        '2025-02-13T19:05:34.826Z',
        '2025-02-13T19:06:03.464Z',
        '2025-02-17T14:35:36.146Z'
    ],
    'repaired_asn_path': [
        [2852, 2852, 2852, 2852, 2607, 2607, 2607],
        [2852, 2852, 2852, 2852, 2607, 2607],
        [2852, 2852, 2852, 20965, 20965, 20965, 20965, 20965, 20965, 20965]
    ],
    'path_len': [7, 6, 10]
})

@pytest.mark.parametrize("mock_data, expected_output", [
    #Case 1: empty data
    pytest.param(
        mock_data_empty,
        html.Div([
            html.H1("No data found for alarm PRAGUELCG2-LHCONE to IEPSAS-KOSICE"),
            html.P("No data was found for the alarm selected. Please try another alarm.", style={"font-size": "1.2rem"})
        ], className="l-h-3 p-2 boxwithshadow page-cont ml-1 p-1"),
        id="empty_data"
    ),
    # Case 2: asn list is absent
    pytest.param(
        mock_data_no_asn_list,
        html.Div([
        dcc.Graph(id='asn-sankey-ipv4', figure=KeyError("['asn_list'] not in index"))
        ]),  
        id="missing_asn_list"
    ),
    # TO-DO: Case 3. test cases when columns data types are different
])
@patch('src.pages.asn_anomalies.query_ASN_anomalies')
def test_update_graphs_incomplete_data(mock_query_ASN_anomalies, mock_data, expected_output):
    # mock the query_ASN_anomalies function to return an empty DataFrame
    mock_query_ASN_anomalies.return_value = mock_data

    query_params = {
        'src_netsite': 'PRAGUELCG2-LHCONE',
        'dest_netsite': 'IEPSAS-KOSICE'
    }

    # Call the function
    result = update_graphs(query_params)

    assert isinstance(result, html.Div)

    if mock_data.empty:
        # If the DataFrame is empty, assert that the function returns a no-data message
        assert result.children[0].children == expected_output.children[0].children
        assert result.children[1].children == expected_output.children[1].children
    else:
        assert str(result) == str(expected_output)