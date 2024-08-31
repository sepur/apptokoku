from django.conf import settings
from django.http import HttpResponse,HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AddBeliForm,BayarForm,AddStokForm,AddBarangForm,MemberBayarForm
import datetime
from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect
from .models import ItemOrder,Barang,Pembeli,Order,Stok,PenjualanBarang
from django.contrib import messages
from decimal import *
from gate.templatetags.number_format import number_format,get_query
import json
from urllib import request
import urllib.request as ur


def coba_api(request):
    #linkk = 'https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json'
    linkk = 'https://mdn.github.io/learning-area/javascript/oojs/json/superheroes.json'
    cb = ur.urlopen(linkk)
    data = json.loads(cb.read())
    return render(request,'barang/coba_api.html',{'data':data,})


def add_barang(request):
    form = AddBarangForm()
    skr = datetime.date.today()
    user = request.user
    if request.method == "POST":
        form = AddBarangForm(request.POST)
        if form.is_valid():
            nama_barang = form.cleaned_data['nama_barang']
            kode_barang = form.cleaned_data['kode_barang']
            ukuran = form.cleaned_data['ukuran']
            satuan = form.cleaned_data['satuan']
            singkatan = form.cleaned_data['singkatan']
            katagori = form.cleaned_data['katagori']
            harga_barang = form.cleaned_data['harga_barang']
            harga_jual = form.cleaned_data['harga_jual']
    
            bar = Barang(nama_barang = nama_barang, kode_barang = kode_barang, ukuran = ukuran,
                satuan = satuan, singkatan = singkatan, katagori = katagori, harga_barang = harga_barang,
                harga_jual = harga_jual,jumlah_stok = 0,cu = user,cdate = skr)
            bar.save()               
            messages.add_message(request, messages.INFO, 'Barang Telah tersimpan')
            return HttpResponseRedirect('/bar/add-barang/' ,{'form':form})
        else:
            form  = AddBarangForm()
            messages.add_message(request, messages.INFO, 'Kode Barang Telah Ada / Yang Anda Inputkan Salah')
    else:
        form  = AddBarangForm()
    return render(request,'barang/add_barang.html',{'form':form})

def addstok_barang(request):
    user = request.user
    skr = datetime.date.today()
    form = AddStokForm()
    show = Stok.objects.filter(status = '1')#tanggal= skr,

    if request.POST:
        form = AddStokForm(request.POST)
        if form.is_valid():
            brg = form.cleaned_data['barang']
            jml = form.cleaned_data['jumlah']
            harga = form.cleaned_data['harga_beli']
            spl = brg[:brg.index('-')]

            ss = Barang.objects.get(kode_barang = spl)
            st = Stok(stok = jml,stok_barang = ss,harga_beli = harga, tanggal = skr, status = '1')
            st.save()
            #sbl = ss.jumlah_stok
            #ss.jumlah_stok = sbl + st.stok
            #ss.save()
            return HttpResponseRedirect('/bar/addstok-barang/' ,{'form':form,'show':show,})
            #return render(request,'barang/add_beli.html',{'form':form,'show':show,'form_bayar':form_bayar, 'total_tagihan': sum([p.total_harga_item for p in show])})
    else:
        form = AddStokForm()
    return render(request,'barang/add_stok.html',{'form':form,'show':show})

def eksekusi_stok(request):
    user = request.user
    skr = datetime.date.today()
    form = AddStokForm()
    show = Stok.objects.filter(status = '1')#tanggal= skr,
    if request.POST:
        for i in request.POST.getlist('id_minta'):
            pik = Stok.objects.get(id=int(i))
            pik.status = 2
            pik.save()
            bar = pik.stok_barang
            sbl = bar.jumlah_stok
            bar.jumlah_stok = sbl + pik.stok
            bar.save()
        messages.add_message(request, messages.INFO,'Stok Berhasil Ditambahkan')
        return HttpResponseRedirect('/bar/addstok-barang/' ,{'form':form,'show':show})
    else:
        form = AddStokForm()
    return render(request,'barang/add_stok.html',{'form':form,'show':show})


def autokomplit(request):
    print('ayaa kadieu 1')
    #if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      q = request.GET.get('term', '')
      masuk_data = get_query(q, ['kode_barang','nama_barang'])
      places = Barang.objects.filter(masuk_data)
      results = []
      for pl in places:
        place_json = {}
        place_json = str(pl.id) + "- " + pl.nama_barang + "- " + pl.ukuran
        results.append(place_json)
      data = json.dumps(results)
    else:
      data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def memberautokomplit(request):
    print('ayaa kadieu 2')
    #if request.is_ajax():
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
      q = request.GET.get('term', '')
      masuk_data = get_query(q, ['nama'])
      places = Pembeli.objects.filter(masuk_data)
      results = []
      for pl in places:
        place_json = {}
        place_json = str(pl.id) + "- " + pl.nama
        results.append(place_json)
      data = json.dumps(results)
    else:
      data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
def addbeli(request):
    user = request.user
    skr = datetime.date.today()
    form = AddBeliForm()
    form_bayar = BayarForm()
    show = ItemOrder.objects.filter(ket_item="Beli", item_order__sts_bayar=None)

    if request.POST:
        form = AddBeliForm(request.POST)
        if form.is_valid():
            brg = form.cleaned_data['barang']
            jml = form.cleaned_data['jumlah']
            spl = brg[:brg.index('-')]

            try:
                ss = Barang.objects.get(kode_barang=spl)
                print('ini brg =', brg, 'ini nama barang =', ss, 'ini stok barang =', ss.jumlah_stok, 'ini type jumlah stok', type(ss.jumlah_stok), 'ini type jumlah', type(jml))

                if ss.jumlah_stok >= int(jml):
                    ss.jumlah_stok -= int(jml)
                    ss.save()
                    jb = PenjualanBarang.objects.create(
                        nama_barang=ss.nama_barang, kobar=ss, ukuran=ss.
                        ukuran,satuan=ss.satuan, singkatan=ss.singkatan,
                        katagori=ss.katagori, harga_barang=ss.harga_barang,
                        harga_jual_langganan=0,
                        harga_jual=ss.harga_jual, cu=request.user, mu=request.user,
                        isi=0)
                    item = ItemOrder(item_barang=jb, tanggal=skr, total_item=int(jml), harga_item=ss.harga_jual, ket_item="Beli")
                    item.total_harga_item = Decimal(item.total_item) * Decimal(item.harga_item)
                    item.save()
                    return HttpResponseRedirect('/bar/add-beli/', {'form': form, 'show': show, 'form_bayar': form_bayar, 'total_tagihan': sum([p.total_harga_item for p in show])})
                
                elif ss.jumlah_stok < int(jml) and ss.jumlah_stok > 0:
                    messages.add_message(request, messages.ERROR, 'Barang yang tersedia kurang, stok tinggal %s !!!' % ss.jumlah_stok)
                
                elif ss.jumlah_stok <= 0:
                    messages.add_message(request, messages.ERROR, 'Stok Barang Kosong !!!')
            
            except Barang.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Stok Barang Tidak Ada')
                return HttpResponseRedirect('/bar/add-beli/', {'form': form, 'show': show, 'form_bayar': form_bayar, 'total_tagihan': sum([p.total_harga_item for p in show])})
    
    return render(request, 'barang/add_beli.html', {'form': form, 'form_bayar': form_bayar, 'show': show, 'total_tagihan': sum([p.total_harga_item for p in show])})

def bayar(request):
    user = request.user
    skr = datetime.date.today()
    form = AddBeliForm()
    form_bayar = BayarForm()
    form_member = MemberBayarForm()
    pmb = Pembeli.objects.get(pk =1)
    show = ItemOrder.objects.filter(ket_item = "Beli",item_order__sts_bayar = None)#tanggal= skr,
    jml_barang = show.count()
    jml_bayar = Decimal(sum([p.total_harga_item for p in show]))
    if request.POST.get('submit') == 'bayar':
        form_bayar = BayarForm(request.POST)
        if form_bayar.is_valid():
            bayar = form_bayar.cleaned_data['bayar']
            pesan = Order(pembeli = pmb, nominal_harus_dibayar = jml_bayar , nominal_pembayaran = bayar,
            nominal_kembalian = Decimal(bayar) - Decimal(jml_bayar), total_barang = jml_barang, tanggal = skr, sts_bayar = 2)
            pesan.save()
            for i in request.POST.getlist('id_minta'):
                pik = ItemOrder.objects.get(id=int(i))
                pik.ket_item = "Bayar"
                pik.item_order = pesan
                pik.save()
            messages.add_message(request, messages.INFO,'Pembayaran Berhasil')
            return HttpResponseRedirect('/bar/print-rinci/%s/' % pesan.id)
        else:
            messages.add_message(request, messages.INFO,' Mohon Periksa Kembali Inputan Anda.')
            form_bayar = BayarForm()
    elif request.POST.get('submit') == 'kasbon':
        form_bayar = BayarForm(request.POST)
        form_member = MemberBayarForm(request.POST)
        if form_bayar.is_valid() and form_member.is_valid():
            bayar = form_bayar.cleaned_data['bayar']
            mbr = form_member.cleaned_data['kode_member']
            spl = mbr[:mbr.index('-')]
            beli_spl = Pembeli.objects.get(pk = spl)
            pesan = Order(pembeli = beli_spl, nominal_harus_dibayar = jml_bayar , nominal_pembayaran = bayar,
            nominal_kembalian = Decimal(bayar) - Decimal(jml_bayar), total_barang = jml_barang, tanggal = skr, sts_bayar = 2)
            pesan.save()
            for i in request.POST.getlist('id_minta'):
                pik = ItemOrder.objects.get(id=int(i))
                pik.ket_item = "Kasbon"
                pik.item_order = pesan
                pik.save()
            messages.add_message(request, messages.INFO,'Pembayaran Berhasil')
            return HttpResponseRedirect('/')

    return render(request,'barang/add_beli.html',{'form':form,'form_bayar':form_bayar,'form_member':form_member})
def print_rinci(request,objects_id):
    user = request.user
    skr = datetime.datetime.now()
    orr = Order.objects.get(pk = objects_id)
    ps = ItemOrder.objects.filter(item_order = objects_id)
    return render(request,'barang/print_item.html',{'ps':ps,'skr':skr,'oid':objects_id,'orr':orr,'uus':user})    


def daftar_kasbon(request):
    user = request.user
    skr = datetime.datetime.now()
    pem = ItemOrder.objects.filter(ket_item ="kasbon")
    
    return render(request,'barang/daftar_kasbon.html',{'pem':pem,'skr':skr,'uus':user})    
