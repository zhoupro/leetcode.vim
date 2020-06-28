import time
from . import   mycfg

class leetresult():
    session=""
    headers = ""
    LC_BASE = ''
    LC_CHECK = ''


    def __init__(self, session, headers, source="leet"):
        self.session= session
        self.headers = headers

        self.LC_BASE = mycfg.getConfig(source,"LC_BASE")
        self.LC_CHECK = mycfg.getConfig(source,"LC_CHECK")

    def check_result(self,submission_id):
        while True:
            headers = self.headers
            url = self.LC_CHECK.format(submission=submission_id)
            res = self.session.get(url, headers=headers)
            if res.status_code != 200:
                return None
            r = res.json()
            if r['state'] == 'SUCCESS':
                prog_stage = 'Done      '
                break
            elif r['state'] == 'PENDING':
                prog_stage = 'Pending   '
            elif r['state'] == 'STARTED':
                prog_stage = 'Running   '
            time.sleep(1)

        result = {
            'answer': r.get('code_answer', []),
            'runtime': r['status_runtime'],
            'state': self._status_to_name(r['status_code']),
            'testcase': self._split(r.get('input', r.get('last_testcase', ''))),
            'passed': r.get('total_correct') or 0,
            'total': r.get('total_testcases') or 0,
            'error': [v for k, v in r.items() if 'error' in k and v]
        }

        # the keys differs between the result of testing the code and submitting it
        # for submission judge_type is 'large', and for testing judge_type does not exist
        if r.get('judge_type') == 'large':
            result['answer'] = self._split(r.get('code_output', ''))
            result['expected_answer'] = self._split(r.get('expected_output', ''))
            result['stdout'] = self._split(r.get('std_output', ''))
            result['runtime_percentile'] = r.get('runtime_percentile', '')
        else:
            # Test states cannot distinguish accepted answers from wrong answers.
            if result['state'] == 'Accepted':
                result['state'] = 'Finished'
            result['stdout'] = r.get('code_output', [])
            result['expected_answer'] = []
            result['runtime_percentile'] = r.get('runtime_percentile', '')
            result['expected_answer'] = r.get('expected_code_answer', [])
        return result


    def _split(self,s):
        # str.split has an disadvantage that ''.split('\n') results in [''], but what we want
        # is []. This small function returns [] if `s` is a blank string, that is, containing no
        # characters other than whitespaces.
        if s.strip() == '':
            return []
        return s.split('\n')

    def _status_to_name(self, status):
        if status == 10:
            return 'Accepted'
        if status == 11:
            return 'Wrong Answer'
        if status == 12:
            return 'Memory Limit Exceeded'
        if status == 13:
            return 'Output Limit Exceeded'
        if status == 14:
            return 'Time Limit Exceeded'
        if status == 15:
            return 'Runtime Error'
        if status == 16:
            return 'Internal Error'
        if status == 20:
            return 'Compile Error'
        if status == 21:
            return 'Unknown Error'
        return 'Unknown State'
