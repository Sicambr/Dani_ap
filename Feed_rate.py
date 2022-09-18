"""This modul count feed rate
"""

class feed_r:
    def __init__(self, My_block, title):
        self.My_block = My_block
        self.title = title
        self.feed = []
        self.parametrs = {}


    # Find a feed
    def feed_mesuare(self):
        i = 0
        means_F = '0123456789.'
        if self.title == 'milling' or self.title == 'Drill':
            while i < len(self.My_block):
                feed_rate = ''
                f = ''
                if (len(self.My_block[i]) > 1 and self.My_block[i][:1] != '('
                    and 'F' in self.My_block[i]):
                    feed_rate = self.My_block[i].partition('F')[2]
                    j = 0
                    while j < len(feed_rate):
                        if feed_rate[j] in means_F:
                            f = f + feed_rate[j]
                        else:
                            j = len(feed_rate)
                        j += 1
                if f != '' and f not in self.feed:
                    self.feed.append(f)
                i += 1
        elif (self.title == 'old_boring' or self.title == 'Loop'
              or self.title == 'milling_GOTO'):
            while i < len(self.My_block):
                feed_rate = ''
                f = ''
                if (len(self.My_block[i]) > 1 and self.My_block[i][:1] == '#'):
                    feed_rate = self.My_block[i].partition('=')[2]
                    j = 0
                    while j < len(feed_rate):
                        if feed_rate[j] in means_F:
                            f = f + feed_rate[j]
                        else:
                            j = len(feed_rate)
                        j += 1
                    self.parametrs[self.My_block[i].partition('=')[0]] = f
                elif (len(self.My_block[i]) > 1 and self.My_block[i][:1] != '('
                    and 'F' in self.My_block[i]):
                    feed_rate = self.My_block[i].partition('F')[2]
                    if len(feed_rate) > 0 and feed_rate[0] == '#':
                        j = 1
                        par = '#'
                        while j < len(feed_rate):
                            if feed_rate[j] in means_F:
                                par = par + feed_rate[j]
                            else:
                                j = len(feed_rate)
                            j += 1
                        if par in self.parametrs:
                            f = self.parametrs[par]
                        else:
                            f = ''
                    else:
                        j = 0
                        while j < len(feed_rate):
                            if feed_rate[j] in means_F:
                                f = f + feed_rate[j]
                            else:
                                j = len(feed_rate)
                            j += 1
                    if f != '' and f not in self.feed:
                        self.feed.append(f)
                i += 1
        return self.feed


    # Replace feed
    def feed_rep(self,title, old_feed, new_feed):
        means_F = '0123456789.'
        if title == 'milling' or title == 'Drill':
            i = 0
            while i < len(self.My_block):
                feed_rate = ''
                if ('F' + old_feed) in self.My_block[i]:
                    feed_rate = self.My_block[i].partition('F' + old_feed)[2]
                    if len(feed_rate) > 0 and feed_rate[0] not in means_F:
                        self.My_block[i] = self.My_block[i].replace('F' + old_feed, 'F' + new_feed)
                i += 1
        elif (title == 'old_boring' or title == 'Loop'
              or title == 'milling_GOTO'):
            if old_feed in self.parametrs.values():
                my_par = ''
                for k in self.parametrs:
                    if self.parametrs[k] == old_feed:
                        my_par = my_par + k
                my_par = my_par + '='
                i = 0
                while i < len(self.My_block):
                    if my_par in self.My_block[i]:
                        self.My_block[i] = self.My_block[i].replace(old_feed, new_feed)
                    i += 1
            i = 0
            while i < len(self.My_block):
                feed_rate = ''
                if ('F' + old_feed) in self.My_block[i]:
                    feed_rate = self.My_block[i].partition('F' + old_feed)[2]
                    if len(feed_rate) > 0 and feed_rate[0] not in means_F:
                        self.My_block[i] = self.My_block[i].replace('F' + old_feed, 'F' + new_feed)
                i += 1            
        return self.My_block
