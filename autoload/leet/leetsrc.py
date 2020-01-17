import os
class leetsrc():
    def get_151_problems_slug(self):
        f = open(os.path.dirname(__file__)+"/151problem.txt")
        slugs = f.read().splitlines()
        f.close()
        return slugs

    def get_151_problems(self,problems):
        ret =[]
        slugs = self.get_151_problems_slug()
        for problem in problems:
            if problem['slug'] in slugs:
                ret.append(problem)
        return ret

    def get_fav_list_problems(self,problems, fav_ids):
        ret =[]
        for problem in problems:
            if problem['id'] in fav_ids:
                ret.append(problem)
        return ret
    def format_fav_list(self,fav_lists):
        ret =[]
        for fav_list in fav_lists:
            fav_list["num"] = len(fav_list["questions"])
            fav_list["name"] = fav_list["name"].replace(' ','')
            ret.append(fav_list)
        return ret


    def format_problems(self, problems):
        ret = []
        for problem in problems:
            problem["level"] = self._level_to_name(problem["level"])
            problem["state"] = self._state_to_flag(problem["state"])
            ret.append(problem)
        return ret

    def _level_to_name(self, level):

        if  isinstance(level, str):
            return  level

        if level == 1:
            return 'Easy'
        if level == 2:
            return 'Medium'
        if level == 3:
            return 'Hard'
        return  ' '

    def _state_to_flag(self, state):
        if state == 'ac':
            return 'X'
        if state == 'notac':
            return '?'
        return  ' '


    def format_problem(self, problem):
        problem['desc'] = self._break_paragraph_lines(problem['desc'])
        for t in problem['templates']:
            problem['templates'][t] = self._break_code_lines(problem['templates'][t])
        return problem


    def _break_code_lines(self, s):
        return s.replace('\r\n', '\n').replace('\xa0', ' ').split('\n')


    def _break_paragraph_lines(self, s):
        lines = self._break_code_lines(s)
        result = []
        # reserve one and only one empty line between two non-empty lines
        for line in lines:
            if line.strip() != '':  # a line with only whitespaces is also empty
                result.append(line)
                result.append('')
        return result
