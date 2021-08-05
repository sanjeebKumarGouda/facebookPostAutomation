# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 19:36:15 2021

@author: Sanjeeb
"""


# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 13:43:12 2021

@author: Sanjeeb
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import sys
from os.path import isfile, join
from os import listdir
import os
from df2gspread import df2gspread as d2g

##### Reading in Google Spreadsheets
def read_google_spreadsheet(sheet_name,worksheet_name,column_list):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Sanjeeb\Desktop\Gramoday\7fbPosting\Google_Spreadsheet_Data-a1102009ecbb.json", scope)
#   creds = ServiceAccountCredentials.from_json_keyfile_name('C:\Users\Sud\Downloads\sudwhatsapp\Whatsapp-df6ca9484ba5.json', scope)
    client = gspread.authorize(creds)
    price_sheet = client.open(sheet_name).worksheet(worksheet_name)
    price_values = price_sheet.get_all_values()
    price_df = pd.DataFrame(price_values[1:], columns = column_list)
    return price_df

##### Writing in Google Spreadsheets
def write_to_google_spreadsheet(sheet_name,df,spreadsheet_key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Sanjeeb\Desktop\Gramoday\7fbPosting\Google_Spreadsheet_Data-a1102009ecbb.json", scope)
    client = gspread.authorize(creds)
    wks_name = sheet_name
    d2g.upload(df, spreadsheet_key, wks_name, credentials=creds,start_cell = 'A1',row_names=False)
    
    
if __name__ == "__main__":

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    #options = Options()
    ##### Handling of Allow Pop Up In Facebook
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    #options.add_argument("--headless")
    options.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2 
    })

    driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)
    driver.get('https://www.facebook.com/')
    
    # Enter your EmailID below
    email = ''
    # Enter your Facebook Password below
    password = ''
    #post = "This post is just to test automation in facebook"
    owner_name = "Sanjeeb"
    
    my_date = datetime.date.today().weekday()
    date_today = datetime.date.today()
    print(date_today)
    #print(my_date)
    l1 = [0,1,2,3,4,5,6]
    l2 = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    week_day_dict = dict(zip(l1,l2))
    #print(week_day_dict)
    print(week_day_dict[my_date])
    
    # Authentication
    # Filling EmailID
    email_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
    email_box.click()
    email_box.send_keys(email)
    # Filling Password
    password_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pass"]')))
    password_box.click()
    password_box.send_keys(password)
    # Clicking LogIN
    login_click = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    login_click.click()
            

    ## Identifying the groups to be posted on
    df_combined = read_google_spreadsheet("Social_Media_Groups","groupDescr",["groupID","groupName","platform","is_gramoday_group (1/0)","dateOfAddition (YYYY-MM-DD)","groupURL","#groupMembers","groupCropCategory","groupCommodity","groupState","groupOccupation","groupLanguage","addedBy","groupEntrantID","dayOfPosting","postCaption"])
    groupPosting_monitoring_df = read_google_spreadsheet("Team KPI Metrics","groupPosting_monitoring",["dateOfPosting","addedBy","platform","groupCropCategory","groupCommodity","#Impressions"])
    df_combined = df_combined[df_combined["platform"] == "facebook"]
    df_combined = df_combined[(df_combined["addedBy"] == owner_name) & (df_combined["dayOfPosting"] == week_day_dict[my_date])]
    print(df_combined.head(10))
    group_list = list(df_combined["groupName"])

    group_language_dict = pd.Series(df_combined["groupLanguage"].values,index = df_combined["groupName"]).to_dict()
    group_url_dict = pd.Series(df_combined["groupURL"].values,index = df_combined["groupName"]).to_dict()
    postCaption_dict = pd.Series(df_combined["postCaption"].values,index = df_combined["groupName"]).to_dict()
    category_dict = pd.Series(df_combined["groupCropCategory"].values,index = df_combined["groupName"]).to_dict()
    commodity_dict = pd.Series(df_combined["groupCommodity"].values,index = df_combined["groupName"]).to_dict()
    impression_dict = pd.Series(df_combined["#groupMembers"].values,index = df_combined["groupName"]).to_dict()
    lst_combine = []
    
    for groups in group_list:
        language = group_language_dict[groups].lower()
        commodity = commodity_dict[groups].lower()
        category = category_dict[groups].lower()
        url = group_url_dict[groups]
        impression = impression_dict[groups]
        try:
            driver.get(url)

            # Create post
            create_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body._6s5d._71pn._-kb.segoe:nth-child(2) div.rq0escxv.l9j0dhe7.du4w35lb div.rq0escxv.l9j0dhe7.du4w35lb:nth-child(6) div.du4w35lb.l9j0dhe7.cbu4d94t.j83agx80 div.j83agx80.cbu4d94t.l9j0dhe7.jgljxmt5.be9z9djy div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb:nth-child(1) div.l9j0dhe7.dp1hu0rb.cbu4d94t.j83agx80:nth-child(1) div.j83agx80.cbu4d94t:nth-child(4) div.bp9cbjyn.j83agx80.cbu4d94t.k4urcfbm div.rq0escxv.d2edcug0.ecyo15nh.hv4rvrfc.dati1w0a.discj3wi div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.taijpn5t.gs1a9yip.kbz25j0m.btwxx1t3.sv5sfqaa.o22cckgh.obtkqiv7.fop5sh7t div.rq0escxv.l9j0dhe7.du4w35lb.qmfd67dx.hpfvmrgz.gile2uim.buofh1pr.g5gj957u.aov4n071.oi9244e8.bi6gxh9e.h676nmdw.aghb5jc5:nth-child(1) div.sjgh65i0 div.j83agx80.l9j0dhe7.k4urcfbm div.rq0escxv.l9j0dhe7.du4w35lb.hybvsw6c.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.k4urcfbm.ni8dbmo4.stjgntxs.sbcfpzgs div.bp9cbjyn.j83agx80.ihqw7lf3.hv4rvrfc.dati1w0a.pybr56ya div.oajrlxb2.b3i9ofy5.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.j83agx80.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.cxgpxx05.d1544ag0.sj5x9vvc.tw6a2znq.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l.bp9cbjyn.orhb3f3m.czkt41v7.fmqxjp7s.emzo65vh.btwxx1t3.buofh1pr.idiwt2bm.jifvfom9.kbf60n1y div.m9osqain.a5q79mjw.gy2v8mqq.jm1wdb64.k4urcfbm.qv66sw1b > span.a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7')))
            create_post.click()


            # Write Post
            write_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body._6s5d._71pn._-kb.segoe:nth-child(2) div.rq0escxv.l9j0dhe7.du4w35lb div.__fb-light-mode.l9j0dhe7.tkr6xdv7 div.rq0escxv.l9j0dhe7.du4w35lb:nth-child(1) div.j83agx80.cbu4d94t.h3gjbzrl.l9j0dhe7 div.iqfcb0g7.tojvnm2t.a6sixzi8.k5wvi7nf.q3lfd5jv.pk4s997a.bipmatt0.cebpdrjk.qowsmv63.owwhemhu.dp1hu0rb.dhp61c6y.l9j0dhe7.iyyx5f41.a8s20v7p:nth-child(2) div.gs1a9yip.rq0escxv.j83agx80.cbu4d94t.kb5gq1qc.taijpn5t.h3gjbzrl div.ll8tlv6m.rq0escxv.j83agx80.taijpn5t.pnzxbu4t.hpfvmrgz.hzruof5a.dflh9lhu.scb9dxdr.guvg9d06.is38vakr.f59ohtjy.aw1xchsf.k9xwq5rp.fyttoq6t div.cjfnh4rs.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.lzcic4wl.ni8dbmo4.stjgntxs.oqq733wu.cwj9ozl2.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.nwpbqux9.iy3k6uwz.e9a99x49.g8p4j16d.bv25afu3.d2edcug0 div.idiwt2bm.lzcic4wl.ni8dbmo4.stjgntxs.l9j0dhe7.dbpd2lw6 div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4:nth-child(1) div.idiwt2bm.lzcic4wl.ni8dbmo4.stjgntxs.l9j0dhe7.dbpd2lw6:nth-child(1) div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4:nth-child(1) div.k4urcfbm.l9j0dhe7.datstx6m.rq0escxv div.l9j0dhe7 div.j83agx80.btwxx1t3 div.j83agx80.cbu4d94t.f0kvp8a6.mfofr4af.l9j0dhe7.ij1vhnid.smbo3krw.oh7imozk div.q5bimw55.rpm2j7zs.k7i0oixp.gvuykj2m.j83agx80.cbu4d94t.ni8dbmo4.eg9m0zos.l9j0dhe7.du4w35lb.ofs802cu.pohlnb88.dkue75c7.mb9wzai9.l56l04vs.r57mb794.kh7kg01d.c3g1iek1.buofh1pr:nth-child(2) div.j83agx80.cbu4d94t.buofh1pr.l9j0dhe7 div.o6r2urh6.buofh1pr.datstx6m.l9j0dhe7.oh7imozk.x68sjeil div.rq0escxv.buofh1pr.df2bnetk.hv4rvrfc.dati1w0a.l9j0dhe7.k4urcfbm.du4w35lb.gbhij3x4:nth-child(1) div.taijpn5t.j83agx80 div.gcieejh5.bn081pho.humdl8nn.izx4hr6d.rq0escxv.oo9gr5id.t5a262vz.o0t2es00.b1v8xokw.datstx6m.f530mmz5.lzcic4wl.ecm0bbzt.rz4wbd8a.sj5x9vvc.a8nywdso.k4urcfbm.o8yuz56k div.rq0escxv.datstx6m.k4urcfbm.a8c37x1j div._5rp7 div._5rpb div.notranslate._5rpu:nth-child(1) div:nth-child(1) div.bi6gxh9e > div._1mf._1mj')))
            write_post.send_keys(postCaption_dict[groups])


            # Click Photo/Video
            click_photo_botton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body._6s5d._71pn._-kb.segoe:nth-child(2) div.rq0escxv.l9j0dhe7.du4w35lb div.__fb-light-mode.l9j0dhe7.tkr6xdv7 div.rq0escxv.l9j0dhe7.du4w35lb:nth-child(1) div.j83agx80.cbu4d94t.h3gjbzrl.l9j0dhe7 div.iqfcb0g7.tojvnm2t.a6sixzi8.k5wvi7nf.q3lfd5jv.pk4s997a.bipmatt0.cebpdrjk.qowsmv63.owwhemhu.dp1hu0rb.dhp61c6y.l9j0dhe7.iyyx5f41.a8s20v7p:nth-child(2) div.gs1a9yip.rq0escxv.j83agx80.cbu4d94t.kb5gq1qc.taijpn5t.h3gjbzrl div.ll8tlv6m.rq0escxv.j83agx80.taijpn5t.pnzxbu4t.hpfvmrgz.hzruof5a.dflh9lhu.scb9dxdr.guvg9d06.is38vakr.f59ohtjy.aw1xchsf.k9xwq5rp.fyttoq6t div.cjfnh4rs.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.lzcic4wl.ni8dbmo4.stjgntxs.oqq733wu.cwj9ozl2.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.nwpbqux9.iy3k6uwz.e9a99x49.g8p4j16d.bv25afu3.d2edcug0 div.idiwt2bm.lzcic4wl.ni8dbmo4.stjgntxs.l9j0dhe7.dbpd2lw6 div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4:nth-child(1) div.idiwt2bm.lzcic4wl.ni8dbmo4.stjgntxs.l9j0dhe7.dbpd2lw6:nth-child(1) div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4:nth-child(1) div.k4urcfbm.l9j0dhe7.datstx6m.rq0escxv div.l9j0dhe7 div.j83agx80.btwxx1t3 div.j83agx80.cbu4d94t.f0kvp8a6.mfofr4af.l9j0dhe7.ij1vhnid.smbo3krw.oh7imozk div.ihqw7lf3.discj3wi.l9j0dhe7:nth-child(3) div.scb9dxdr.sj5x9vvc.dflh9lhu.cxgpxx05.dhix69tm.wkznzc2l.i1fnvgqd.j83agx80.rq0escxv.ibutc8p7.l82x9zwi.uo3d90p7.pw54ja7n.ue3kfks5.tr4kgdav.eip75gnj.ccnbzhu1.dwg5866k.cwj9ozl2.bp9cbjyn div.j83agx80 div.dwxx2s2f.dicw6rsg.kady6ibp.rs0gx3tq:nth-child(1) span.tojvnm2t.a6sixzi8.abs2jz4q.a8s20v7p.t1p8iaqh.k5wvi7nf.q3lfd5jv.pk4s997a.bipmatt0.cebpdrjk.qowsmv63.owwhemhu.dp1hu0rb.dhp61c6y.iyyx5f41 div.oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.pq6dq46d.mg4g778l.btwxx1t3.pfnyh3mw.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.p8dawk7l.dwo3fsh8.ow4ym5g4.auili1gw div:nth-child(1) div.tv7at329.l9j0dhe7.thwo4zme.s45kfl79.emlxlaya.bkmhp75w.spb7xbtv div.iyyx5f41.l9j0dhe7.cebpdrjk.bipmatt0.k5wvi7nf.a8s20v7p.k77z8yql.qs9ysxi8.arfg74bv.n00je7tq.a6sixzi8.tojvnm2t div.bp9cbjyn.j83agx80.datstx6m.taijpn5t.l9j0dhe7.k4urcfbm > i.hu5pjgll.bixrwtb6')))
            click_photo_botton.click()
            
            
            key = str(category + "_" + commodity + "_" + language)
            exe_dict = {"vegetables_potato_hindi":"vegetables_potato_hi", "vegetables_potato_english":"vegetables_potato_en", 
                        "vegetables_onion_hindi":"vegetables_onion_hi", "vegetables_onion_english":"vegetables_onion_en",
                        "vegetables_all_hindi":"vegetables_all_hi", "vegetables_all_english":"vegetables_all_en"}
            i = exe_dict[key]
            path = "C:\\Users\\Sanjeeb\\Downloads\\push_messages_new\\{0}\\{1}\\{2}\\{3}.exe"
            print(path.format(category,commodity, language, i))
            time.sleep(10)
            os.system(path.format(category,commodity, language, i))
            
            print("Waiting for 10 sec to attach file\n")
            time.sleep(10)
            
            
            # click POST
            click_post_botton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'body._6s5d._71pn._-kb.segoe:nth-child(2) div.rq0escxv.l9j0dhe7.du4w35lb div.__fb-light-mode.l9j0dhe7.tkr6xdv7 div.rq0escxv.l9j0dhe7.du4w35lb:nth-child(1) div.j83agx80.cbu4d94t.h3gjbzrl.l9j0dhe7 div.iqfcb0g7.tojvnm2t.a6sixzi8.k5wvi7nf.q3lfd5jv.pk4s997a.bipmatt0.cebpdrjk.qowsmv63.owwhemhu.dp1hu0rb.dhp61c6y.l9j0dhe7.iyyx5f41.a8s20v7p:nth-child(2) div.gs1a9yip.rq0escxv.j83agx80.cbu4d94t.kb5gq1qc.taijpn5t.h3gjbzrl div.ll8tlv6m.rq0escxv.j83agx80.taijpn5t.pnzxbu4t.hpfvmrgz.hzruof5a.dflh9lhu.scb9dxdr.guvg9d06.is38vakr.f59ohtjy.aw1xchsf.k9xwq5rp.fyttoq6t div.cjfnh4rs.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.lzcic4wl.ni8dbmo4.stjgntxs.oqq733wu.cwj9ozl2.io0zqebd.m5lcvass.fbipl8qg.nwvqtn77.nwpbqux9.iy3k6uwz.e9a99x49.g8p4j16d.bv25afu3.d2edcug0 div.idiwt2bm.lzcic4wl.ni8dbmo4.stjgntxs.l9j0dhe7.dbpd2lw6 div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4:nth-child(1) div.idiwt2bm.lzcic4wl.ni8dbmo4.stjgntxs.l9j0dhe7.dbpd2lw6:nth-child(1) div.rq0escxv.pmk7jnqg.du4w35lb.pedkr2u6.oqq733wu.ms05siws.pnx7fd3z.b7h9ocf4.j9ispegn.kr520xx4:nth-child(1) div.k4urcfbm.l9j0dhe7.datstx6m.rq0escxv div.l9j0dhe7 div.j83agx80.btwxx1t3 div.j83agx80.cbu4d94t.f0kvp8a6.mfofr4af.l9j0dhe7.ij1vhnid.smbo3krw.oh7imozk div.ihqw7lf3.discj3wi.l9j0dhe7:nth-child(3) div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.i1fnvgqd.gs1a9yip.owycx6da.btwxx1t3.hv4rvrfc.dati1w0a.discj3wi.b5q2rw42.lq239pai.mysgfdmx.hddg9phg div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.p8fzw8mz.pcp91wgn.iuny7tx3.ipjc6fyt div.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.pq6dq46d.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.l9j0dhe7.abiwlrkh.p8dawk7l.cbu4d94t.taijpn5t.k4urcfbm div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.taijpn5t.bp9cbjyn.owycx6da.btwxx1t3.kt9q3ron.ak7q8e6j.isp2s0ed.ri5dt5u2.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.d1544ag0.tw6a2znq.s1i5eluu.tv7at329 div.bp9cbjyn.j83agx80.taijpn5t.c4xchbtz.by2jbhx6.a0jftqn4 div.rq0escxv.l9j0dhe7.du4w35lb.d2edcug0.hpfvmrgz.bp9cbjyn.j83agx80.pfnyh3mw.j5wkysh0.hytbnt81 span.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.lr9zc1uh.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d3f4x2em.fe6kdd0r.mau55g9w.c8b282yb.iv3no6db.jq4qci2q.a3bd9o3v.lrazzd5p.bwm1u5wc > span.a8c37x1j.ni8dbmo4.stjgntxs.l9j0dhe7.ltmttdrg.g0qnabr5')))
            print("POST button found\n")
            click_post_botton.click()
            print("Waiting for 15 sec after clicking POSt botton\n")
            time.sleep(15)
            print("Congratulation you automated Facebook Post!!!")
            lst = [date_today, owner_name, "facebook", category, commodity, impression]
            lst_combine.append(lst)
        except Exception as e:
            print("Could not send to group")
            print(e)
                
    df_append = pd.DataFrame(lst_combine, columns=["dateOfPosting","addedBy","platform","groupCropCategory","groupCommodity","#Impressions"])
    df1 = df_append.groupby(["dateOfPosting","addedBy","platform","groupCropCategory","groupCommodity"])
    df1.sum().to_csv(r"C:\Users\Sanjeeb\Desktop\Gramoday\7fbPosting\impression3.csv")
    df1 = pd.read_csv(r"C:\Users\Sanjeeb\Desktop\Gramoday\7fbPosting\impression3.csv")
    
    groupPosting_monitoring_df_updated = pd.concat([groupPosting_monitoring_df, df1])
    groupPosting_monitoring_df_updated = groupPosting_monitoring_df_updated.reset_index(drop=True)
    groupPosting_monitoring_df_updated.drop_duplicates(inplace=True)
    write_to_google_spreadsheet("groupPosting_monitoring",groupPosting_monitoring_df_updated,"1CuMsHfynafgUVvd-2dRATKg6K79hW7oaqBaTzgHJQ4o")
    
    
    driver.quit()