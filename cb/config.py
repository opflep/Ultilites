class Config:
    CB = {
        'BASE_URL': 'https://10.14.132.35',
        'TOKEN': os.getenv('APIToken'),  
        'SSL_VERIFY': False,
        'ALERT_TYPE': {
            'PROCESS': ['alert.watchlist.hit.query.process', 'watchlist.hit.query.process']
        },
        'WATCHLIST_URL': '{base_url}/#/watchlist/{watchlist_id}',
        'PROCESS_URL': '{base_url}/#/analyze/{process_id}/{segment_id}?cb.legacy_5x_mode=false',
        'TENANT': 'CSD_Workstation'
    }
