import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)
from jinaai import JinaAI

jinaai = JinaAI(
    tokens = {
        'promptperfect-token': os.environ.get('PROMPTPERFECT_TOKEN', ''),
        'scenex-token': os.environ.get('SCENEX_TOKEN', ''),
        'rationale-token': os.environ.get('RATIONALE_TOKEN', ''),
        'chatcat-token': os.environ.get('CHATCAT_TOKEN', '')
    }
)

def toBase64(img: str) -> str:
    return jinaai.utils.image_to_base64(f"examples/images/{img}")

situations = [toBase64(img) for img in [
    'factory-1.png',
    'factory-2.png',
    'factory-3.png',
    'factory-4.png',
]]

def evaluate():
    try:
        # 1. get a description of each situations
        descriptions = jinaai.describe(situations)
        for i, desc in enumerate(descriptions['results']):
            print(f"DESCRIPTION {i + 1}:\n{desc['output']}\n")
        # 2. get an analysis based on those descriptions
        analysis = jinaai.generate('\n'.join([
            'Does any of those situations present a danger?',
            'Reply with [SITUATION_NUMBER] [YES] or [NO] and explain why',
            *['SITUATION ' + str(i + 1) + ':\n' + desc['output'] for i, desc in enumerate(descriptions['results'])]
        ]))
        print('ANALYSIS:\n', analysis['output'])
        # 3. get a recommendation on the most urgent action to take
        recommendation = jinaai.generate('\n'.join([
            'According to those situations, what should be done first to make everything safer?',
            'I only want the most urgent situation',
            *['SITUATION ' + str(i + 1) + ':\n' + desc['output'] for i, desc in enumerate(descriptions['results'])]
        ]))
        print('RECOMMENDATION:\n', recommendation['output'])
        # 4. get a swot analysis of the recommendation
        swot = jinaai.decide(
            recommendation['output'],
            { 'analysis': 'swot' }
        )
        print('SWOT:\n', swot['results'][0]['swot'])
    except Exception as e:
        print("Error:", str(e))

evaluate()
