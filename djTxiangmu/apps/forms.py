
class FormMixin:
    # @staticmethod
    def get_error(self):
        if hasattr(self,'error'):
            '''
                   {
                       'telephone': [
                                       {'message': '手机号长度有误','code': 'max_length'}
                                   ],
                        'password': [
                                       {'message': '密码长度有误','code': 'max_length'}
                                   ]
                    }
                   '''
            # print(error_json)

            '''
            (
                'telephone', [
                                {'message': '手机号长度有误', 'code': 'max_length'}
                            ]
            )
            '''

            error_tuple = self.error_json.popitem()
            error_list = error_tuple[1]
            error_dict = error_list[0]
            # error_dict=error_json.popitem()[1][0]
            # print(error_dict['message'])
            message = error_dict['message']
            return message
        return None
