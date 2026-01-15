def fetch_crm_data(client_name):
    mock_crm = {
        "Acme Corp": {
            "industry": "Manufacturing",
            "budget": "$120,000",
            "past_deals": ["ERP Upgrade", "Supply Chain Optimization"]
        },
        "Northstar Retail": {
            "industry": "Retail",
            "budget": "$75,000",
            "past_deals": ["AI Demand Forecasting"]
        }
    }

    return mock_crm.get(
        client_name,
        {
            "industry": "Unknown",
            "budget": "Not Disclosed",
            "past_deals": []
        }
    )
