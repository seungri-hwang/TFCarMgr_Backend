dbSchema = {
        'ML_MEMBER': {
            'AUTO_INCREMENT': 'MM_ID',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'MM_ID',
                'MM_USER_EMAIL',
                'MM_USER_NAME',
                'MM_USER_PASSWORD',
                'CREATE_DT'
            ],
            'KEYS': [
                'MM_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'MM_ID',
                'MM_USER_EMAIL',
                'MM_USER_NAME'
            ],
            'SELECT_KEYS': [
            ]
        }
    ,   'CSL_FUEL_EFFICIENCY': {
            'AUTO_INCREMENT': 'CFE_ID',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'CFE_ID',
                'CFE_NAME',
                'CFE_EFFCIENCY_CD',
                'CFE_EXPLANATION_DESC',
                'CREATE_DT',
                'UPDATE_DT'
            ],
            'KEYS': [
                'CFE_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'CFE_ID',
                'CFE_EFFCIENCY_CD'
            ],
            'SELECT_KEYS': [
            ]
        }
    ,   'ML_FUEL_EFFICIENCY': {
            'AUTO_INCREMENT': '',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'MM_ID',
                'CFE_ID',
                'CREATE_DT',
                'UPDATE_DT'
            ],
            'KEYS': [
                'MM_ID',
                'CFE_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'MM_ID',
                'CFE_ID'
            ],
            'SELECT_KEYS': [
            ]
        }
    ,   'SL_STATS_CAR_ACCOUNT': {
            'AUTO_INCREMENT': 'SSCA_ID',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'SSCA_ID',
                'SSS_ID',
                'SST_ID',
                'VCI_ID',
                'SSCA_REG_DATE',
                'SSCA_PRICE_NUM',
                'SSCA_GAS_NUM',
                'SSCA_GAS_VOLUME_CD',
                'SSCA_DISTANCE_NUM',
                'SSCA_DISTANCE_CD',
                'SSCA_GASSTATION_NAME',
                'SSCA_NOTE',
                'CREATE_DT',
                'UPDATE_DT'
            ],
            'KEYS': [
                'SSCA_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'SSCA_ID',
                'SSS_ID',
                'SST_ID',
                'VCI_ID',
                'SSCA_GAS_VOLUME_CD'
            ],
            'SELECT_KEYS': [
            ]
        }
    ,   'SL_STATS_MILEAGE': {
            'AUTO_INCREMENT': 'SSM_ID',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'SSM_ID',
                'VCI_ID',
                'SSM_DISTANCE_NUM',
                'SSM_DISTANCE_CD',
                'CREATE_DT'
            ],
            'KEYS': [
                'SSM_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'SSM_ID',
                'VCI_ID',
                'SSM_DISTANCE_CD'
            ],
            'SELECT_KEYS': [
            ]
        }
    ,   'SL_STATS_SORT': {
            'AUTO_INCREMENT': 'SSS_ID',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'SSS_ID',
                'SSS_SORT_NAME',
                'SSS_ORDER_NUM',
                'CREATE_DT',
                'UPDATE_DT'
            ],
            'KEYS': [
                'SSS_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'SSS_ID',
                'SSS_ORDER_NUM'
            ],
            'SELECT_KEYS': [
            ]
        }
    ,   'SL_STATS_TYPE': {
            'AUTO_INCREMENT': 'SST_ID',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'SST_ID',
                'SST_TYPE_NAME',
                'SST_ORDER_NUM',
                'CREATE_DT',
                'UPDATE_DT'
            ],
            'KEYS': [
                'SST_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'SST_ID',
                'SST_ORDER_NUM'
            ],
            'SELECT_KEYS': [
            ]
        }
    ,   'VL_CAR_INFO': {
            'AUTO_INCREMENT': 'VCI_ID',
            'ADDTIONAL_DATA': [
            ],
            'COLUMNS': [
                'VCI_ID',
                'MM_ID',
                'VCI_CAR_NUMBER',
                'VCI_CAR_NAME',
                'CREATE_DT',
                'UPDATE_DT',
                'DEL_YN'
            ],
            'KEYS': [
                'VCI_ID'
            ],
            'NOT_NULL_COLUMNS': [
                'VCI_ID',
                'MM_ID',
                'VCI_CAR_NUMBER',
                'DEL_YN'
            ],
            'SELECT_KEYS': [
            ]
        }

}


