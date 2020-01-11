import importlib
import req


class leet():
    arg = "leet"
    session = ""
    headers = ""
    def __init__(self, imp):
        x = req.req("leet")
        self.session = x.get_curl()
        self.headers = x.make_headers(self.session)
        self.imp = imp

    def get_problems(self, cat=["all"]):
        req = self._get_req_imp()
        problems = req.leet(self.session,self.headers).get_problems(cat)
        return  self._format_problems(problems)

    def get_topics(self):
        req = self._get_req_imp()
        return req.leet(self.session,self.headers).get_topics()


    def get_fav_list(self):
        req = self._get_req_imp()
        fav_list = req.leet(self.session,self.headers).get_fav_list()
        return self._format_fav_list(fav_list)

    def get_problems_of_topic(self, topic):
        req = self._get_req_imp()
        topics = req.leet(self.session,self.headers).get_problems_of_topic(topic)
        topics["problems"] =  self._format_problems(topics["problems"])
        return topics

    def _get_fav_list_problems(self, problems, fav_ids):
        req = self._get_req_imp("leetsrc")
        problems = req.leetsrc().get_fav_list_problems(problems, fav_ids)
        return  problems

    def get_problems_of_fav(self,fav_name):
        fav = self.get_fav_list()
        all_problems = self.get_problems()
        return self._get_fav_list_problems(all_problems, fav[0]['questions'])

    def get_problem(self, problem_id):
        req = self._get_req_imp()
        problem =  req.leet(self.session,self.headers).get_problem(problem_id)
        return self._format_problem(problem)

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
    return problems

def get_topics():
    x = leet("leet");
    topics = x.get_topics()
    return  topics


def get_fav_list():
    x = leet("leet");
    fav_list = x.get_fav_list()
    return  fav_list

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
    problem = x.get_problems_of_fav(fav_name)
    return problem


if __name__ == "__main__":
    x = leet("leet");

    problems = x.get_problems()
    all_problems = problems

    print("####################")
    print("all problems nums:")
    print(len(problems))
    print("frist problems:")
    print(problems[0])
    exit()

    print("####################")
    topics = x.get_topics()
    print("all topics nums:")
    print(len(topics))
    print("frist topics:")
    print(topics[0])


    print("####################")
    topic = topics[0]
    print("topic name:")
    print(topic["topic_name"])
    topics = x.get_problems_of_topic(topic["topic_name"])
    problems = topics["problems"]
    print("all topics problems nums:")
    print(len(problems))
    print("frist topics problem:")
    print(problems[0])



    print("####################")
    fav = x.get_fav_list()
    print("all fav nums:")
    print(len(fav))
    print("last fav:")
    print(fav[0])
    print("####################")

    fav_name = fav[0]["name"].replace(' ','')
    fav = x.get_problems_of_fav(fav_name)
    print("fav list:")
    print(len(fav))
    print("first fav:")
    print(fav[0])
    print("####################")

    problem = x.get_problem(fav[0]['slug'])
    print("problem :")
    print(problem)
    print("####################")
