class leetsubmitsrc():

    def format_submit(self, problem):
        problem["state"] = self._status_to_name(problem["state"])
        return problem

    def _status_to_name(self,status):
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
