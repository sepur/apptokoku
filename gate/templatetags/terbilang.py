from django import template
import locale

locale.setlocale(locale.LC_ALL, '')

register = template.Library()
'''
def terbilang(value):
	value = int(value)
	bunyi = ""
	satuan = ("", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam","Tujuh","Delapan","Sembilan","Sepuluh", "Sebelas")
	if value >= 0 and value < 12:
		bunyi = ' ' + satuan[value]
	if value >= 12 and value < 20:
		bunyi = terbilang(value%10) + ' Belas'
	if value >= 20 and value < 100:
		bunyi = terbilang(value/10) + ' Puluh' + terbilang(value%10)
	if value >= 100 and value < 200:
		bunyi = ' seratus' + terbilang(value - 100)
	if value >= 200 and value < 1000:
		bunyi = terbilang(value/100) + ' Ratus' + terbilang(value%100)
	if value >= 1000 and value < 2000:
		bunyi = ' seribu' + terbilang(value - 1000)
	if value >= 2000 and value < 1000000:
		bunyi = terbilang(value / 1000) + ' Ribu' + terbilang(value % 1000)
	if value >= 1000000 and value < 1000000000:
		bunyi = terbilang(value/1000000) + ' Juta' + terbilang(value % 1000000)
	return bunyi

register.filter('terbilang', terbilang)
'''
def terbilangsen(no):
    # str(no) will result in  56.9 for 56.90 so we used the method which is given below.
    strNo = "%.2f" %no
    n = strNo.split(".")
    rs = terbilang(int(n[0])).strip()
    ps =""
    if(len(n)>=2):
        ps = terbilang(int(n[1])).strip()
        rs = "" + ps+ " Sen"  if(rs.strip()=="") else  (rs + " Rupiah " + ps+ " Sen").strip()
    return rs
register.filter('terbilangsen', terbilangsen)

def terbilang(value):
    value = int(value)
    bunyi = ""
    satuan = ("", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam","Tujuh","Delapan","Sembilan","Sepuluh", "Sebelas")
    if value >= 0 and value < 12:
        bunyi = ' ' + satuan[value]
    if value >= 12 and value < 20:
        bunyi = terbilang(value%10) + ' Belas'
    if value >= 20 and value < 100:
        bunyi = terbilang(value/10) + ' Puluh' + terbilang(value%10)
    if value >= 100 and value < 200:
        bunyi = ' Seratus' + terbilang(value - 100)
    if value >= 200 and value < 1000:
        bunyi = terbilang(value/100) + ' Ratus' + terbilang(value%100)
    if value >= 1000 and value < 2000:
        bunyi = ' Seribu' + terbilang(value - 1000)
    if value >= 2000 and value < 1000000:
        bunyi = terbilang(value / 1000) + ' Ribu' + terbilang(value % 1000)
    if value >= 1000000 and value < 1000000000:
        bunyi = terbilang(value/1000000) + ' Juta' + terbilang(value % 1000000)
    if value >= 1000000000 and value < 1000000000000:
        bunyi = terbilang(value/1000000000) + ' Milyar' + terbilang(value % 1000000000)
    if value >= 1000000000000 and value < 1000000000000000:
        bunyi = terbilang(value/1000000000000) + ' Triliun' + terbilang(value % 1000000000000)
    return bunyi
register.filter('terbilang', terbilang)

def roma(value):
    value = int(value)
    rib = ['','M','MM','MMM']
    rat = ['','C','CC','CCC','CD','D','DC','DCC','DCCC','CM']
    pul = ['','X','XX','XXX','XL','L','LX','LXX','LXXX','XC']
    sat = ['','I','II','III','IV','V','VI','VII','VIII','IX']
    return rib[value/1000] + rat[value%1000/100] + pul[value%100/10] + sat[value%10/1]
register.filter('roma', roma)

def currency(value):
	return locale.currency(value, grouping=True)

register.filter('currency', currency)

def number_tanpa_desimal(number, dec_point=',', thousands_sep='.'):
    try:
        number = round(float(number))
    except ValueError:
    	return number
    except TypeError:
        return number
    neg = number < 0
    integer, fractional = str(abs(number)).split('.')
    m = len(integer) % 3
    if m:
        parts = [integer[:m]]
    else:
        parts = []    
    parts.extend([integer[m+t:m+t+3] for t in xrange(0, len(integer[m:]), 3)])
    return '%s%s' % (neg and '-' or '', thousands_sep.join(parts))

from django.utils.safestring import mark_safe
def negative_positive(value):
    esc =''
    if value < 0 :
        esc = value * - 1
        result = '<FONT COLOR=\"FF0000\">(%s)</FONT>' % number_tanpa_desimal(esc)
    else:
        esc = value
        result = '<FONT COLOR=\"#000000\">%s</FONT>' % number_tanpa_desimal(esc)
    return mark_safe(result)
register.filter('negative_positive', negative_positive)
