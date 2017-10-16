import urllib.request
from rutermextract import TermExtractor
term_extractor = TermExtractor()
#url, на котором находится список преподователей
link = urllib.request.urlopen('http://itas.pstu.ru')
 
lines = []
for line in link.readlines():
    #взяли все строки с сотрудниками
    #Каждый сотрудник начинается с тегов <li><a href .....
    if line.find(b'<p>') != -1 and line.find(b'a href'):
        lines.append(line)
link.close()

#Переводим bytes в str
for i in range(len(lines)):
    lines[i] = lines[i].decode('utf-8')

#Можно работать как с обычной строкой
for i in range(len(lines)):
    #Убираем все лишнее
    lines[i] = lines[i].replace('\t\t\t<li>', '')
    lines[i] = lines[i].replace('\"', '')
    lines[i] = lines[i].replace('<a href=', '')
    lines[i] = lines[i].replace('target=_blank>', '')
    lines[i] = lines[i].replace('</a></li>', '')
    lines[i] = lines[i].replace('</ul>', '')
    lines[i] = lines[i].replace("\r\n", '')
    lines[i] = lines[i].replace('<p>', '')
    lines[i] = lines[i].replace('</p>', '')
    lines[i] = lines[i].replace('<br />', '')
    lines[i] = lines[i].replace('</a>', '')
    lines[i] = lines[i].replace('title', '')
    lines[i] = lines[i].replace('</>', '')
    lines[i] = lines[i].replace('%A4%D0%B0%D0%B9%D0%B7%D1%80%D0%B0%D1%85%D0%BC%D0%B0%D0%BD%D0%BE%D0%B2_%D0%A0%D1%83%D1%81%D1%82%D0%B0%D0%BC_%D0%90%D0%B1%D1%83%D0%B1%D0%B0%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%B8%D1%87 =', '')
    lines[i] = lines[i].replace('%D0%A8%D0%B5%D1%80%D0%B5%D0%BC%D0%B5%D1%82%D1%8C%D0%B5%D0%B2_%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80_%D0%93%D0%B5%D0%BD%D0%BD%D0%B0%D0%B4%D1%8C%D0%B5%D0%B2%D0%B8%D1%87 =', '')
    lines[i] = lines[i].replace('%D0%9F%D0%BE%D0%B3%D1%83%D0%B4%D0%B8%D0%BD_%D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B9_%D0%9B%D0%B5%D0%BE%D0%BD%D0%B8%D0%B4%D0%BE%D0%B2%D0%B8%D1%87 =', '')
    lines[i] = lines[i].replace('/wiki/index.php/', '')


for i in range(len(lines)):
    print (lines[i])
#Извлекаем ключевые слова
for i in range(len(lines)):
    text = lines[i] #'Сколько .помню себя, был моряк, да старик смотритель. Старик говорил, что нашел меня в пасмурный день на крыльце, я - корзинка ни слова о матери или отце'
    for term in term_extractor(text):
        print (term.normalized, term.count)
