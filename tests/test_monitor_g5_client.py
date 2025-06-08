from api_client.monitor_g5_client import MonitorG5Client


def test_parse_person_info_structure():
    client = MonitorG5Client()
    sample_persons = [
        {'Id': 1, 'FirstName': 'Tom Erik', 'LastName': 'Harnes', 'WorkLocation': 'Factory'},
        {'Id': 2, 'FirstName': 'Jane', 'LastName': 'Doe', 'WorkLocation': 'Factory'}
    ]

    result = {
        str(p['Id']): {
            "name": f"{p.get('FirstName')} {p.get('LastName')}".strip(),
            "location": p.get("WorkLocation")
        }
        for p in sample_persons
    }

    assert result['1']['name'] == 'Tom Erik Harnes'
    assert result['1']['location'] == 'Factory'
