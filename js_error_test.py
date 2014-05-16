#! /usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import sys
import os
from selenium import webdriver
import time



class JSErrorTest(unittest.TestCase):

    """
    Страницы которые проверяются
    
    1.Главная страница.
    2.Страница каталога без подбора.
    3.Страница каталога с подбором.
    4.Карточка товара.
    5.Корзина.
    6.Страница подтверждения заказа.
    7.Информационная страница.
    8. Страница поиска
    9.Страница сравнения.
    10.Страница «Избранное».

    """
        
   

    ADDRESS = 'http:/%s.%s/' % (os.getenv('CITY'), os.getenv('SITE'))

    profile = webdriver.FirefoxProfile()
    profile.add_extension('JSErrorCollector.xpi')
    profile.set_preference("general.useragent.override", os.getenv('USERAGENT'))#set useragent
    driver = webdriver.Firefox(profile)
    
                

    def tearDown(self):
        """Удаление переменных для всех тестов. Остановка приложения"""

        self.driver.get('%slogout/' % self.ADDRESS)
        self.driver.close()
        if sys.exc_info()[0]:   
            print sys.exc_info()[0]


    def check_errors(self, cnt):
        "Проверяет страницу на наличие ошибок"
        jserrors = self.driver.execute_script('return window.JSErrorCollector_errors.pump()')
        if jserrors:
            for error in jserrors:
                cnt+=1
                print 'На странице ', self.driver.current_url[len(self.ADDRESS):], ' обнаружена JavaScript ошибка:'
                print 'Файл с ошибкой, либо URL страницы: ', error['sourceName']
                print 'Информация об ошибке: ', error['errorMessage']
                print 'Строка содержащая ошибку: ', error['lineNumber']
                print '-'*80
        return cnt

    def test_js_error(self):
        """ 1.Главная страница.
            2.Страница каталога без подбора.
            3.Страница каталога с подбором. """
        
        
        cnt=0

        self.driver.get('%slogin/' % self.ADDRESS)
        self.driver.find_element_by_id('username').send_keys(os.getenv('AUTH'))
        self.driver.find_element_by_id('password').send_keys(os.getenv('AUTHPASS'))
        self.driver.find_element_by_class_name('btn-primary').click()    
        time.sleep(5)
        cnt = self.check_errors(cnt)

        tm_first_icon = self.driver.find_element_by_class_name('headerNav').find_element_by_tag_name('td')
        a = tm_first_icon.find_element_by_tag_name('a').get_attribute('href') #открывается страница шаблона cat, при изменении ТОП-меню, возможны правки
        self.driver.get(a)
        time.sleep(5)
        cnt = self.check_errors(cnt)

        cat_inner = self.driver.find_element_by_class_name('catSegLeft').find_element_by_class_name('segNavi')
        a = cat_inner.find_element_by_tag_name('a').get_attribute('href') #открывается страница шаблона catInner, при изменении ТОП-меню, возможны правки
        self.driver.get(a)
        time.sleep(5)
        cnt = self.check_errors(cnt)


        """4.Карточка товара.
           5.Корзина.
           6.Страница подтверждения заказа."""
       
        print '\n\n'
        card = self.driver.find_element_by_class_name('j-items-frame').find_element_by_class_name('cardCont').find_elements_by_tag_name('a')[1].get_attribute('href')
        self.driver.get(card)
        time.sleep(5)
        cnt = self.check_errors(cnt)

        try:
            self.driver.find_element_by_link_text('Купить').click()
        except:
            print card
            raise Error
        time.sleep(5)
        self.driver.get('%sbasket/' % self.ADDRESS)
        time.sleep(5)
        cnt = self.check_errors(cnt)

        self.driver.find_element_by_id('personal_order_form_comment').send_keys('AutoTEST ORDER - JavaScript errors check script')
        self.driver.find_element_by_class_name('btn-primary').click() #Покупаем товар
        try:
            self.driver.find_element_by_class_name('order-details')
        except:
            print self.driver.current_url
            print 'Ошибка оформления заказа'
            print '-'*80
            cnt += 1
        cnt = self.check_errors(cnt)


        """ 7.Информационная страница."""

        print '\n\n'
        botNav = self.driver.find_elements_by_class_name('lvl2')
        link = []
        for x in botNav:
	    link.extend([y.get_attribute('href') for y in x.find_elements_by_tag_name('a')])
        ext_link =('http://hh.ru/employer/741274','http://ok.terminal.ru/')

        for href in link:
            if href not in ext_link:
                self.driver.get(href)
                time.sleep(5)
                cnt = self.check_errors(cnt)

        """ 8. Страница поиска  """
        
        print '\n\n'
        self.driver.get('%ssearch/?q=Samsung' % self.ADDRESS)
        time.sleep(5)
        cnt = self.check_errors(cnt)
   
        """
        9.Страница сравнения.
        10.Страница «Избранное». """
        
   
        print '\n\n'
        self.driver.get('%scompare/' % self.ADDRESS)
        time.sleep(5)
        cnt = self.check_errors(cnt)
        
        self.driver.get('%sfavorite/' % self.ADDRESS)
        time.sleep(5)
        cnt = self.check_errors(cnt)

             
        assert cnt==0, (u'Errors found: %d')%(cnt)
    
