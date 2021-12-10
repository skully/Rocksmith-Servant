import requests


class Rocksniffer:
    def __init__(self, host, port):
        """
        Rocksniffer reader. Minimalistic, can be improved
        :param host: Rocksniffer host IP (localhost by default)
        :param port: Rocksniffer port (9938 by default)
        """
        self.host = host
        self.port = port

        self.memory = None

        self.artistName = None
        self.songName = None
        self.albumName = None
        self.songLength = None
        self.albumYear = None
        # TODO add last artist, song, etc. values? Needed?

        self.samples = [0, 0, 0]

    def update(self):
        """
        Get the content of Rocksniffer. In case of success, take a sample of the song time
        """
        try:
            self.memory = requests.get("http://{}:{}/".format(self.host, self.port)).json()
            if self.memory["success"]:
                self.take_sample()
                self.get_song_details()
        except:
            raise ConnectionError

    def get_song_details(self):
        self.artistName = self.memory['songDetails']['artistName']
        self.songName = self.memory['songDetails']['songName']
        self.albumName = self.memory['songDetails']['albumName']
        self.songLength = self.memory['songDetails']['songLength']
        self.albumYear = self.memory['songDetails']['albumYear']
        pass

    def take_sample(self):
        """
        Take a sample of the song time up to 3
        :return:
        """
        self.samples.append(self.memory['memoryReadout']['songTimer'])
        if len(self.samples) > 3:
            self.samples.pop(0)

    @property
    def success(self):
        try:
            return self.memory['success']
        except:
            return False

    @property
    def in_pause(self):
        """
        Logic for pause detection
        :return:
        """
        time_between_samples = abs(self.samples[0] - self.samples[2])
        if time_between_samples > 2:
            return True
        else:
            return not self.samples[0] < self.samples[1] < self.samples[2]

    @property
    def currentState(self):
        return self.memory["currentState"]

    @property
    def in_game(self):
        return self.currentState in range(3, 5)
