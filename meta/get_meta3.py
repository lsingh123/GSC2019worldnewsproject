#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:10:42 2019

@author: lavanyasingh
"""

from bs4 import BeautifulSoup
import csv
import time
import os
os.chdir(os.path.dirname(os.getcwd()))
import subprocess
import tempfile
import pychrome
import threading

CHROMIUM = '/usr/bin/chromium-browser'

class ChromeHandler():
    
    def __init__(self):
        self.port = 0
        self.ph = None
        self.chrome_home = tempfile.mkdtemp(prefix='chrome-home')
        self.profile_dir = os.path.join(self.chrome_home, 'profile')
        if not os.path.isdir(self.profile_dir):
            os.mkdir(self.profile_dir)
        self.__lock = threading.RLock()
    
    def start_chrome(self):
        args = [
            CHROMIUM,
            '--headless',
            '--homepage', 'blank:',
            '--disable-gpu',
            '--hide-scrollbars',
            '--noerrdialogs',
            '--no-pings',
            '--safebrowsing-disable-auto-update',
            '--disable-suggestions-ui',
            '--disable-speech-api',
            '--disable-background-timer-throttling',
            '--disable-breakpad',
            '--disable-client-side-phishing-detection',
            '--disable-cloud-import',
            '--disable-component-cloud-policy',
            '--disable-default-apps',
            '--disable-demo-mode',
            '--disable-domain-reliability',
            '--disable-infobars'
        ]
        self.chrome_home = tempfile.mkdtemp(prefix='chrome-home')
        env = dict(os.environ, HOME=self.chrome_home)
        self.ph = subprocess.Popen(args, env=env, close_fds=True)
        self._connect()
        
    def _connect(self):
        if self.port == 0:
            portfile = os.path.join(self.profile_dir, 'DevToolsActivePort')
            retries = 0
            while retries < 3:
                try:
                    with open(portfile, 'r') as f:
                        # chrome writes out port number in the first line
                        # by itself. there follows more line(s).
                        self.port = int(f.readline())
                    break
                except IOError as ex:
                    print('failed to read debugging port from %s (retrying)',
                        portfile)
                    time.sleep(1.0)
                retries += 1
                
        url= "http://127.0.0.1:{}".format(self.port)
        self.client = pychrome.Browser(url=url)
        while True:
            try:
                version = self.client.version()
                print('connected version=%s', version)
                break
            except ConnectionError as ex:
                print('failed to connect to %s (retrying)', url)
                time.sleep(1.0)
                
    def terminate(self):
        if self.ph:
            rc = self.ph.poll()
            if rc is None:
                self.ph.terminate()
            rc = self.ph.wait()
            self.ph = None
            self.client = None
            
    def __del__(self):
        try:
            self.terminate()
        except:
            pass
        
    def check_respawn(self):
        with self.__lock:
            rc = self.ph.poll()
            if rc is None:
                # still alive / respawned
                return
            elif rc in (-2, -15, -9):
                # If chrome was killed by SIGINT/TERM/KILL, that's intended.
                # we don't want to restart it.
                print('chrome died with signal %d', -rc)
                raise KeyboardInterrupt()
            else:
                print('chrome died with rc=%d', rc)
                self.ph = None

    def open_session(self):
        """Return new session (represented as Tab object).
        """
        with self.__lock:
            if self.ph is None:
                self.start_chrome()
        tab = self.client.new_tab()
        return tab

    def close_session(self, tab):
        # close_tab() fails with "connection refused" if
        # chrome has been terminated.
        try:
            self.client.close_tab(tab)
        except IOError as ex:
            self._log.warning('close_tab failed: %s', ex)
            self.check_respawn()

class Crawler():

    PATH = os.getcwd() + "/data"

    def __init__(self):
        self.res, self.urls = [], []
        self.read_in()
        self.count = 0
        self.chrome = ChromeHandler()
    
    def shutdown(self):
        if self.chrome:
            self.chrome.terminate()

    def read_in(self):
        with open(self.PATH + "/all_raw_cleaned.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                if len(self.urls) > 2: break
                self.urls.append("http://" + "".join(line[1]))
        print("DONE READING")
        
    def shoot(self, url):
        while True:
            try:
                return self._shoot(url)
            except ConnectionError as ex:
                print('_shoot(%s) failed: %s', url, ex)
                # For example, chrome died before new_tab()
                self.chrome.check_respawn()
                # retry
            except pychrome.UserAbortException as ex:
                # likely be SIGINT
                print('_shoot(%s) failed: %s', url, ex)
                raise 
    
    def _shoot(self, url):
        tab = self.chrome.open_session()
        tab.Page.navigate(url=url, _timeout = 5)
        loaded = threading.Event()
        loaded.wait(15)
        result = tab.Runtime.evaluate(expression="document.documentElement.outerHTML")
        html = result.get('result', {}).get('value', "")
        tab.stop()
        tab.wait(10)
        self.chrome.close_session(tab)
        return html
    
    # finds FBOG or Twitter Card metadata for a given attribute
    def get_attr(self, head, attr):
        try:
            return head.find(attrs={"property": "og:" + attr})['content']
        except TypeError:
            pass
        try:
            return head.find(attrs={"property": "twitter:" + attr})['content']
        except TypeError:
            pass
        try:
            return head.find("title").text
        except AttributeError:
            return ""

    # finds FBOG locale metadata
    def get_locale(self, head):
        try:
            return head.find(attrs={"property": "og:locale"})['content']
        except TypeError:
            return ""

    # returns url, page title, page description, page locale 
    def parse_html(self, url):
        try:
            html = self.shoot(url)
            soup = BeautifulSoup(html, features="html.parser")
            head = soup.head
            title = self.get_attr(head, "title")
            desc = self.get_attr(head, "description")
            locale = self.get_locale(head)
            return [url, title, desc, locale]
        except Exception as e:
            #logger.exception(traceback.format_exc())
            raise
            return [url, str(e)]
        
    def write_meta(self):
        with open(self.PATH + "/meta_good3.csv", 'w') as outf:
            w = csv.writer(outf, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
            for url in self.res:
                w.writerow(url)
        print("WROTE ALL METADATA")

    def main(self):
        time1 = time.time()
        for url in self.urls:
            self.res.append(self.shoot(url))
            print(len(self.res))
        print(self.res)
        time2 = time.time()
        print(f"Took {time2-time1:.2f} s")

if __name__ == "__main__":
    crawler = Crawler()
    crawler.main()
    print("FINISHED RUNNING")
