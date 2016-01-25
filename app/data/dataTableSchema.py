dbSchema = {
            'ML_MEMBER': {
                            'ADDTIONAL_DATA': [],
                            'AUTO_INCREMENT': 'MM_ID',
                            'COLUMNS': [
                                          'MM_ID',
                                          'MM_USER_EMAIL',
                                          'MM_USER_NAME',
                                          'MM_USER_PASSWORD',
                                          'CREATE_DT'
                                        ],
                            'KEYS': [
                                        'MM_ID',
                                        'MM_USER_EMAIL'
                                    ],
                            'NOT_NULL_COLUMNS':
                                        [
                                            'MM_ID',
                                           'MM_USER_EMAIL',
                                           'MM_USER_NAME'
                                        ],
                            'SELECT_KEYS': [],
                            'TABLE_NAME': 'ML_MEMBER'
                            },

            'VL_CAR_INFO': {
                            'ADDTIONAL_DATA': [],
                            'AUTO_INCREMENT': 'VCI_ID',
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
                                          'VCI_ID',
                                          'MM_ID',
                                          'VCI_CAR_NUMBER'
                                    ],
                            'NOT_NULL_COLUMNS':
                                          [
                                          'VCI_ID',
                                          'MM_ID',
                                          'DEL_YN'
                                          ],
                             'SELECT_KEYS': [],
                             'TABLE_NAME': 'VL_CAR_INFO'
                            }
            }
