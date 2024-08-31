from django import forms
from django.forms import Textarea
from django.core.exceptions import ValidationError
from .models import KATAGORI_CHOICES,UKURAN_CHOICES,Barang

class AddBeliForm(forms.Form):
    barang = forms.CharField(label="Nama / Kode Barang",widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus','id':'nama_barang','name':'nama_barang'}))
    jumlah = forms.DecimalField(label="Jumlah",initial=1,widget=forms.TextInput(attrs={'id':'count','class':'form-control','alt':'integer'}))

class BayarForm(forms.Form):
    bayar = forms.DecimalField(label="Bayar",widget=forms.TextInput(attrs={'size': 9,'class':'form-control', "onkeyup":"hitung()", "onInput":"showCurrentValue(event)" ,"id":"bayar"}))
    #kode_member = forms.CharField(label="Kode Member",widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus','id':'kode_member','name':'kode_member'}),required =False)

class MemberBayarForm(forms.Form):
    kode_member = forms.CharField(label="Kode Member",widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus','id':'kode_member','name':'kode_member'}),required =False)

class AddStokForm(forms.Form):
    jumlah = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus','id':'stok','name':'stok','alt': 'integer'}))
    #stok = forms.CharField(label="Nama / Kode Barang",widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus','id':'nama_barang','name':'nama_barang'}))
    barang = forms.CharField(label="Nama / Kode Barang",widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':'autofocus','id':'nama_barang','name':'nama_barang'}))
    harga_beli = forms.IntegerField(label="Harga Beli ",widget=forms.TextInput(attrs={'size': 9, 'class':'form-control','alt': 'integer' }),required =False)

class AddBarangForm(forms.Form):
    nama_barang = forms.CharField(label="Nama Barang",widget=forms.TextInput(attrs={'class':'form-control','id':'nama_barang','name':'nama_barang'}))
    kode_barang = forms.CharField(label="Kode Barang",widget=forms.TextInput(attrs={'class':'form-control','id':'kode_barang','name':'kode_barang'}))
    ukuran = forms.CharField(label="Ukuran Barang",widget=forms.TextInput(attrs={'class':'form-control','id':'ukuran','name':'ukuran'}))
    satuan = forms.ChoiceField(label="Satuan", widget=forms.Select(attrs={'class':'form-control',}), choices = UKURAN_CHOICES)
    singkatan = forms.CharField(label="Singakatan",widget=forms.TextInput(attrs={'class':'form-control', 'id':'singkatan','name':'singkatan'}))
    katagori = forms.ChoiceField(label="Satuan", widget=forms.Select(attrs={'class':'form-control',}), choices = KATAGORI_CHOICES)
    harga_barang = forms.IntegerField(label="Harga Beli",widget=forms.TextInput(attrs={'size': 9,'class':'form-control','alt': 'integer'}))
    harga_jual = forms.IntegerField(label="Harga Jual",widget=forms.TextInput(attrs={'size': 9,'class':'form-control','alt': 'integer'}))

    def clean_kode_barang(self):
        kode_barang = self.cleaned_data['kode_barang']
        if Barang.objects.filter(kode_barang=kode_barang).exists():
            raise ValidationError("Kode ini sudah terdaftar")
        return kode_barang
