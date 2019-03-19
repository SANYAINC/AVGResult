import time, subjectsList
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


def main():
    while True:
        iscode = input('Введите 1, чтобы войти по логину и паролю, либо наберите специальный код:\n')
        if iscode == '1' or iscode == '14ss':
            break
    if iscode == '14ss':
        log = 'snnc'
        pswrd = '14092001'
    else:
        log = input('Пожалуйста, введите логин:\n')
        pswrd = input('И пароль:' + '\n')


    opts = webdriver.ChromeOptions()
    opts.add_argument('headless')
    opts.add_argument('--window-size=1280,1080')
    opts.add_argument("user-agent=Mozilla/5.0 (Linux; Android 8.1.0; Mi A1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36")
    driver = webdriver.Chrome(chrome_options=opts)
    driver.get('https://schools.by/login')

    loginInput = driver.find_element_by_xpath('//*[@id="id_username"]')
    loginInput.send_keys(log)
    pswrdInput = driver.find_element_by_xpath('//*[@id="id_password"]')
    pswrdInput.send_keys(pswrd)
    submitButton = driver.find_element_by_xpath('//*[@id="page_layout"]/div/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/form/div[3]/div/div[1]/div/input')
    submitButton.click()
    try:
        tabsWrap = driver.find_element_by_class_name('tabs1_wrap')
    except NoSuchElementException:
        driver.quit()
        print('Неверный логин/пароль')
        time.sleep(10)
        return None
    journalButton = driver.find_element_by_xpath('//*[@id="pupil_tabs_menu_1124926"]/li[1]/a')
    journalButton.click()
    time.sleep(1.5)

    print('Успешный вход, собираю оценки. Процесс может занять несколько минут.')

    def getmarks(driver):
        days = driver.find_elements_by_class_name('db_day')
        for day in days:
            tbodies = day.find_elements_by_tag_name('tbody')
            for tbody in tbodies:
                rows = tbody.find_elements_by_tag_name('tr')
                for row in rows:
                    mark = row.find_element_by_class_name('mark').text
                    if mark == '':
                        continue
                    if mark.find('/') != -1:
                        parts = mark.split('/')
                        for part in parts:
                            part = int(part)
                            lessonName = row.find_element_by_class_name('lesson').text
                            lessonName = lessonName.replace(lessonName[0:3], '')
                            subjectsList.allSubjectsDic.get(lessonName).append(part)
                        continue
                    mark = int(mark)
                    lessonName = row.find_element_by_class_name('lesson').text
                    lessonName = lessonName.replace(lessonName[0:3], '')
                    subjectsList.allSubjectsDic.get(lessonName).append(mark)

    i=0

    while True:
        try:
            getmarks(driver)
            con = driver.find_elements_by_class_name('db_week')[i]
            con = con.find_element_by_class_name('db_period')
            prev = con.find_element_by_class_name('prev')
            prev.click()
            i = i + 1
            time.sleep(5)
        except:
            break

    print('Оценки собраны, считаю средний балл по каждому предмету.')

    def calculateAvg(markDic):
        basicSum = 0
        for subj in markDic:
            if len(markDic[subj]) != 0:
                for mark in markDic[subj]:
                    basicSum = basicSum + mark
                amount = len(markDic[subj])
                avg = basicSum/amount
                subjectsList.allSubjectsDic2[subj].append(avg)
                basicSum = 0

    calculateAvg(subjectsList.allSubjectsDic)

    print('Средний балл по каждому предмету расчитан, суммирую все...')

    def calcTotal(markDic):
        newLen = len(markDic)
        basicSum = 0
        for subj in markDic:
            if len(markDic[subj]) == 0:
                newLen = newLen - 1
            for avgs in markDic[subj]:
                basicSum = basicSum + avgs
        avg = basicSum/newLen
        basicSum = 0
        return round(avg,2)

    AVG = calcTotal(subjectsList.allSubjectsDic2)

    print('Готово!')

    for subj in subjectsList.allSubjectsDic:
        print(subj, subjectsList.allSubjectsDic[subj])
    print('---------------------------------------------')
    for subj in subjectsList.allSubjectsDic2:
        print(subj, subjectsList.allSubjectsDic2[subj])
    print('---------------------------------------------')
    print(AVG)

    time.sleep(30)

    #return subjectsList.allSubjectsDic, subjectsList.allSubjectsDic2, AVG





if __name__ == '__main__':
    main()
