# -*- coding:utf-8 -*-

# author: yangyuchen time:2019/7/9

import requests
from lxml import etree

class mobileLib():
    def __init__(self):
        self.projectAll = [{'name':'香港NIKE', 'project':'鲨鱼:17137,号码短租:13750'},
                           {'name':'nike', 'project':'号码短租:13750,易码:723'}]
        self.typeAll = [{'name':'鲨鱼', 'url':'http://120.79.44.146/index.html', 'version':'20190710'},
                        {'name':'号码短租', 'url':'http://116.62.109.116:8888/help.jsp', 'version':'20190710'},
                        {'name':'易码', 'url':'http://www.51ym.me', 'version':'20190903'}]
        self.type = ''
        self.username = ''
        self.password = ''
        self.token = ''

    def login(self, username='', password='', type=''):
        #login(username='sinyung222',password='35242388', type='鲨鱼')
        self.type = type
        self.username = username
        self.password = password
        if self.type == '鲨鱼':
            url = 'http://www.shayuguoji.com:9180/service.asmx/UserLoginStr?name={username}&psw={password}'.format(username=self.username,password=self.password)
            ret = requests.get(url=url).text
            if ret == '0':
                raise Exception('message:   帐户处于禁止使用状态')
            if ret == '-1':
                raise Exception('message:	调用接口失败')
            if ret == '-2':
                raise Exception('message:	帐户信息错误')
            if ret == '-3':
                raise Exception('message:	用户或密码错误')
            if ret == '-4':
                raise Exception('message:	不是普通帐户')
            if ret == '-30':
                raise Exception('message:	非绑定IP')
            if ret == '':
                raise Exception('message:   调用接口超时异常')
            if len(ret) == 32:
                dianshu = requests.get(url='http://www.shayuguoji.com:9180/service.asmx/GetBalance?name={username}&psw={password}'.format(username=self.username,password=self.password)).text.replace('<string xmlns="http://tempuri.org/">', '').replace('</string>', '').replace('<?xml version="1.0" encoding="utf-8"?>', '').strip()
                self.token = ret
                return str(dianshu)
            raise Exception('message:   %s' % ret)
        if self.type == '号码短租':
            url = 'http://api.jmyzm.com/http.do?action=loginIn&uid={username}&pwd={password}'.format(username=self.username,
                                                                                                     password=self.password)
            ret = requests.get(url=url).text
            if '|' not in ret:
                if ret == 'login_error':
                    raise Exception('messsage:  用户名密码错误')
                if ret == 'message|to_fast_try_again':
                    raise Exception('messsage:  访问过快，限制1秒一次。')
                if ret == 'account_is_closed':
                    raise Exception('messsage:  账号被关闭（登录官网进入安全中心开启）')
                if ret == 'account_is_stoped':
                    raise Exception('messsage:  账号被停用。')
                if ret == 'account_is_locked':
                    raise Exception('messsage:  账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
                raise Exception('message:%s' % ret)
            else:
                self.token = ret.split('|')[1].strip()
                return ''
        if self.type == '易码':
            url = 'http://i.fxhyd.cn:8080/UserInterface.aspx?action=login&username={username}&password={password}'.format(username=self.username,password=self.password)
            ret = requests.get(url=url).text
            if 'success|' not in ret:
                if ret == '1002':
                    raise Exception('message:   参数action不能为空')
                if ret == '1003':
                    raise Exception('message:   参数action错误')
                if ret == '1013':
                    raise Exception('message:   接口功能未开启')
                if ret == '1014':
                    raise Exception('message:   接口登录未开启')
                if ret == '1005':
                    raise Exception('message:   用户名或密码错误')
                if ret == '1006':
                    raise Exception('message:   用户名不能为空')
                if ret == '1007':
                    raise Exception('message:   密码不能为空')
                if ret == '1011':
                    raise Exception('message:   账户待审核')
                if ret == '1012':
                    raise Exception('message:   账户暂停使用')
                if ret == '1009':
                    raise Exception('message:   账户被禁用')
                raise Exception('mesasage:  %s' % ret)
            else:
                self.token = ret.split('|')[1].strip()
                ret = requests.get(url='http://i.fxhyd.cn:8080/UserInterface.aspx?action=getaccountinfo&token={token}').text
                if 'success|' in ret:
                    return ret.split('|')[4]
                else:
                    return ''
    def getMobile(self, project=''):
        projectId = self.getProject(project=project)
        if self.type == '鲨鱼':
            url = 'http://www.shayuguoji.com:9180/service.asmx/GetHM2Str?token={token}&xmid={projectId}&sl=1&lx=0&a1=&a2=&pk=&ks=0&rj=mnbv1775'.format(token=self.token,
                                                                                                                                                       projectId=projectId)
            ret = requests.get(url=url).text
            if ret == '':
                raise Exception('message: 	调用接口超时异常')
            if ret == '-1':
                raise Exception('message:   当前没有合条件号码')
            if ret == '-2':
                raise Exception('message: 	提交取号任务超量，请释放占用号码')
            if ret == '-3':
                raise Exception('message: 	获取号码数量超量，请释放已经做完任务不使用的号码，以便获取新号码。')
            if ret == '-4':
                raise Exception('message: 	该项目已经被禁用，暂停取号做业务	')
            if ret == '-8':
                raise Exception('message: 	帐户余额不足')
            if ret == '-11':
                raise Exception('message: 	帐户余额不足')
            if ret == '-12':
                raise Exception('message: 	该项目不能以获取号码方式工作')
            if ret == '-15':
                raise Exception('message: 	查找不到该专属对应KEY')
            if ret == '0':
                raise Exception('message: 	没登陆或token过期')
            if 'id=' in ret:
                raise Exception('message:   服务器繁忙不能即时分配号码')
            if 'hm=' in ret:
                return ret.replace('hm=', '')
            raise Exception('message:   %s' % ret)
        if self.type == '号码短租':
            url = 'http://api.jmyzm.com/http.do?action=getMobilenum&pid={projectId}&uid={username}&token={token}&mobile=&size=1'.format(projectId=projectId,username=self.username,token=self.token)
            ret = requests.get(url=url).text
            if self.token in ret:
                return ret.split('|')[0].split(';')[0].strip()
            if ret == 'no_data':
                raise Exception('message:   系统暂时没有可用号码了')
            if ret == 'parameter_error':
                raise Exception('message:   传入参数错误')
            if ret == 'not_login':
                raise Exception('message:   没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
            if ret == 'message|to_fast_try_again':
                raise Exception('message:   请稍后再试访问速度过快，建议休眠1秒后再试')
            if ret == 'account_is_closed':
                raise Exception('message:   账号被关闭（登录官网进入安全中心开启）')
            if ret == 'account_is_locked':
                raise Exception('message:   账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
            if ret == 'account_is_stoped':
                raise Exception('message:   账号被停用')
            if ret == 'you_cannot_get':
                raise Exception('message:   使用了项目绑定（登录官网进入安全中心解除绑定或添加该项目绑定） ')
            if ret == 'not_found_project':
                raise Exception('message:   没有找到项目,项目ID不正确')
            if ret == 'Lack_of_balance':
                raise Exception('message:   可使用余额不足')
            if ret == 'max_count_disable':
                raise Exception('message:   已经达到了当前等级可以获取手机号的最大数量，请先处理完您手上的号码再获取新的号码（处理方式：能用的号码就获取验证码，不能用的号码就加黑）')
            if ret == 'unknow_error':
                raise Exception('message:   未知错误,再次请求就会正确返回')
            raise Exception('message:   %s' % ret)
        if self.type == '易码':
            url = 'http://i.fxhyd.cn:8080/UserInterface.aspx?action=getmobile&token={token}&itemid={projectId}&excludeno=170.171.165&timestamp=TIMESTAMP'.format(token=self.token,projectId=projectId)
            ret = requests.get(url=url).text
            if 'success|' not in ret:
                if ret == '1008':
                    raise Exception('message:   账户余额不足')
                if ret == '1010':
                    raise Exception('message:   参数错误')
                if ret == '2001':
                    raise Exception('message:   参数itemid不能为空')
                if ret == '2002':
                    raise Exception('message:   项目不存在')
                if ret == '2003':
                    raise Exception('message:   项目未启用')
                if ret == '2004':
                    raise Exception('message:   暂时没有可用的号码')
                if ret == '2005':
                    raise Exception('message:   获取号码数量已达到上限')
                if ret == '2008':
                    raise Exception('message:   号码已离线')
                if ret == '2010':
                    raise Exception('message:   号码正在使用中')
            else:
                return ret.split('|')[1]

    def getMobileCap(self, mobile='', project=''):
        projectId = self.getProject(project=project)
        if self.type == '鲨鱼':
            url = 'http://www.shayuguoji.com:9180/service.asmx/GetYzm2Str?token={token}&xmid={projectId}&hm={mobile}&sf=1'.format(token=self.token,projectId=projectId,mobile=mobile)
            ret = requests.get(url=url).text
            if ret == '1':
                raise Exception('message:   卡商还没接收到验证信息，等待返回验证码信息')
            if ret == '0':
                raise Exception('message:   	没登陆或token过期')
            if ret == '-1':
                raise Exception('message:   	该号码已经已经被卡商注销。')
            if ret == '-2':
                raise Exception('message:   	业务已被取消，可重试重新操作语音验证')
            if ret == '-3':
                raise Exception('message:   	业务异常中止')
            if ret == '-8':
                raise Exception('message:   	余额不足扣费')
            if ret == '-9':
                raise Exception('message:   	专属数据出错')
            if len(ret) >=4:
                return ret
            raise Exception('message:   %s' % ret)
        if self.type == '号码短租':
            url = 'http://api.jmyzm.com/http.do?action=getVcodeAndReleaseMobile&uid={username}&token={token}&mobile={mobile}'.format(username=self.username,token=self.token,mobile=mobile)
            ret = requests.get(url=url).text
            if mobile in ret:
                return ret.split('|')[1].strip()
            if ret == 'not_receive':
                raise Exception('message:   还没有接收到验证码,请让程序等待几秒后再次尝试')
            if ret == 'parameter_error':
                raise Exception('message:   传入参数错误')
            if ret == 'not_login':
                raise Exception('message:   没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
            if ret == 'message|to_fast_try_again':
                raise Exception('message:   请稍后再试访问速度过快，建议休眠1秒后再试')
            if ret == 'account_is_closed':
                raise Exception('message:   账号被关闭（登录官网进入安全中心开启）')
            if ret == 'account_is_locked':
                raise Exception('message:   账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
            if ret == 'account_is_stoped':
                raise Exception('message:   账号被停用')
            if ret == 'Lack_of_balance':
                raise Exception('message:   可使用余额不足')
            if ret == 'not_found_moblie':
                raise Exception('message:   没有找到手机号')
            if ret == 'not_found_project':
                raise Exception('message:   没有找到项目,项目ID不正确')
            raise Exception('message:   %s' % ret)
        if self.type == '易码':
            url = 'http://i.fxhyd.cn:8080/UserInterface.aspx?action=getsms&token={token}&itemid={projectId}&mobile={mobile}&release=1&timestamp=TIMESTAMP'.format(token=self.token,projectId=projectId,mobile=mobile)
            ret = requests.get(url=url).text
            if 'success|' not in ret:
                if ret == '2006':
                    raise Exception('message:   参数mobile不能为空')
                if ret == '2001':
                    raise Exception('message:   参数itemid不能为空')
                if ret == '2002':
                    raise Exception('message:   项目不存在')
                if ret == '2003':
                    raise Exception('message:   项目未启用')
                if ret == '1008':
                    raise Exception('message:   账户余额不足')
                if ret == '2007':
                    raise Exception('message:   号码已被释放')
                if ret == '3001':
                    raise Exception('message:   尚未收到短信')
                if ret == '2008':
                    raise Exception('message:   号码已离线')
            else:
                return ret.split('|')[1].strip()
    def addIgnoreList(self, mobile='', project=''):
        projectId=self.getProject(project=project)
        if self.type == '鲨鱼':
            url = 'http://www.shayuguoji.com:9180/service.asmx/Hmd2Str?token={token}&xmid={projectId}&hm={mobile}&sf=1'
            ret = requests.get(url=url).text
            if ret == '1':
                return
            if ret == '':
                raise Exception('message:   调用接口超时异常')
            if ret == '0':
                raise Exception('message:   没登陆或失败')
            if ret == '-1':
                raise Exception('message:   增加失败')
            if ret == '-2':
                raise Exception('message:   号码黑名单已经存在，不需要重复增加')
            raise Exception('message:   %s' % ret)
        if self.type == '号码短租':
            url = 'http://api.jmyzm.com/http.do?action=addIgnoreList&uid={username}&token={token}&mobiles={mobile}&pid={projectId}'.format(username=self.username,token=self.token,mobile=mobile,projectId=projectId)
            ret = requests.get(url=url).text
            if ret == '1':
                return
            else:
                if ret == 'parameter_error':
                    raise Exception('message:   传入参数错误')
                if ret == 'not_login':
                    raise Exception('message:   没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值')
                if ret == 'message|to_fast_try_again':
                    raise Exception('message:   请稍后再试访问速度过快，建议休眠500毫秒后再试')
                if ret == 'account_is_closed':
                    raise Exception('message:   账号被关闭（登录官网进入安全中心开启）')
                if ret == 'account_is_locked':
                    raise Exception('message:   账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）')
                if ret == 'account_is_stoped':
                    raise Exception('message:   账号被停用')
                if ret == 'unknow_error':
                    raise Exception('message:   未知错误,再次请求就会正确返回')
                raise Exception('message:   %s' % ret)
        if self.type == '易码':
            url = 'http://i.fxhyd.cn:8080/UserInterface.aspx?action=addignore&token={token}&itemid={projectId}&mobile={mobile}'.format(token=self.token,projectId=projectId,mobile=mobile)
            ret = requests.get(url=url).text
            if ret == 'success':
                return
            else:
                if ret == '2001':
                    raise Exception('message:   	参数itemid不能为空')
                if ret == '2006':
                    raise Exception('message:   	参数mobile不能为空')
                if ret == '1010':
                    raise Exception('message:   	参数错误')
                if ret == '2007':
                    raise Exception('message:   	号码已被释放')

    def getProject(self, project=''):
        for a in self.projectAll:
            if a['name'] == project:
                for b in a['project'].split(','):
                    if b.split(':')[0] == self.type:
                        return b.split(':')[1]
        raise Exception('message: 未找到对应的项目ID 请联系作者添加')
if __name__ == '__main__':
    MOBILE = mobileLib()
    print(MOBILE.login(username='',password='', type='鲨鱼'))
    print(MOBILE.getMobile(project='香港NIKE'))
    #MOBILE.login(username='mnbv1775',password='990726ccl',type='号码短租')