from ARQMathCode.post_reader_record import DataReaderRecord

from datetime import datetime
from collections import defaultdict
import json

data_path = '../raw_data'
out_dir = '.'
reader = DataReaderRecord(data_path, version='1.2')
answers = defaultdict(list)

def clean_votes(votes):
    cleaned = {'accepted': False, 'vote_count':0}
    if votes is None:
        return cleaned
    for vote in votes:
        if vote.vote_type_id == 1:
            cleaned['accepted'] = True
        elif vote.vote_type_id == 2:
            cleaned['vote_count'] += 1
        elif vote.vote_type_id == 3:
            cleaned['vote_count'] -= 1
    return cleaned


cleaned = []
for year in [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]:
    print(f'Processing Year - {year}')
    now = datetime.now()
    questions = reader.get_list_of_questions_posted_in_a_year(year)
    for q in questions:
        accepted_answer_id = q.accepted_answer_id
        thread = {'post_id': q.post_id, 'accepted_answer_id': accepted_answer_id}
        thread['tags'] = q.tags
        if q.answers:
            thread['answer_ids'] = []
            thread['votes'] = []
            for a in q.answers:
                thread['answer_ids'].append(a.post_id)
                thread['votes'].append(clean_votes(a.votes))
        thread['related_posts'] = []
        thread['duplicates'] = []
        for p_id, is_duplicate in q.related_post:
            if is_duplicate:
                thread['duplicates'].append(p_id)
            else:
                thread['related_posts'].append(p_id)
        cleaned.append(thread)
    print(f'{year} took: {datetime.now() - now}')
del reader
del questions
json.dump(cleaned, open(f'{out_dir}/cleaned_votes_only.json', 'w', encoding='utf-8'))
print('Done saving cleaned json.')
