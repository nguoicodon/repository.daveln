# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/  
'''                                                                           

import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon

mysettings=xbmcaddon.Addon(id='plugin.video.netmedia')
profile=mysettings.getAddonInfo('profile')
home=mysettings.getAddonInfo('path')
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
homemenu=xbmc.translatePath(os.path.join(home, 'userlist.xml'))
homelink='https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/userlist.xml'

if not os.path.exists(homemenu):
  try:
    open(homemenu, 'w+').close()
  except:
    pass  	
	
status=urllib.urlopen(homelink).getcode()
if status==200:
  urllib.urlretrieve (homelink, homemenu)
else:
  pass

def userlist():
  try:
    mainmenu=open(homemenu, 'r')  
    menulink=mainmenu.read()
    mainmenu.close()
    return menulink
  except:
    pass	
	
def makeRequest(url):
  try:
    req=urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
    response=urllib2.urlopen(req)
    link=response.read()
    response.close()  
    return link
  except:
    pass
		
def main():
  content=userlist()
  match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
  for title, url, thumbnail in match:
    if 'Main Menu - ' in title:  
      addDir(title.replace('Main Menu - ',''), url , 2, logos + thumbnail)
    elif 'Main Menu Plus - ' in title:  
      addDir(title.replace('Main Menu Plus - ',''), url , 1, logos + thumbnail)	  
    else:
      pass

def directories():
  addDir('Tin Tức Hải Ngoại', url, 2, logos + 'haingoai.png')
  addDir('Tin Tức Trong Nước', url, 2, logos + 'vietnam.png')
	  
def categories():
  content=userlist()
  match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(content)
  for title, url, thumbnail in match:
    if 'Tin Tức Hải Ngoại' in name:
      if 'OverseaNews' in title:	
        addDir(title.replace('OverseaNews - ',''), url , 3, logos + thumbnail)
      else: pass	
    elif 'Tin Tức Trong Nước' in name:
      if 'NewsInVN' in title:	
        addDir(title.replace('NewsInVN - ',''), url , 3, logos + thumbnail)
      else: pass		  
    elif 'Ca Nhạc' in name:
      if 'Music' in title:	
        addDir(title.replace('Music - ',''), url , 3, logos + thumbnail)
      else: pass		
    elif 'Hài Kịch' in name:
      if 'Sitcom' in title:	
        addDir(title.replace('Sitcom - ',''), url , 3, logos + thumbnail)
      else: pass
    elif 'TV Shows' in name:
      if 'TiviShows' in title:	
        addDir(title.replace('TiviShows - ',''), url , 3, logos + thumbnail)
      else: pass
    elif 'Thể Thao' in name:
      if 'Sports' in title:	
        addDir(title.replace('Sports - ',''), url , 3, logos + thumbnail)
      else: pass
    elif 'Du Lịch' in name:
      if 'Travel' in title:	
        addDir(title.replace('Travel - ',''), url , 3, logos + thumbnail)
      else: pass
    elif 'Y Khoa' in name:
      if 'Medical' in title:	
        addDir(title.replace('Medical - ',''), url , 3, logos + thumbnail)
      else: pass		  
    elif 'Nấu Ăn' in name:
      if 'Cooking' in title:	
        addDir(title.replace('Cooking - ',''), url , 3, logos + thumbnail)
      else: pass		
    elif 'Trang Điểm' in name:
      if 'MakeUp' in title:	
        addDir(title.replace('MakeUp - ',''), url , 3, logos + thumbnail)
      else: pass		
    elif 'Đọc Truyện' in name:
      if 'AudioBook' in title:	
        addDir(title.replace('AudioBook - ',''), url , 3, logos + thumbnail)
      else: pass
    elif 'Những Mục Khác' in name:
      if 'Other' in title:	
        addDir(title.replace('Other - ',''), url , 3, logos + thumbnail)
      else: pass	  
	  
def mediaLists(url):
  content=makeRequest(url)
  if 'youtube' in url:	  
    match=re.compile("player url='(.+?)\&.+?><media.+?url='(.+?)' height=.+?'plain'>(.+?)<\/media").findall(content)
    for url, thumbnail, name in match:
      name = name.replace("&#39;", "'").replace('&amp;', '&').replace('&quot;', '"')
      url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')	  
      addLink(name, url, thumbnail)
    match=re.compile("<link rel='next' type='application\/atom\+xml' href='(.+?)'").findall(content)
    for url in match:  
      addDir('[COLOR yellow]Trang kế tiếp  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]', url.replace('&amp;','&'), 3, icon)		  
  elif 'dailymotion' in url:	    
    match=re.compile('<title>(.+?)<\/title>\s*<link>(.+?)_.+?<\/link>\s*<description>.+?src="(.+?)"').findall(content)
    for name, url, thumbnail in match:  
      name = name.replace("&#039;", "'").replace('&quot;', '"').replace('&amp;', '&').replace('.', ' ')
      url = url.replace('http://www.dailymotion.com/video/', 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=')	  
      addLink(name, url, thumbnail)
    match=re.compile('<dm:link rel="next" href="(.+?)"').findall(content)
    for url in match:  
      addDir('[COLOR lime]Trang kế tiếp  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]', url, 3, icon)	
	  
def resolveUrl(url):
  mediaUrl = url	
  item=xbmcgui.ListItem(path=mediaUrl)
  xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)  
  return

def get_params():
  param=[]
  paramstring=sys.argv[2]
  if len(paramstring)>=2:
    params=sys.argv[2]
    cleanedparams=params.replace('?','')
    if (params[len(params)-1]=='/'):
      params=params[0:len(params)-2]
    pairsofparams=cleanedparams.split('&')
    param={}
    for i in range(len(pairsofparams)):
      splitparams={}
      splitparams=pairsofparams[i].split('=')
      if (len(splitparams))==2:
        param[splitparams[0]]=splitparams[1]
  return param
				  
def addDir(name,url,mode,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok
   
def addLink(name,url,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=4"  
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  liz.setProperty('IsPlayable', 'true')  
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  
                     
params=get_params()
url=None
name=None
mode=None

try:
  url=urllib.unquote_plus(params["url"])
except:
  pass
try:
  name=urllib.unquote_plus(params["name"])
except:
  pass
try:
  mode=int(params["mode"])
except:
  pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
  main()
  
elif mode==1:
   directories()  
  
elif mode==2:
   categories()  

elif mode==3:
   mediaLists(url)
   
elif mode==4:
  resolveUrl(url)
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))