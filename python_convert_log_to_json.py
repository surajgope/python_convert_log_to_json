python_convert_log_to_json.py
# Python Convert Log to JSON
----------------------------
# read_log_file.py
# Read last n lines from Kite Log File



import re
import json


'''
logging.basicConfig(
    filename    = 'example.log', 
    encoding    = 'utf-8', 
    level       = logging.DEBUG,
    format      = '%(asctime)s - %(levelname)s - %(message)s'
)
# logger = logging.getLogger(__name__)
'''

def read_last_n_lines(file,lines_to_read):
    with open(file,'r') as file:
        lines = file.readlines()
    return lines[-lines_to_read:]

def convert_to_json(lines: list):
    json_data = []
    # check if the lines are Candle Response or not
    candle_responses = [line for line in lines if 'Candle response' in line]
    for line in candle_responses:
        line = line.split('$')
        timestamp_utc   = line[0]
        levelname       = line[1]
        candle_response = re.sub('[\[\]\n]','',line[2]).split(',')
        try:
            timestamp_ist   = candle_response[0].split(' ')[2].strip(r'\'')
            value_1         = candle_response[1].strip()
            value_2         = candle_response[2].strip()
            value_3         = candle_response[3].strip()
            value_4         = candle_response[4].strip()
            value_5         = candle_response[5].strip()        
        except:
            timestamp_ist   =   None
            value_1         =   None
            value_2         =   None
            value_3         =   None
            value_4         =   None
            value_5         =   None    
        json_data.append({
            'timestamp_utc' :   timestamp_utc,
            'levelname'     :   levelname,
            'timestamp_ist' :   timestamp_ist,
            'value_1'       :   value_1,
            'value_2'       :   value_2,
            'value_3'       :   value_3,
            'value_4'       :   value_4,
            'value_5'       :   value_5          
        })
    json_data = json.dumps(json_data)
    #json_data = json.dumps(json_data, indent=2)
    return json_data


lines_to_read = 50
log_file = '/tmp/kite_test/kite.log'
json_file = '/tmp/kite_test/kite.json'
lines = read_last_n_lines(log_file,lines_to_read)
json_data = convert_to_json(lines)
save_json_to_file(json_data,json_file)


def save_data_to_file(data:list, json_file):
    with open(json_file, 'w') as file:
        for line in data:
            file.write(line)
    print(f'data saved to {json_file}')


def save_json_to_file(data:list, json_file):
    with open(json_file, 'w') as file:
        json.dump(data, file)
    print(f'json data saved to {json_file}')


'''
def save_to_dynamodb(table_name, json_data):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for item in json_data:
            batch.put_item(Item=item)

def send_data_to_api(url, json_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=json_data, headers=headers)
    if response.status_code == 200:
        logger.info("Data sent to API successfully.")
    else:
        logger.error(f"Failed to send data to API. Status code: {response.status_code}")
'''

def main():
    lines_to_read = 50
    log_file = '/home/ec2-user/py-market-fetch/kite.log'
    json_file = '/tmp/kite_test/kite.json'
    lines = read_last_n_lines(log_file,lines_to_read)
    json_data = convert_to_json(lines)
    save_json_to_file(lines,json_file)

    # table_name = 'your-dynamodb-table-name'
    #save_to_dynamodb(table_name, json_data):
    
    # api_endpoint = 'http://your-api-endpoint.com'
    #send_data_to_api(url, json_data):


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60)  # Wait for 60 seconds before the next execution
