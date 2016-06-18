import websocket
import thread
import threading
import requests
from utils.logger import AppLogger


class SlackApi:
    GET = 'get'
    POST = 'post'

    def __init__(self, ui, users_table, token=None):
        self.logger = AppLogger.get_logger()
        self.UI = ui
        self._token = 'xoxp-4098964602-4096552845-19491432598-2b27154c5c'
        init_data = self._get_ws_basic_data()
        ws_url = self._get_ws_url(init_data)

        self.users = self._get_init_users(init_data)
        self._channels = self._get_init_channels(init_data)
        self._groups = self._get_init_groups(init_data)
        self._profile = self._get_init_profile(init_data)

        self.logger.info("$$$ INTIAL DATA")
        self.logger.info(init_data)

        self.logger.info(self.users)
        self.logger.info(self._channels)
        self.logger.info(self._profile)

        # ADDING USERS !!!
        # self.UI.USERS.add_many(self.users)
        users_table.add_many(self.users)

        self._ws = websocket.WebSocketApp(ws_url,
                                          on_message=self._api_on_message,
                                          on_error=self._api_on_error,
                                          on_close=self._api_on_close)

        self._ws.on_open = self._api_on_open
        self.logger.debug("="*160)
        self.logger.debug("PRE thread start")
        self._ws_thread = threading.Thread(target=self._ws.run_forever)
        self._ws_thread.start()
        self.logger.debug("POST thread start")
        # self._ws.run_forever()

    def _request(self, met, url, params=None):
        req_params = None

        if params is not None:
            req_params = '&'.join(['{}={}'.format(k, v)
                                   for k, v in params.iteritems()])

        if met == 'get':
            r = requests.get(url, req_params)

        if met == 'post':
            r = requests.post(url, req_params)

        self.logger.debug("REQUEST: "+url+" PARAMS: "+str(req_params))
        response_log = str(r.json())
        self.logger.debug("RESPONSE: "+response_log)

        return r

    def _get_ws_basic_data(self):
        url = 'https://slack.com/api/rtm.start?token='+self._token
        # r = requests.get(url)
        r = self._request(self.GET, url)
        if r.status_code != 200:
            raise Exception("Could not connect to Slack HTTP API")
        return r.json()

    def _get_ws_url(self, data):
        return data['url']

    def _get_init_channels(self, data):
        chnls = data['channels']
        channels = []

        for channel in chnls:
            c_dict = {'name': channel['name'], 'id': channel['id'],
                      'type': 'channel'}
            channels.append(c_dict)

        return channels

    def _get_init_groups(self, data):
        chnls = data['groups']
        groups = []

        for channel in chnls:
            c_dict = {'name': channel['name'], 'id': channel['id'],
                      'type': 'group'}
            groups.append(c_dict)

        return groups

    def _get_init_users(self, data):
        usrs = data['users']
        users = []
        for user in usrs:
            u_dict = {'name': user['name'],
                      'full_name': user['profile']['real_name_normalized'],
                      'presence': user['presence'], 'id': user['id']}
            users.append(u_dict)

        return users

    def _get_init_profile(self, data):
        profile = {'name': data['self']['name'], 'id': data['self']['id']}
        return profile

    def _api_on_message(self, ws, message):
        self.logger.info('INCOMING MESSAGE')
        self.logger.info(str(dict(message)))

        # print '%%%%%%%%%%%% MESSAGE %%%%%%%%%%%%'
        # print message
        pass

    def _api_on_error(self, ws, error):
        print '%%%%%%%%%%%% ERROR %%%%%%%%%%%%'
        print error

    def _api_on_close(self, ws):
        print "### closed ###"

    def _api_on_open(self, ws):
        self.UI.change_status('Connected')

        def run(*args):
            self.UI.change_status('Connected')
            # j = send_dummy_msg(channels[0]['id'])
            # ws.send(j.encode('utf-8'))

            # for i in range(3):
            # time.sleep(1)
            # # ws.send("Hello %d" % i)
            # time.sleep(1)
            # ws.close()
            # print "thread terminating..."
        thread.start_new_thread(run, ())

    def _retrieve_identity(self):
        url_base = "https://slack.com/api/"
        url_action = 'auth.test?'
        url_token = "token=" + str(self._token)
        url = url_base + url_action + url_token

        r = self._request(self.GET, url)
        if r.status_code != 200:
            raise Exception("Could not connect to Slack HTTP API")
        self.logger.info("REQUEST RESPONSE: auth.test" + str(r.json()))
        return r.json()

    def get_identity(self):
        if hasattr(self, '_identity') is False:
            self._identity = self._retrieve_identity()
        return self._identity

    def get_rooms(self):
        return self._channels

    def get_groups(self):
        return self._groups

    def get_messages(self, room, count=200):
        url_base = "https://slack.com/api/"

        if room['type'] == 'channel':
            url_action = 'channels.history?'
        elif room['type'] == 'group':
            url_action = 'groups.history?'
        else:
            raise NameError('Cannot retrieve messages of unknown type')

        url_token = "token=" + str(self._token)
        url_channel = "&channel=" + str(room['id']) + "&count=" + str(count)
        url = url_base + url_action + url_token + url_channel

        r = self._request(self.GET, url)
        if r.status_code != 200:
            raise Exception("Could not connect to Slack HTTP API")
        self.logger.info("REQUEST RESPONSE: channels.history" + str(r.json()))
        return r.json()

    def send_message(self, room, msg):
        url_base = "https://slack.com/api/"
        url_action = 'chat.postMessage?'
        url_token = "token=" + str(self._token)
        url_channel = "&channel=" + str(room['id']) + "&text=" + str(msg)
        url = url_base + url_action + url_token + url_channel

        self.logger.info("SEND MSG REQUEST " + str(url))

        r = self._request(self.GET, url)
        if r.status_code != 200:
            raise Exception("Could not connect to Slack HTTP API")
        self.logger.info("REQUEST RESPONSE: channels.history" + str(r.json()))
        return r.json()
