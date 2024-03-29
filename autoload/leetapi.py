import importlib
import req
import sys
import os


class leet():
    arg = "leet"
    session = ""
    headers = ""
    leet_source = ""
    def __init__(self, imp):
        source = os.getenv("leet_source")
        if source != None:
            self.leet_source =  source
        else:
            self.leet_source = "leet-cn"

        x = req.req("leet")
        self.session = x.get_curl(self.leet_source)
        self.headers = x.make_headers(self.session)
        self.imp = imp


    def get_problems(self, cat=["all"]):
        req = self._get_req_imp()
        problems = req.leet(self.session,self.headers,self.leet_source).get_problems(cat)
        return  self._format_problems(problems)

    def get_topics(self):
        req = self._get_req_imp()
        return req.leet(self.session,self.headers,self.leet_source).get_topics()


    def get_fav_list(self):

        return self.get_problemset_list()


    def get_problemset_list(self):
        req = self._get_req_imp()
        problemset_list = req.leet(self.session,self.headers,self.leet_source).get_problemset_list()

        for item in problemset_list["categories"]["0"]:
            item["cat"] = "cat"

        for item in problemset_list["categories"]["1"]:
            item["cat"] = "fav"

        problemset_list["categories"]["0"].extend(problemset_list["categories"]["1"])
        ret = problemset_list["categories"]["0"]
        for item in ret:
            item["name"] = item["title"]
        return ret

    def get_top_151_list(self):
        problems = self.get_problems_of_top151()
        top_list = {}
        top_list["name"] = "top151"
        top_list["num"] = len(problems)
        ret = []
        ret.append(top_list)
        return ret

    def get_problems_of_topic(self, topic):
        req = self._get_req_imp()
        topics = req.leet(self.session,self.headers,self.leet_source).get_problems_of_topic(topic)
        topics["problems"] =  self._format_problems(topics["problems"])
        return topics

    def _get_fav_list_problems(self, problems, fav_ids):
        req = self._get_req_imp("leetsrc")
        problems = req.leetsrc().get_fav_list_problems(problems, fav_ids)
        return  problems

    def get_problems_of_top151(self ):
        req = self._get_req_imp("leetsrc")
        all_problems = self.get_problems()
        problems = req.leetsrc().get_151_problems(all_problems )
        return  problems

    def _get_problem_questions(self, question_url, cat ):
        req = self._get_req_imp()
        problems = req.leet(self.session,self.headers,self.leet_source).get_problemset_list_ids(question_url, cat)
        ids = []
        for item in problems["stat_status_pairs"]:
            ids.append(item["stat"]["question_id"])
        return  ids



    def get_problems_of_fav(self,fav_name):

        fav = self.get_fav_list()
        question_url = ""
        for item in fav:
            if fav_name in item["name"]:
                question_url = item["slug"]
                question_cat = item["cat"]
        questions = self._get_problem_questions(question_url, question_cat)
        all_problems = self.get_problems()
        return self._get_fav_list_problems(all_problems, questions)

    def get_problem(self, problem_id):
        req = self._get_req_imp()
        problem =  req.leet(self.session,self.headers,self.leet_source).get_problem(problem_id)
        return self._format_problem(problem)

    def get_submissions(self, problem):
        req = self._get_req_imp("leetsubmit")
        submissions =  req.leetsubmit(self.session,self.headers,self.leet_source).get_submissions(problem)
        return  submissions

    def get_submit(self, sid):
        req = self._get_req_imp("leetsubmit")
        submission =  req.leetsubmit(self.session,self.headers,self.leet_source).get_submit(sid)
        req = self._get_req_imp("leetsubmitsrc")
        submission = req.leetsubmitsrc().format_submit(submission)
        problem = self.get_problem(submission['slug'])
        submission['title'] = problem['title']
        return  submission


    def get_submission(self, sid):
        req = self._get_req_imp("leetsubmit")
        submission =  req.leetsubmit(self.session,self.headers,self.leet_source).get_submission(sid)
        req = self._get_req_imp("leetsubmitsrc")
        submission = req.leetsubmitsrc().format_submit(submission)
        problem = self.get_problem(submission['slug'])
        submission['title'] = problem['title']
        return  submission

    def test_solution(self, problem_id, title, slug, filetype, code, test_input):
        req = self._get_req_imp("leetest")
        result_id =  req.leetest(self.session,self.headers,self.leet_source).test_solution(problem_id,  slug, filetype, code, test_input )

        req = self._get_req_imp("leetresult")
        result =  req.leetresult(self.session,self.headers,self.leet_source).check_result(result_id)
        result['testcase'] = test_input.split('\n')
        result['title'] = title
        return result

    def submit_solution(self,slug, filetype, code=None):
        problem = self.get_problem(slug)
        req = self._get_req_imp("leetsubmit")
        result_id =  req.leetsubmit(self.session,self.headers,self.leet_source).submit_solution(slug, filetype, code, problem)

        req = self._get_req_imp("leetresult")
        result =  req.leetresult(self.session,self.headers,self.leet_source).check_result(result_id)
        result['title'] = problem["title"]
        return result

    def _format_fav_list(self, fav_list):
        req = self._get_req_imp("leetsrc")
        return req.leetsrc().format_fav_list(fav_list)

    def _format_problems(self, problems):
        req = self._get_req_imp("leetsrc")
        return req.leetsrc().format_problems(problems)

    def _format_problem(self, problem):
        req = self._get_req_imp("leetsrc")
        return req.leetsrc().format_problem(problem)

    def _get_req_imp(self,name="leetapi"):
        importClass = self.arg+"."+ name
        req=importlib.import_module(importClass)
        return req


def get_problems( cat=["all"]):
    x = leet("leet");
    problems = x.get_problems()
    return sorted(problems, key = lambda i: i['fid'])

def get_topics():
    x = leet("leet");
    topics = x.get_topics()
    return  topics


def get_fav_list():
    x = leet("leet");
    fav_list = x.get_fav_list()
    return  fav_list

def get_problemset_list():
    x = leet("leet");
    x.get_problemset_list()


def get_problems_of_topic( topic):

    x = leet("leet");
    topic = x.get_problems_of_topic(topic)
    return topic

def get_fav_list_problems( problems, fav_ids):
    x = leet("leet");
    problems = x.get_fav_list_problems(problems, fav_ids)
    return problems

def get_problem( problem_id):
    x = leet("leet");
    problem = x.get_problem(problem_id)
    return problem

def get_problems_of_fav( fav_name):
    x = leet("leet");
    problems = x.get_problems_of_fav(fav_name)
    return problems

def get_problems_of_top151( ):
    x = leet("leet");
    problems = x.get_problems_of_top151()
    return problems
def get_top_151_list():
    x = leet("leet");
    lists = x.get_top_151_list()
    return lists

def get_submissions(problem ):
    x = leet("leet");
    submissions = x.get_submissions(problem)
    return submissions

def get_submission(sid ):
    x = leet("leet");
    submission = x.get_submission(sid)
    return submission


def test_solution( problem_id, title, slug, filetype, code, test_input):
    x = leet("leet");
    test = x.test_solution( problem_id, title, slug, filetype, code, test_input)
    return test


def submit_solution(slug, filetype, code=None):
    x = leet("leet");
    submit = x.submit_solution(slug, filetype, code)
    return submit

if __name__ == "__main__":
    x = leet("leet");
    print("####################")
    fav = x.get_fav_list()
    print(fav)
    print("####################")


    # fav = x.get_problems_of_fav(fav[len(fav)-2]["name"])
    # print(fav)

    problems = x.get_problems()
    all_problems = problems

    print("####################")
    print("all problems nums:")
    print(len(problems))
    print("frist problems:")
    print(problems)

    sys.exit()

    # print("####################")
    # topics = x.get_topics()
    # print("all topics nums:")
    # print(len(topics))
    # print("frist topics:")
    # print(topics[0])


    # print("####################")
    # topic_name = "sliding-window"
    # topics = x.get_problems_of_topic(topic_name)
    # problems = topics["problems"]
    # print("all topics problems nums:")
    # print(len(problems))
    # print("frist topics problem:")
    # print(problems[0])


    # problem_id = "13"
    # title = "Roman To Integer"
    # slug = "roman-to-integer"
    # filetype = "golang"
    # code = "func romanToInt(s string) int {\n    return 1\n}"
    # test_input = "\"III\""
    # x.test_solution(problem_id, title, slug, filetype, code, test_input)

    slug = "two-sum"
    submissions = x.get_submissions(slug)
    print("first submissions :")
    print(submissions)
    print("####################")
    x.get_submit("383003768")

    # submission = x.get_submission(submissions[0]['id'])
    # print("submission :")
    # print(submission)
    # print("####################")



    sys.exit()

    # print("####################")
    # fav = x.get_fav_list()
    # print("all fav nums:")
    # print(len(fav))
    # print("last fav:")
    # print(fav[0])
    # print("####################")

    # fav_name = fav[0]["name"].replace(' ','')
    # fav = x.get_problems_of_fav(fav_name)
    # print("fav list:")
    # print(len(fav))
    # print("first fav:")
    # print(fav[0])
    # print("####################")


    # problem = x.get_problem(fav[0]['slug'])
    # print("problem :")
    # print(problem)
    # print("####################")


    # problems = x.get_problems_of_top151()
    # print("num:")
    # print(len(problems))
    # print("151 problem  :")
    # print(problems[0])
    # print("####################")


    # top_list = x.get_top_151_list()
    # print("151 list  :")
    # print(top_list)
    # print("####################")

