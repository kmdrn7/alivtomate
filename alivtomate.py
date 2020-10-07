from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import bios
import requests
import random
import json
import time
import unittest

class Alivtomate(unittest.TestCase):
    def setUp(self):
        self.config = bios.read('config.yaml')
        self.server = Server(self.config.get('dailyGrammar').get('browsermobPath') + "bin/browsermob-proxy")
        self.server.start()
        self.proxy = self.server.create_proxy()
        options = webdriver.ChromeOptions()
        options.add_argument('--proxy-server={host}:{port}'.format(host='localhost', port=self.proxy.port))
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920,1080")
        if self.config.get('headless'):
            options.add_argument('--headless')
            print("Chrome is running in headless mode")

        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

    def loginCasMis(self):
        driver = self.driver
        driver.get("https://aliv.lecturer.pens.ac.id/indonesia/?redirect_to=https://aliv.lecturer.pens.ac.id/")

        email_field = driver.find_element_by_id("username")
        email_field.send_keys(self.config.get('username'))

        pass_field = driver.find_element_by_id("password")
        pass_field.send_keys(self.config.get('password'))

        pass_field.send_keys(Keys.RETURN)
        time.sleep(10)

    def prepareH5P(self, url, config):
        driver = self.driver
        driver.get(url);

        phpsessid = ""
        wp_test_cuk = ""
        wp_logged_in = ""
        wp_logged_in_val = ""
        wfwaf = ""
        wfwaf_val = ""

        cukis = driver.get_cookies()

        for cuk in cukis:
            cukname = cuk.get('name')
            cukval = cuk.get('value')
            ###########################################
            if cukname == 'PHPSESSID':
                phpsessid = cukval
                continue
            ###########################################
            if cukname == 'wordpress_test_cookie':
                wp_test_cuk = cukval
                continue
            ###########################################
            if 'wordpress_logged_in' in cukname:
                wp_logged_in = cukname
                wp_logged_in_val = cukval
                continue
            ###########################################
            if 'wfwaf-authcookie' in cukname:
                wfwaf = cukname
                wfwaf_val = cukval
                continue
            ###########################################

        skrip = driver.find_elements_by_xpath("//script[contains(text(), 'H5PIntegration')]")
        token = skrip[0].get_property('innerText')[216:226]

        cookies = {
            'whatsup': 'whatsupman',
            'PHPSESSID': phpsessid,
            'wordpress_test_cookie': wp_test_cuk,
            wp_logged_in: wp_logged_in_val,
            wfwaf: wfwaf_val,
        }
        print(cookies)

        headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://aliv.lecturer.pens.ac.id',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': url,
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,jv;q=0.7',
        }
        print(headers)

        params = (
            ('token', token),
            ('action', 'h5p_setFinished'),
        )
        print(params)

        for Content in self.config.get(config).get('content'):
            print("+----------------------------------------")
            print("| Phrases: " + Content.get('title'))
            print("+----------------------------------------")
            if Content.get('enabled'):
                opened = time.time()
                finished = opened+random.randint(195,348)
                ####################################################
                for itr in range(1, Content.get('iteration')+1):
                    print("+========================================")
                    print("| Iteration: " + str(itr))
                    print("+========================================")
                    ################################################
                    data = {
                        'contentId': Content.get('id'),
                        'score': Content.get('score'),
                        'maxScore': Content.get('score'),
                        'opened': str(opened)[0:10],
                        'finished': str(finished)[0:10]
                    }
                    time.sleep(random.randint(
                        self.config.get('wait_time').get('from'),
                        self.config.get('wait_time').get('to')
                    ))
                    opened = finished+random.randint(234, 509)
                    finished = opened+random.randint(195, 348)
                    response = requests.post('https://aliv.lecturer.pens.ac.id/wp-admin/admin-ajax.php', headers=headers, params=params, cookies=cookies, data=data)
                    print("| " + str(response.content))
                    print("+========================================")
                    print("|")
                    #################################################
            else:
                print("| SKIPPING ....")
                print("+========================================")
                print("|")

    def test_PhraseForPresentation(self):
        self.loginCasMis()

        driver = self.driver
        driver.get("https://aliv.lecturer.pens.ac.id/topic/useful-phrases-for-presentation/");

        phpsessid = ""
        wp_test_cuk = ""
        wp_logged_in = ""
        wp_logged_in_val = ""
        wfwaf = ""
        wfwaf_val = ""

        cukis = driver.get_cookies()

        for cuk in cukis:
            cukname = cuk.get('name')
            cukval = cuk.get('value')
            ###########################################
            if cukname == 'PHPSESSID':
                phpsessid = cukval
                continue
            ###########################################
            if cukname == 'wordpress_test_cookie':
                wp_test_cuk = cukval
                continue
            ###########################################
            if 'wordpress_logged_in' in cukname:
                wp_logged_in = cukname
                wp_logged_in_val = cukval
                continue
            ###########################################
            if 'wfwaf-authcookie' in cukname:
                wfwaf = cukname
                wfwaf_val = cukval
                continue
            ###########################################

        skrip = driver.find_elements_by_xpath("//script[contains(text(), 'H5PIntegration')]")
        token = skrip[0].get_property('innerText')[216:226]

        cookies = {
            'whatsup': 'whatsupman',
            'PHPSESSID': phpsessid,
            'wordpress_test_cookie': wp_test_cuk,
            wp_logged_in: wp_logged_in_val,
            wfwaf: wfwaf_val,
        }
        print(cookies)

        headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://aliv.lecturer.pens.ac.id',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://aliv.lecturer.pens.ac.id/topic/useful-phrases-for-presentation/',
            'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,jv;q=0.7',
        }
        print(headers)

        params = (
            ('token', token),
            ('action', 'h5p_setFinished'),
        )
        print(params)

        for Content in self.config.get('phrases').get('content'):
            print("+----------------------------------------")
            print("| Phrases: " + Content.get('title'))
            print("+----------------------------------------")
            if Content.get('enabled'):
                opened = time.time()
                finished = opened+random.randint(195,348)
                ####################################################
                for itr in range(1, Content.get('iteration')+1):
                    print("+========================================")
                    print("| Iteration: " + str(itr))
                    print("+========================================")
                    ################################################
                    data = {
                        'contentId': Content.get('id'),
                        'score': Content.get('score'),
                        'maxScore': Content.get('score'),
                        'opened': str(opened)[0:10],
                        'finished': str(finished)[0:10]
                    }
                    time.sleep(random.randint(
                        self.config.get('wait_time').get('from'),
                        self.config.get('wait_time').get('to')
                    ))
                    opened = finished+random.randint(234, 509)
                    finished = opened+random.randint(195, 348)
                    response = requests.post('https://aliv.lecturer.pens.ac.id/wp-admin/admin-ajax.php', headers=headers, params=params, cookies=cookies, data=data)
                    print("| " + str(response.content))
                    print("+========================================")
                    print("|")
                    #################################################
            else:
                print("| SKIPPING ....")
                print("+========================================")
                print("|")

    def test_AdvancedVocabulary(self):
        self.loginCasMis()
        self.prepareH5P("https://aliv.lecturer.pens.ac.id/advanced-vocabulary/", "advancedVocab")

    def test_DailyGrammarQuiz(self):
        self.loginCasMis()

        driver = self.driver

        print("+----------------------------------------")
        print("| Daily Grammar                          |")
        print("+----------------------------------------")
        for itr in range(1, self.config.get('dailyGrammar').get('iteration')+1):
            driver.get("https://aliv.lecturer.pens.ac.id/quizzes/daily-grammar-quiz/")
            time.sleep(8)

            self.proxy.new_har('req', options={'captureHeaders': True,'captureContent':True})
            print("+========================================")
            print("| Iteration: " + str(itr))
            print("+========================================")

            startButton = driver.find_element_by_name("startQuiz")
            startButton.click()
            time.sleep(8)

            responseJson = ""
            for ent in self.proxy.har['log']['entries']:
                if (ent['serverIPAddress'] == "202.9.85.28"
                    and ent['request']['url'] == "https://aliv.lecturer.pens.ac.id/wp-admin/admin-ajax.php"
                    and ent['request']['method'] == "POST"
                    and "globalPoints" in ent['response']['content']['text']):
                    responseJson = ent['response']['content']['text']

            idx = 0
            ansABC = ['a', 'b', 'c', 'd']
            if responseJson == "":
                print("Kosong")
            else:
                responseJson = json.loads(responseJson)
                #######################################
                for key in responseJson['json'].keys():
                    for ans in responseJson['json'][key]['correct']:
                        if ans != 1:
                            idx += 1
                        else:
                            break
                #######################################
                print("| Jawaban: " + ansABC[idx])
                print("+========================================")
                print("|")

            liCorrect = driver.find_elements_by_class_name('wpProQuiz_questionListItem')[idx]
            liCorrect.click()
            time.sleep(5)

            submitButton = driver.find_element_by_name('next')
            submitButton.click()
            time.sleep(20)

    def test_DailyDictation(self):
        self.loginCasMis()

        driver = self.driver

        print("+----------------------------------------")
        print("| Daily Dictation                       |")
        print("+----------------------------------------")
        for itr in range(1, self.config.get('dailyDictation').get('iteration')+1):
            driver.get("https://aliv.lecturer.pens.ac.id/quizzes/daily-dictation/")
            time.sleep(8)

            self.proxy.new_har('req', options={'captureHeaders': True,'captureContent':True})
            print("+========================================")
            print("| Iteration: " + str(itr))
            print("+========================================")

            startButton = driver.find_element_by_name("startQuiz")
            startButton.click()
            time.sleep(8)

            responseJson = ""
            for ent in self.proxy.har['log']['entries']:
                if (ent['serverIPAddress'] == "202.9.85.28"
                    and ent['request']['url'] == "https://aliv.lecturer.pens.ac.id/wp-admin/admin-ajax.php"
                    and ent['request']['method'] == "POST"
                    and "globalPoints" in ent['response']['content']['text']):
                    responseJson = ent['response']['content']['text']

            answer = ""
            if responseJson == "":
                print("Kosong")
            else:
                responseJson = json.loads(responseJson)
                #######################################
                for key in responseJson['json'].keys():
                    for ans in responseJson['json'][key]['correct']:
                        answer = ans[0]
                #######################################
                print("| Jawaban: " + answer)
                print("+========================================")
                print("|")

            inputan = driver.find_element_by_xpath("//input[@data-wordlen='"+ str(len(answer)) +"']")
            inputan.send_keys(answer)
            time.sleep(2)

            checkButton = driver.find_element_by_name('check')
            checkButton.click()
            time.sleep(5)

            finishButton = driver.find_element_by_name('next')
            finishButton.click()
            time.sleep(20)

    def tearDown(self):
        self.driver.close()
        self.driver.quit()
        self.proxy.close()
        self.server.stop()

if __name__ == "__main__":
    unittest.main()
