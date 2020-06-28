import sys
from bs4 import BeautifulSoup
import json
from . import   mycfg


class leet():
    session=""
    headers = ""
    LC_BASE = ""
    LC_PROBLEM = ""
    LC_CATEGORY_PROBLEMS =  ""
    LC_PROBLEM_SET_ALL =  ""
    LC_PROBLEM_FAV = ""
    LC_GRAPHQL =  ""
    EMPTY_FREQUENCIES = [0, 0, 0, 0, 0, 0, 0, 0]


    def __init__(self, session, headers, source="leet"):
        self.session= session
        self.headers = headers
        self.LC_BASE = mycfg.getConfig(source,"LC_BASE")
        self.LC_PROBLEM= mycfg.getConfig(source,"LC_PROBLEM")
        self.LC_CATEGORY_PROBLEMS= mycfg.getConfig(source,"LC_CATEGORY_PROBLEMS")
        self.LC_PROBLEM_SET_ALL= mycfg.getConfig(source,"LC_PROBLEM_SET_ALL")
        self.LC_PROBLEM_FAV= mycfg.getConfig(source,"LC_PROBLEM_FAV")
        self.LC_GRAPHQL= mycfg.getConfig(source,"LC_GRAPHQL")


    def _get_category_problems(self,category):
        headers = self.headers
        url = self.LC_CATEGORY_PROBLEMS.format(category=category)
        res = self.session.get(url, headers=headers)
        if res.status_code != 200:
            return []

        problems = []
        content = res.json()
        for p in content['stat_status_pairs']:
            # skip hidden questions
            if p['stat']['question__hide']:
                continue
            problem = {'state':p['status'],
                       'id': p['stat']['question_id'],
                       'fid': p['stat']['frontend_question_id'],
                       'title': p['stat']['question__title'],
                       'slug': p['stat']['question__title_slug'],
                       'paid_only': p['paid_only'],
                       'ac_rate': p['stat']['total_acs'] / p['stat']['total_submitted'],
                       'level': p['difficulty']['level'],
                       'favor': p['is_favor'],
                       'category': content['category_slug'],
                       'frequency': p['frequency']}
            problems.append(problem)
        return problems



    def get_problems(self,categories=['all']):
        problems = []
        for c in categories:
            problems.extend(self._get_category_problems(c))
        return sorted(problems, key=lambda p: p['id'])


    def get_topics(self):
        topics_and_comp = self._get_topics_and_companies()
        return topics_and_comp['topics']

    def get_companies(self):
        topics_and_comp = self._get_topics_and_companies()
        return topics_and_comp['companies']

    def _get_topics_and_companies(self):
        headers = self.headers
        res = self.session.get(self.LC_PROBLEM_SET_ALL, headers=headers)
        if res.status_code != 200:
            return []

        soup = BeautifulSoup(res.text, features='html.parser')

        topic_elements = soup.find_all(class_='sm-topic')
        topics = [self._process_topic_element(topic) for topic in topic_elements]

        company_elements = soup.find_all(class_='sm-company')
        companies = [self._process_company_element(company) for company in company_elements]
        return {
            'topics': topics,
            'companies': companies
            }

    def _process_topic_element(self,topic):
        return {'topic_name': topic.find(class_='text-gray').string.strip(),
                'num_problems': topic.find(class_='badge').string,
                'topic_slug': topic.get('href').split('/')[2]}


    def _process_company_element(self,company):
        return {'company_name': company.find(class_='text-gray').string.strip(),
                'num_problems': company.find(class_='badge').string,
                'company_slug': company.get('href').split('/')[2]}

    def get_fav_list(self):
        headers = self.headers
        res = self.session.get(self.LC_PROBLEM_FAV, headers=headers)
        if res.status_code != 200:
            return []
        content = res.json()
        return content

    def get_problems_of_topic(self, topic_slug):
        request_body = {
            'operationName':'getTopicTag',
            'variables': {'slug': topic_slug},
            'query': '''query getTopicTag($slug: String!) {
      topicTag(slug: $slug) {
        name
        translatedName
        questions {
          status
          questionId
          questionFrontendId
          title
          titleSlug
          translatedTitle
          stats
          difficulty
          isPaidOnly
        }
        frequencies
      }
    }
    '''}

        headers =  self.headers

        res = self.session.post(self.LC_GRAPHQL, headers=headers, json=request_body)

        if res.status_code != 200:
            return {'topic_name': topic_slug, 'problems': []}

        topic_tag = res.json()['data']['topicTag']

        if not topic_tag:
            return {'topic_name': topic_slug, 'problems': []}

        if topic_tag['frequencies']:
            id_to_frequency_map = json.loads(topic_tag['frequencies'])
        else:
            id_to_frequency_map = {}

        def process_problem(p):
            stats = json.loads(p['stats'])

            return {
                'state': p['status'],
                'id': p['questionId'],
                'fid': p['questionFrontendId'],
                'title': p['title'],
                'slug': p['titleSlug'],
                'paid_only': p['isPaidOnly'],
                'ac_rate': stats['totalAcceptedRaw'] / stats['totalSubmissionRaw'],
                'level': p['difficulty'],
                'favor': False,
                'frequency': id_to_frequency_map.get(p['questionId'], 0)}

        return {
            'topic_name': topic_tag['name'],
            'problems': [process_problem(p) for p in topic_tag['questions']]}

    def get_problem(self,slug):
        headers = self.headers
        headers['Referer'] = self.LC_PROBLEM.format(slug=slug)
        body = {'query': '''query getQuestionDetail($titleSlug : String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        content
        stats
        difficulty
        codeDefinition
        sampleTestCase
        enableRunCode
        translatedContent
      }
    }''',
                'variables': {'titleSlug': slug},
                'operationName': 'getQuestionDetail'}
        res = self.session.post(self.LC_GRAPHQL, json=body, headers=headers)
        if res.status_code != 200:
            return None

        q = res.json()['data']['question']

        content = q['translatedContent'] or q['content']
        if content is None:
            return None

        soup = BeautifulSoup(content, features='html.parser')
        problem = {}
        problem['id'] = q['questionId']
        problem['title'] = q['title']
        problem['slug'] = slug
        problem['level'] = q['difficulty']
        problem['desc'] = soup.get_text()
        problem['templates'] = {}
        for t in json.loads(q['codeDefinition']):
            problem['templates'][t['value']] = t['defaultCode']
        problem['testable'] = q['enableRunCode']
        problem['testcase'] = q['sampleTestCase']
        stats = json.loads(q['stats'])
        problem['total_accepted'] = stats['totalAccepted']
        problem['total_submission'] = stats['totalSubmission']
        problem['ac_rate'] = stats['acRate']
        return problem
